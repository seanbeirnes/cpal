package main

import (
	"fmt"
	"log"
	"os"

	"github.com/seanbeirnes/cpal/pipeline/internal/extract"
)

func main() {
	logFile, err := os.Create("extractor.log")
	if err != nil {
		errorMsg := fmt.Sprintf("[ERROR] Could not open log file: %s", err.Error())
		log.Fatalln(errorMsg)
	}
	defer logFile.Close()
	log.SetOutput(logFile)

	greetMsg := "[INFO] Starting data extractor..."
	fmt.Println(greetMsg)
	log.Println(greetMsg)

	config, err := extract.LoadConfig("config.json")
	if err != nil {
		errorMsg := fmt.Sprintf("[ERROR] Could not open config file: %s", err.Error())
		fmt.Println(errorMsg)
		log.Fatalln(errorMsg)
	}

	extract.Run(config)

	finishMsg := "[INFO] Process complete! Exiting..."
	fmt.Println(finishMsg)
	log.Println(finishMsg)
}
