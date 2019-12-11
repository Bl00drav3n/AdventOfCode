package main

import (
	"fmt"
	"AdventOfCode/icpu"
)

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func robot(startingColor int) {
	program := icpu.ReadProgram("input.txt")
	iCPU := icpu.LoadProgram(program, 1000)
	go icpu.Run(iCPU)
	directions := [][]int{[]int{0, -1}, []int{1, 0}, []int{0, 1}, []int{-1, 0}}
	direction := 0
	width, height := 200, 200
	x, y := width / 2, height / 2
	xmin, ymin, xmax, ymax := 0x7fffffff, 0x7fffffff, 0, 0
	panelColor := make([]int, width * height)
	panelVisits := make([]bool, width * height)
	panelColor[y * width + x] = startingColor
	for !icpu.Halted(iCPU) {
		idx := y * width + x
		icpu.Send(iCPU, panelColor[idx])
		color := <-icpu.Receive(iCPU)
		turn  := <-icpu.Receive(iCPU)
		switch turn {
		case 0:
			direction = direction + len(directions) - 1
		case 1:
			direction++
		}
		direction = direction % len(directions)
		panelColor[idx] = color
		panelVisits[idx] = true
		x += directions[direction][0]
		y += directions[direction][1]
		if x < 0 || x >= width || y < 0 || y >= height {
			panic("Robot moved outside the panel!")
		}
		xmin, ymin, xmax, ymax = min(x, xmin), min(y, ymin), max(x, xmax), max(y, ymax)
	}
	totalVisitedPanels := 0
	for _, visited := range panelVisits {
		if visited {
			totalVisitedPanels++
		}
	}
	fmt.Printf("Total panels visisted: %d\n", totalVisitedPanels)
	fmt.Printf("Panel area bounds: [(%d,%d), (%d,%d)]\n", xmin, ymin, xmax, ymax)
	buf := make([]rune, xmax - xmin + 1)
	for y = ymin; y <= ymax; y++ {
		for x = xmin; x <= xmax; x++ {
			c := '.'
			if panelColor[y * width + x] > 0 {
				c = '#'
			}
			buf[x - xmin] = c
		}
		fmt.Println(string(buf))
	}
}

func main() {
	robot(0)
	robot(1)
}