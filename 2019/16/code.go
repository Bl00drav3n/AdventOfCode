package main

import (
	"fmt"
	"io/ioutil"
)

func toDigits(s string) (digits []int) {
	digits = make([]int, len(s))
	for i := range s {
		digits[i] = int(s[i] - '0')
	}
	return
}

func fft(digitsIn []int) (digitsOut []int) {
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

func part1(input string) {
	digits := toDigits(input)
	for i := 0; i < 100; i++ {
		digits = fft(digits)
	}
	fmt.Printf("After %3d phases of FFT: %v\n", 100, digits[:8])
}

func main() {
	signal, err := ioutil.ReadFile("input.txt")
	if err != nil {
		panic(err)
	}
	part1(string(signal))
}
