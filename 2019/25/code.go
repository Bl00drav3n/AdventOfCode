package main

import (
	"AdventOfCode/icpu"
	"bufio"
	"fmt"
	"os"
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
	send(iCPU, 10)
}

func main() {
	code := icpu.ReadProgram("input.txt")
	iCPU := icpu.LoadProgram(code, 1000)
	go icpu.Run(iCPU)
	reader := bufio.NewReader(os.Stdin)
	for {
		for {
			str := waitForPrompt(iCPU)
			fmt.Println(str)
			if str == "Command?" {
				break
			}
		}
		text, _ := reader.ReadString('\n')
		sendASCII(iCPU, strings.Trim(text, "\r\n"))

		select {
		case <-icpu.Halted(iCPU):
			fmt.Println("Halted.")
			return
		default:
		}
	}
}
