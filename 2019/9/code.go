package main

import (
	"fmt"
	"AdventOfCode/icpu"
)

func runBOOST(input int) {
	program := icpu.ReadProgram("input.txt")
	iCPU := icpu.LoadProgram(program, 1000)
	go icpu.Run(iCPU)
	icpu.Send(iCPU, input)
	for !icpu.Halted(iCPU) {
		output := <-icpu.Receive(iCPU)
		fmt.Printf("Diagonstic code for input %d: %d\n", input, output)
	}
}

func main() {
	runBOOST(1)
	runBOOST(2)
}