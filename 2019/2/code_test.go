package main

import (
	"fmt"
	"strings"
	"testing"
)

func TestCode(t *testing.T) {
	tests := []string{
		"1,9,10,3,2,3,11,0,99,30,40,50",
		"1,0,0,0,99",
		"2,3,0,3,99",
		"2,4,4,5,99,0",
		"1,1,1,4,99,5,6,0,99"}
	for i, test := range tests {
		t.Run(fmt.Sprintf("test %d", i), func(t *testing.T) {
			f := strings.NewReader(test)
			ints := readIntcode(f, ",")
			runProgram(ints)
			fmt.Println(ints) // assert
		})
	}
}
