package problems

import (
	"bufio"
	"os"
	"strconv"
	"time"
)

func getFuelMassPart1(mass int) int {
	return mass/3 - 2
}

func getFuelMassPart2(mass int) int {
	totalFuelMass := 0

	for {
		mass = mass/3 - 2
		if mass < 0 {
			break
		}
		totalFuelMass += mass
	}

	return totalFuelMass
}

func SolveDayOne(path string) (int, int) {
	defer TimeTrack(time.Now(), "Day 1 The Tyranny of the Rocket Equation")

	inFile, _ := os.Open(path)
	defer inFile.Close()

	scanner := bufio.NewScanner(inFile)
	resultPartOne := 0
	resultPartTwo := 0
	for scanner.Scan() {
		mass, _ := strconv.Atoi(scanner.Text())
		resultPartOne += getFuelMassPart1(mass)
		resultPartTwo += getFuelMassPart2(mass)
	}
	return resultPartOne, resultPartTwo
}
