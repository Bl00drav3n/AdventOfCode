package main

import (
	"AdventOfCode/icpu"
	"fmt"
	"strings"
)

func waitForInput(iCPU *icpu.IntComputer) {
	for {
		select {
		case <-icpu.RequestedInput(iCPU):
			return
		}
	}
}

func waitForPrompt(iCPU *icpu.IntComputer) string {
	var builder strings.Builder
	for {
		b := byte(<-icpu.Receive(iCPU))
		if b == '\n' {
			return builder.String()
		}
		builder.WriteByte(b)
	}
}

func send(iCPU *icpu.IntComputer, value int) {
	waitForInput(iCPU)
	icpu.Send(iCPU, value)
}

func sendASCII(iCPU *icpu.IntComputer, s string) {
	for _, b := range s {
		send(iCPU, int(b))
	}
	send(iCPU, '\n')
	fmt.Println(s)
}

func robot(cmdBuffer []string, extendedMode bool) {
	code := icpu.ReadProgram("input.txt")
	iCPU := icpu.LoadProgram(code, 1000)
	go icpu.Run(iCPU)
	prompt := waitForPrompt(iCPU)
	fmt.Println(prompt)
	for _, cmd := range cmdBuffer {
		sendASCII(iCPU, cmd)
	}
	if !extendedMode {
		sendASCII(iCPU, "WALK")
	} else {
		sendASCII(iCPU, "RUN")
	}
	for {
		select {
		case recv := <-icpu.Receive(iCPU):
			if recv > 0xff {
				fmt.Println("Amount of hull damage:", recv)
			} else {
				fmt.Printf("%c", byte(recv))
			}
		case <-icpu.Halted(iCPU):
			fmt.Println("Halted.")
			return
		}
	}
}

func part1() {
	// NOTE: found through trial and error
	cmdBuffer := []string{
		// ##.x
		"NOT C J",
		"AND A J",
		"AND B J",

		// ...x
		"OR  A T",
		"OR  B T",
		"OR  C T",
		"NOT T T",
		"OR  T J",

		// .xxx
		"NOT A T",
		"OR  T J",

		// #..x
		"NOT B T",
		"OR  T J",
		
		// xxx#
		"AND D J",
	}
	robot(cmdBuffer, false)
}

func part2() {
	cmdBuffer := []string{
		// ##.#
		"NOT C J",
		"AND A J",
		"AND B J",
		"AND H J",

		// ...#
		"NOT A T",
		"OR T J",

		// #..#
		"NOT B T",
		"AND A T",
		"OR T J",

		"AND D J",
	}
	robot(cmdBuffer, true)
}

func main() {
	part1()
	part2()
}
