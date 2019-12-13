package main

import (
	"AdventOfCode/icpu"
	"fmt"
	"time"
)

func patch(intCode []int) []int {
	intCode[0] = 2
	return intCode
}

func getInput(barX, ballX int) int {
	if barX < ballX {
		return 1
	} else if barX > ballX {
		return -1
	}
	return 0
}

func main() {
	field := [21][44]rune{}
	for _, row := range field {
		for i := range row {
			row[i] = ' '
		}
	}
	intCode := patch(icpu.ReadProgram("input.txt"))
	iCPU := icpu.LoadProgram(intCode, 1000)
	var outIdx int
	var outBuf [3]int
	var score int
	ballX := -1
	barX := -1
	timeStep := 200
	go icpu.Run(iCPU)
loop:
	for {
		if outIdx == 3 {
			outIdx = 0
			x, y, id := outBuf[0], outBuf[1], outBuf[2]
			if x == -1 && y == 0 {
				score = id
			} else {
				if x >= 0 && x < 44 && y >= 0 && y < 21 {
					b := ' '
					switch id {
					case 1:
						b = '|'
					case 2:
						b = 'x'
					case 3:
						b = '_'
						barX = x
					case 4:
						b = 'o'
						ballX = x
					}
					field[y][x] = b
				}
			}
		}
		select {
		case <-icpu.RequestedInput(iCPU):
			input := getInput(barX, ballX)
			icpu.Send(iCPU, input)
			for i := 0; i < 21; i++ {
				fmt.Printf("%s\n", string(field[i][:]))
			}
			fmt.Printf("Score: %d\n", score)
			time.Sleep(time.Duration(timeStep) * time.Millisecond)
		case recv := <-icpu.Receive(iCPU):
			outBuf[outIdx] = recv
			outIdx++
		case <-icpu.Halted(iCPU):
			break loop
		default:
		}
	}
	fmt.Printf("Final score: %d\n", score)
}
