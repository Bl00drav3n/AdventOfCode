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
	for ;; {
		select {
		case out := <-icpu.Receive(iCPU):
			fmt.Println(out)
		case <-icpu.Halted(iCPU):
			return
		}
	}
}

func main() {
	runBOOST(1)
	runBOOST(2)
}