package main

import (
	"fmt"
	"github.com/Bl00drav3n/AdventOfCode/2019/icpu"
	"image"
	"image/color"
	"image/png"
	"os"
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

func genImage(panelColor []int, width, xmin, ymin, xmax, ymax int) *image.RGBA {
	img := image.NewRGBA(image.Rectangle{image.Point{0, 0}, image.Point{xmax - xmin + 1, ymax - ymin + 1}})
	black := color.RGBA{0x00, 0x00, 0x00, 0xff}
	white := color.RGBA{0xff, 0xff, 0xff, 0xff}
	for y := ymin; y <= ymax; y++ {
		for x := xmin; x <= xmax; x++ {
			c := black
			if panelColor[y * width + x] > 0 {
				c = white
			}
			img.Set(x - xmin, y - ymin, c)
		}
	}
	return img
}

func robot(startingColor int) *image.RGBA {
	program := icpu.ReadProgram("input.txt")
	iCPU := icpu.LoadProgram(program, 1000)
	go icpu.Run(iCPU)
	directions := [][]int{{0, -1}, {1, 0}, {0, 1}, {-1, 0}}
	direction := 0
	width, height := 200, 200
	x, y := width/2, height/2
	xmin, ymin, xmax, ymax := 0x7fffffff, 0x7fffffff, 0, 0
	panelColor := make([]int, width*height)
	panelVisits := make([]bool, width*height)
	panelColor[y*width+x] = startingColor
	for !icpu.Halted(iCPU) {
		idx := y*width + x
		icpu.Send(iCPU, panelColor[idx])
		recvdColor := icpu.Receive(iCPU)
		turn := icpu.Receive(iCPU)
		switch turn {
		case 0:
			direction = direction + len(directions) - 1
		case 1:
			direction++
		}
		direction = direction % len(directions)
		panelColor[idx] = recvdColor
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
	return genImage(panelColor, width, xmin, ymin, xmax, ymax)
}

func calculate(initialColor int, filename string) {
	f, _ := os.Create(filename)
	png.Encode(f, robot(initialColor))
}

func main() {
	calculate(0, "part1.png")
	calculate(1, "part2.png")
}
