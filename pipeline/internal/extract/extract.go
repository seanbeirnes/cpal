package extract

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"sync"
)

const (
	MAX_REQUESTS = 25
)

const (
	TYPE_KB    = iota
	TYPE_FORUM = iota
)

type Config struct {
	KBEntryPoints    []string `json:"kb_entry_point_urls"`
	ForumEntryPoints []string `json:"forum_entry_point_urls"`
	HtmlStoragePath  string   `json:"html_storage_path"`
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
	ch := make(chan []task, MAX_REQUESTS * 100)
	numBatches := 0

	for len(queue) > 0 {
		numRequests := 0
		for ; numRequests < MAX_REQUESTS && len(queue) > 0; numRequests++ {
			t := queue[0]
			t.batchId = numBatches
			queue = queue[1:]
			wg.Add(1)
			go func() {
				defer func() { wg.Done() }()
				ch <- processTask(t)
			}()
		}

		for _ = range numRequests {
			newTasks := <- ch
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
	switch t.taskType {
	case TYPE_KB:
		return handleKBTask(&t)
	case TYPE_FORUM:
		return handleForumTask(&t)
	default:
		log.Fatalf("[ERROR] no handler for url %s", t.url)
	}
	return make([]task, 0, 0)
}

func handleKBTask(t *task) []task {
	newTasks := make([]task, 0, 0)
	fmt.Printf("[INFO] Batch [%d] Processing url %s\n", t.batchId, t.url)
	return newTasks
}

func handleForumTask(t *task) []task {
	newTasks := make([]task, 0, 0)
	fmt.Printf("[INFO] Batch [%d] Processing url %s\n", t.batchId, t.url)
	return newTasks
}
