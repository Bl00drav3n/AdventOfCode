package main

import (
	"fmt"
	"github.com/Bl00drav3n/AdventOfCode/2019/icpu"
)

func runBOOST(input int) {
	program := icpu.ReadProgram("input.txt")
	iCPU := icpu.LoadProgram(program, 1000)
	go icpu.Run(iCPU)
	icpu.Send(iCPU, input)
	for !icpu.Halted(iCPU) {
		output := icpu.Receive(iCPU)
		fmt.Printf("Diagonstic code for input %d: %d\n", input, output)
	}
}

func main() {
	runBOOST(1)
	runBOOST(2)
}
