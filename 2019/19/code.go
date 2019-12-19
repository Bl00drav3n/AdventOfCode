package main

import (
	"fmt"
	"AdventOfCode/icpu"
)

func getStatus(iCPU *icpu.IntComputer, x, y int) int {
	<-icpu.RequestedInput(iCPU)
	icpu.Send(iCPU, x)
	<-icpu.RequestedInput(iCPU)
	icpu.Send(iCPU, y)
	return <-icpu.Receive(iCPU)
}

func part1() {
	var total int
	field := [50][50]int{}
	code := icpu.ReadProgram("input.txt")
	for y := range field {
		for x := range field[y] {
			iCPU := icpu.LoadProgram(code, 1000)
			go icpu.Run(iCPU)
			recv := getStatus(iCPU, x, y)
			field[y][x] = recv
			total += recv
			switch recv {
			case 0:
				fmt.Print(".")
			case 1:
				fmt.Print("#")
			}
		}
		fmt.Println()
	}
	fmt.Println("Amount of affected points:", total)
}

func part2() {
	code := icpu.ReadProgram("input.txt")
	var startX int
	cache := [2000][2]int{}
	for y := 0; y < len(cache); y++ {
		var runStarted bool
		var interval int
		for x := startX; x < 1000; x++ {
			iCPU := icpu.LoadProgram(code, 1000)
			go icpu.Run(iCPU)
			recv := getStatus(iCPU, x, y)
			if !runStarted && recv > 0 {
				startX = x
				runStarted = true
			} else if runStarted && recv == 0 {
				interval = x - startX
				break
			}
			
		}
		cache[y][0] = startX
		cache[y][1] = interval
	}
	boxSize := 100
	for row := range cache {
		y := row - boxSize + 1
		if y >= 0 {
			x := cache[y][0] + cache[y][1] - boxSize
			if x == cache[row][0] {
				fmt.Println("Answer:", x * 10000 + y)
				break
			}
		}
	}
}

func main() {
	part1()
	part2()
}