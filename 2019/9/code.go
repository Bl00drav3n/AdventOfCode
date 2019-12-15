package main

import (
	"AdventOfCode/icpu"
	"fmt"
)

func runBOOST(input int) {
	program := icpu.ReadProgram("input.txt")
	iCPU := icpu.LoadProgram(program, 1000)
	go icpu.Run(iCPU)
	<-icpu.RequestedInput(iCPU)
	icpu.Send(iCPU, input)
	output := <-icpu.Receive(iCPU)
	fmt.Printf("Diagonstic code for input %d: %d\n", input, output)
	<-icpu.Halted(iCPU)
}

func main() {
	runBOOST(1)
	runBOOST(2)
}
