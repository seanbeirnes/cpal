package main

import (
	"fmt"
	"log"
	"os"
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
}
