package main

// From https://www.golangprograms.com/golang-program-for-implementation-of-binary-search.html

import (
	"fmt"
	"os"
	"runtime/pprof"
	"time"
)

func binarySearch(needle int, haystack []int) bool {

	low := 0
	high := len(haystack) - 1

	for low <= high {
		median := (low + high) / 2

		if haystack[median] < needle {
			low = median + 1
		} else {
			high = median - 1
		}
	}

	if low == len(haystack) || haystack[low] != needle {
		return false
	}

	return true
}

func RecursiveFibonacci(n int) int {
	if n <= 1 {
		return n
	}
	return RecursiveFibonacci(n-1) + RecursiveFibonacci(n-2)
}

func main() {
	f, err := os.Create("cpu_profile.pprof")
	if err != nil {
		panic(err)
	}
	defer f.Close()

	if err := pprof.StartCPUProfile(f); err != nil {
		panic(err)
	}
	defer pprof.StopCPUProfile()

	items := []int{1, 2, 9, 20, 31, 45, 63, 70, 100}
	fmt.Println(binarySearch(63, items))

	time.Sleep(5 * time.Second)
}
