package extract

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strings"
	"sync"

	"golang.org/x/net/html"
	"golang.org/x/net/html/atom"
)

const (
	MAX_REQUESTS = 50
)

const (
	TYPE_KB         = iota
	TYPE_KB_EXTRACT = iota
	TYPE_FORUM      = iota
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
	bytes, err := io.ReadAll(res.Body)
	if err != nil {
		log.Fatalf("error: %s\n", err.Error())
	}
	data := string(bytes)
	reader := strings.NewReader(data)
	parseTree, err := html.Parse(reader)
	if err != nil {
		log.Fatalf("error: %s\n", err.Error())
	}

	switch t.taskType {
	case TYPE_KB:
		return handleKBTask(&t, parseTree)
	case TYPE_KB_EXTRACT:
		handleKBExtractTask(&t, parseTree)
	case TYPE_FORUM:
		return handleForumTask(&t, parseTree)
	default:
		log.Fatalf("[ERROR] no handler for url %s", t.url)
	}
	return make([]task, 0, 0)
}

func handleKBTask(t *task, n *html.Node) []task {
	newTasks := make([]task, 0, 0)
	fmt.Printf("[INFO] Batch [%d] Processing url %s\n", t.batchId, t.url)

	nodes := make([]*html.Node, 10)
	nodes = append(nodes, n)
	for len(nodes) > 0 {
		node := nodes[0]
		nodes = nodes[1:]

		if node == nil {
			continue
		}

		if node.Type == html.ElementNode && node.DataAtom == atom.Div {
			for _, a := range node.Attr {
				if a.Key != "class" || a.Val != "toc-main" {
					continue
				}
				for descendant := range node.Descendants() {
					if descendant.Type != html.ElementNode && descendant.DataAtom != atom.A {
						continue
					}
					for _, a := range descendant.Attr {
						if a.Key != "href" {
							continue
						}
						newTasks = append(newTasks, task{url: strings.Trim(a.Val, " "), taskType: TYPE_KB_EXTRACT})
					}
				}
			}
		}

		for child := node.FirstChild; child != nil; child = child.NextSibling {
			nodes = append(nodes, child)
		}
	}

	return newTasks
}

func handleKBExtractTask(t *task, n *html.Node) {
	fmt.Println(t.url)
}

func handleForumTask(t *task, n *html.Node) []task {
	newTasks := make([]task, 0, 0)
	fmt.Printf("[INFO] Batch [%d] Processing url %s\n", t.batchId, t.url)
	return newTasks
}
