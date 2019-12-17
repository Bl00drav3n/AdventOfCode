package main

import (
	"AdventOfCode/icpu"
	"fmt"
	"strconv"
	"strings"
)

const (
	Open     = 0
	Scaffold = 1
)

const (
	North = 0
	East  = 1
	South = 2
	West  = 3
)

func turn(dir int, b byte) int {
	switch b {
	case 'L':
		return (dir + 3) % 4
	case 'R':
		return (dir + 1) % 4
	}
	panic("Invalid turn!")
}

type field struct {
	data   []int
	width  int
	height int
}

func (f *field) get(x, y int) int {
	return f.data[y*f.width+x]
}

func (f *field) set(value, x, y int) {
	f.data[y*f.width+x] = value
}

func (f *field) step(x, y *int, dir int) bool {
	nextX, nextY := *x, *y
	switch dir {
	case North:
		nextY--
	case South:
		nextY++
	case West:
		nextX--
	case East:
		nextX++
	}
	if nextX >= 0 && nextX < f.width && nextY >= 0 && nextY < f.height {
		if f.get(nextX, nextY) == Scaffold {
			*x = nextX
			*y = nextY
			return true
		}
	}
	return false
}

func walk(builder *strings.Builder, f *field, x, y *int, facing int) {
	rotations := []byte{'L', 'R'}
	for i := 0; i < 2; i++ {
		steps := 0
		newDir := turn(facing, rotations[i])
		for f.step(x, y, newDir) {
			steps++
		}
		if steps > 0 {
			if builder.Len() > 0 {
				builder.WriteByte(',')
			}
			builder.WriteByte(rotations[i])
			builder.WriteByte(',')
			builder.WriteString(strconv.Itoa(steps))
			walk(builder, f, x, y, newDir)
			break
		}
	}
}

func patch(code []int) []int {
	code[0] = 2
	return code
}

func waitForInput(iCPU *icpu.IntComputer) {
	for {
		select {
		case <-icpu.RequestedInput(iCPU):
			return
		}
	}
}

func waitForPrompt(iCPU *icpu.IntComputer) {
	var builder strings.Builder
	for {
		b := byte(<-icpu.Receive(iCPU))
		builder.WriteByte(b)
		if b == '\n' {
			fmt.Print(builder.String())
			return
		}
	}
}

func sendASCII(iCPU *icpu.IntComputer, s string) {
	for _, b := range s {
		waitForInput(iCPU)
		icpu.Send(iCPU, int(b))
	}
	waitForInput(iCPU)
	icpu.Send(iCPU, 10)
}

func main() {
	// NOTE: This puzzle was awful, so the whole code is a mess and I won't clean it up.

	// NOTE: Part1
	var builder strings.Builder
	var px, py, x, y, width, height int
	code := icpu.ReadProgram("input.txt")
	iCPU := icpu.LoadProgram(patch(code), 10000)
	go icpu.Run(iCPU)
	var lastWritten byte
loop:
	for {
		select {
		case <-icpu.Halted(iCPU):
			break loop
		case recv := <-icpu.Receive(iCPU):
			b := byte(recv)
			switch b {
			case '\n':
				if x > width {
					width = x
				}
				x = 0
				y++
				if lastWritten == '\n' {
					break loop
				}
			case '^', '>', '<', 'v':
				px, py = x, y
				x++
			default:
				x++
			}
			builder.WriteByte(b)
			lastWritten = b
		}
	}
	height = y - 1
	str := builder.String()
	fmt.Print(str)

	fmt.Println()
	f := field{
		data:   make([]int, width*height),
		width:  width,
		height: height}
	for y = 0; y < height; y++ {
		for x = 0; x < width; x++ {
			value := Open
			switch str[y*(width+1)+x] {
			case '^', '>', '<', 'v', '#':
				value = Scaffold
			}
			f.set(value, x, y)
		}
	}

	var sum int
	kernel := [5][2]int{{0, -1}, {-1, 0}, {0, 0}, {1, 0}, {0, 1}}
	for y = 1; y < height-1; y++ {
		for x = 1; x < width-1; x++ {
			isIntersection := true
			for _, k := range kernel {
				if f.get(x+k[0], y+k[1]) != Scaffold {
					isIntersection = false
				}
			}
			if isIntersection {
				sum += x * y
			}
		}
	}
	fmt.Printf("The sum of the alignment parameters is %d.\n", sum)

	// NOTE: Part2
	builder.Reset()
	walk(&builder, &f, &px, &py, North)
	path := builder.String()
	fmt.Println("Final path:", path)
	// NOTE: Hardcoded functions found by inspection for my puzzle input, can't be arsed.
	functions := [3]string{"L,8,R,12,R,12,R,10", "R,10,R,12,R,10", "L,10,R,10,L,6"}
	fmap := [3]string{"A", "B", "C"}
	for i := 0; i < 3; i++ {
		fmt.Println("Function", fmap[i], functions[i])
		path = strings.ReplaceAll(path, functions[i], fmap[i])
	}
	fmt.Println("Main routine:", path)

	// NOTE: This whole part should probably be rewritten, but it grew on a foundation of guesswork and works for this input, so whatever.
	waitForPrompt(iCPU)
	sendASCII(iCPU, path)
	for _, fnc := range functions {
		waitForPrompt(iCPU)
		sendASCII(iCPU, fnc)
	}
	waitForPrompt(iCPU)
	sendASCII(iCPU, "n")
	var dust int
	for {
		select {
		case recv := <-icpu.Receive(iCPU):
			dust = recv
		case <-icpu.Halted(iCPU):
			fmt.Printf("The vacuum robot has collected an amount of %d dust.\n", dust)
			return
		}
	}
}
