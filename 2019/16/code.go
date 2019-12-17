package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
	"time"
)

func toDigits(s string) (digits []int) {
	digits = make([]int, len(s))
	for i := range s {
		digits[i] = int(s[i] - '0')
	}
	return
}

func worstFFT(digitsIn []int) (digitsOut []int) {
	digitsOut = make([]int, len(digitsIn))
	pattern := []int{0, 1, 0, -1}
	for i := range digitsOut {
		var value int
		for j := i; j < len(digitsOut); j++ {
			value += digitsIn[j] * pattern[((j+1)/(i+1))%len(pattern)]
		}
		value %= 10
		if value < 0 {
			digitsOut[i] = -value
		} else {
			digitsOut[i] = value
		}
	}
	return
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func sum(digits []int, pos, block int) (result int) {
	if pos < len(digits) {
		for i := pos; i < len(digits); i += 4 * block {
			if i+block > len(digits) {
				block = len(digits) - i
			}
			for j := 0; j < block; j++ {
				result += digits[i+j]
			}
		}
	}
	return
}

func betterFFT(digitsIn []int) (digitsOut []int) {
	// NOTE: Still O(n²)
	digitsOut = make([]int, len(digitsIn))
	for i := range digitsOut {
		var value int
		value = sum(digitsIn, i, i+1) - sum(digitsIn, i+2*(i+1), i+1)
		value %= 10
		if value < 0 {
			digitsOut[i] = -value
		} else {
			digitsOut[i] = value
		}
	}
	return
}

func weirdFFT(digitsIn []int) (digitsOut []int) {
	digitsOut = make([]int, len(digitsIn))
	var s int
	for i := range digitsOut {
		idx := len(digitsIn) - i - 1
		s += digitsIn[idx]
		digitsOut[idx] = s % 10
	}
	return
}

func part1(input string, phases int) {
	digits := toDigits(input)
	start := time.Now()
	for i := 0; i < phases; i++ {
		digits = betterFFT(digits)
	}
	fmt.Printf("After %3d phases of FFT (len=%d): %v\n", phases, len(digits), digits[:8])
	fmt.Println(time.Since(start))
}

func part2(input string, phases int) {
	offset, _ := strconv.Atoi(input[:7])
	digits := toDigits(strings.Repeat(input, 10000))
	start := time.Now()
	for i := 0; i < phases; i++ {
		digits = weirdFFT(digits)
	}
	fmt.Printf("After %3d phases of FFT (len=%d): %v\n", phases, len(digits), digits[offset:offset+8])
	fmt.Println(time.Since(start))
}

func main() {
	signal, err := ioutil.ReadFile("input.txt")
	if err != nil {
		panic(err)
	}
	str := string(signal)
	part1(str, 100)
	part2(str, 100)
}
