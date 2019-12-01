package problems

import (
	"log"
	"time"
)

// Very neat time tracking function using "defer"
// See https://coderwall.com/p/cp5fya/measuring-execution-time-in-go
func TimeTrack(start time.Time, name string) {
	elapsed := time.Since(start)
	log.Printf("%s took %s", name, elapsed)
}
