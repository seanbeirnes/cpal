package extract

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"sync"

	htmltomarkdown "github.com/JohannesKaufmann/html-to-markdown/v2"
	"github.com/PuerkitoBio/goquery"
)

const (
	MAX_REQUESTS = 50
	FPATH_TMP    = "tmp"
	FPATH_RAW    = "raw"
)

const (
	TYPE_KB            = iota
	TYPE_KB_EXTRACT    = iota
	TYPE_FORUM         = iota
	TYPE_FORUM_EXTRACT = iota
)

type Config struct {
	KBEntryPoints    []string `json:"kb_entry_point_urls"`
	ForumEntryPoints []string `json:"forum_entry_point_urls"`
	HtmlStoragePath  string   `json:"html_storage_path"`
	BaseUrl          string   `json:"base_url"`
}

type task struct {
	taskType int
	url      string
	batchId  int
	taskId   int
	urlTitle string
}

func LoadConfig(filename string) (*Config, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, fmt.Errorf("error opening config file: %w", err)
	}
	defer file.Close()

	decoder := json.NewDecoder(file)
	config := &Config{}
	err = decoder.Decode(config)
	if err != nil {
		return nil, fmt.Errorf("error decoding config file: %w", err)
	}

	return config, nil
}

func Run(config *Config) {
	queue := make([]task, 0)
	for _, url := range config.KBEntryPoints {
		task := task{
			taskType: TYPE_KB,
			url:      url,
		}
		queue = append(queue, task)
	}
	for _, url := range config.ForumEntryPoints {
		task := task{
			taskType: TYPE_FORUM,
			url:      url,
		}
		queue = append(queue, task)
	}

	var wg sync.WaitGroup
	ch := make(chan []task)
	numBatches := 0
	numTasks := 0

	for len(queue) > 0 {
		numRequests := 0
		for ; numRequests < MAX_REQUESTS && len(queue) > 0; numRequests++ {
			t := queue[0]
			queue = queue[1:]
			t.batchId = numBatches
			if len(t.url) <= 1 || t.url == "/" || t.url == config.BaseUrl || t.url == config.BaseUrl+"/" {
				fmt.Printf("\033[0;33m[WARN] URL rejected for invalid format: %s\033[0m\n", t.url)
				numRequests--
				continue
			}
			if strings.HasPrefix(t.url, "/") {
				newUrl := fmt.Sprintf("%s%s", config.BaseUrl, t.url)
				t.url = newUrl
			}
			t.taskId = numTasks
			numTasks++

			wg.Add(1)
			go func() {
				defer func() { wg.Done() }()
				ch <- processTask(t)
			}()
		}

		for _ = range numRequests {
			newTasks := <-ch
			for i := range newTasks {
				queue = append(queue, newTasks[i])
			}
		}

		numBatches++
	}
	wg.Wait()
	close(ch)
}

func processTask(t task) []task {
	res, err := http.Get(t.url)
	if err != nil {
		log.Fatalf("[ERROR]: %s\n", err.Error())
		fmt.Printf("[ERROR]: %s\n", err.Error())
	}
	defer res.Body.Close()
	if res.StatusCode != 200 {
		msg := fmt.Sprintf("[ERROR] Non-200 status code: %d", res.StatusCode)
		fmt.Println(msg)
		log.Println(msg)
	}
	doc, err := goquery.NewDocumentFromReader(res.Body)
	if err != nil {
		log.Fatalf("[ERROR]: %s\n", err.Error())
		fmt.Printf("[ERROR]: %s\n", err.Error())
	}

	switch t.taskType {
	case TYPE_KB:
		return handleKBTask(&t, doc)
	case TYPE_KB_EXTRACT:
		handleKBExtractTask(&t, doc)
	case TYPE_FORUM:
		return handleForumTask(&t, doc)
	case TYPE_FORUM_EXTRACT:
		handleForumExtractTask(&t, doc)
	default:
		log.Fatalf("[ERROR] no handler for url %s", t.url)
	}
	return make([]task, 0, 0)
}

func handleKBTask(t *task, doc *goquery.Document) []task {
	newTasks := make([]task, 0, 0)
	fmt.Printf("[INFO] Batch [%d] Processing url %s\n", t.batchId, t.url)

	selection := doc.Find(".toc-main")
	selection.First().Find("a").Each(func(i int, s *goquery.Selection) {
		url, _ := s.Attr("href")
		newTasks = append(newTasks, task{url: strings.Trim(url, " "), urlTitle: s.Text(), taskType: TYPE_KB_EXTRACT})
	})

	return newTasks
}

func handleKBExtractTask(t *task, doc *goquery.Document) {
	fmt.Printf("[INFO] Batch [%d] Extracting data from %s\n", t.batchId, t.url)
	selection := doc.Find("#lia-main-aria-landmark")
	html, err := selection.Html()
	if err != nil {
		log.Fatalf("error: %s\n", err.Error())
	}
	markdown, err := htmltomarkdown.ConvertString(html)
	if err != nil {
		log.Fatalf("error: %s\n", err.Error())
	}
	err = writeMdFile(t, markdown)
	if err != nil {
		msg := fmt.Sprintf("[ERROR] Could not write md file for %s\n", t.url)
		log.Fatalln(msg)
		fmt.Println(msg)
	}

	err = writeJsonFile(t)
	if err != nil {
		msg := fmt.Sprintf("[ERROR] Could not write json file for %s\n", t.url)
		log.Fatalln(msg)
		fmt.Println(msg)
	}
}

func handleForumTask(t *task, doc *goquery.Document) []task {
	newTasks := make([]task, 0, 0)
	fmt.Printf("[INFO] Batch [%d] Processing forum url %s\n", t.batchId, t.url)
	doc.Find(".solved-msg h3 > a").Each(func(i int, s *goquery.Selection) {
		url, _ := s.Attr("href")
		newTasks = append(newTasks, task{url: strings.Trim(url, " "), urlTitle: s.Text(), taskType: TYPE_FORUM_EXTRACT})
	})
	doc.Find(".lia-paging-page-next.lia-component-next > a").Each(func(i int, s *goquery.Selection) {
		url, ok := s.Attr("href")
		if ok {
			msg := fmt.Sprintf("[INFO] Found new forum page: %s", url)
			fmt.Println(msg)
			log.Println(msg)
			newTasks = append(newTasks, task{url: strings.Trim(url, " "), taskType: TYPE_FORUM})
		}
	})

	return newTasks
}

func handleForumExtractTask(t *task, doc *goquery.Document) {
	fmt.Printf("[INFO] Batch [%d] Extracting forum data from %s\n", t.batchId, t.url)
	concatMarkdown := "## Question\n"
	doc.Find("#bodyDisplay .lia-message-body-content > p").Each(func(i int, s *goquery.Selection) {
		html, err := s.Html()
		if err != nil {
			log.Fatalf("error: %s\n", err.Error())
		}
		markdown, err := htmltomarkdown.ConvertString(html)
		if err != nil {
			log.Fatalf("error: %s\n", err.Error())
		}
		concatMarkdown += markdown
	})

	concatMarkdown += "\n\n## Answers\n"
	doc.Find("#threadeddetailmessagelist .lia-message-body-content").Each(func(i int, s *goquery.Selection) {
		html, err := s.Html()
		if err != nil {
			log.Fatalf("error: %s\n", err.Error())
		}
		markdown, err := htmltomarkdown.ConvertString(html)
		if err != nil {
			log.Fatalf("error: %s\n", err.Error())
		}
		concatMarkdown += markdown
	})

	err := writeMdFile(t, concatMarkdown)
	if err != nil {
		msg := fmt.Sprintf("[ERROR] Could not write md file for %s\n", t.url)
		log.Fatalln(msg)
		fmt.Println(msg)
	}

	err = writeJsonFile(t)
	if err != nil {
		msg := fmt.Sprintf("[ERROR] Could not write json file for %s\n", t.url)
		log.Fatalln(msg)
		fmt.Println(msg)
	}
}

/*
 * Utility functions
 */

func makeMetadata(t *task) map[string]string {
	metadata := make(map[string]string)
	metadata["source_url"] = t.url
	metadata["source_url_title"] = t.urlTitle
	metadata["id"] = strconv.Itoa(t.taskId)
	taskType := ""
	switch t.taskType {
	case TYPE_KB_EXTRACT:
		taskType = "kb"
	case TYPE_FORUM_EXTRACT:
		taskType = "forum"
	default:
		log.Printf("[WARN] Unknown task type for JSON data conversion: %s\n", t.url)
	}
	metadata["type"] = taskType
	return metadata
}

func writeMdFile(t *task, markdown string) error {
	mdPath := filepath.Join(FPATH_TMP, FPATH_RAW, strconv.Itoa(t.taskId)+".md")
	mdFile, err := os.Create(mdPath)
	if err != nil {
		return err
	}
	mdFile.WriteString(markdown)

	return nil
}

func writeJsonFile(t *task) error {
	jsonPath := filepath.Join(FPATH_TMP, FPATH_RAW, strconv.Itoa(t.taskId)+".json")
	jsonFile, err := os.Create(jsonPath)
	if err != nil {
		return err
	}
	jsonData, err := json.MarshalIndent(makeMetadata(t), "", "    ")
	jsonFile.Write(jsonData)

	return nil
}
