package main

import (
	"fmt"
	"testing"
)

func BenchmarkRecursiveFibonacci(b *testing.B) {
	for i := 0; i < b.N; i++ {
		_ = RecursiveFibonacci(30)
	}
}

func BenchmarkBinarySearch(b *testing.B) {
	benchmarks := []struct {
		arraySize int
		needle    int
	}{
		{10, 5},
		{100, 5},
		{1000, 5},
		{10000, 5},
	}
	for _, bm := range benchmarks {
		haystack := make([]int, bm.arraySize)
		b.Run(fmt.Sprintf("size-%d", bm.arraySize), func(b *testing.B) {
			b.ResetTimer()
			for i := 0; i < b.N; i++ {
				binarySearch(bm.needle, haystack)
			}
		})
	}
}
