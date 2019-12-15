package main

import (
	"AdventOfCode/icpu"
	"fmt"
	"time"
	"github.com/golang-collections/collections/stack"
)

const (
	Unexplored rune = ' '
	Start      rune = 'S'
	Free       rune = '.'
	Wall       rune = '#'
	Drone      rune = 'D'
	Oxygen     rune = 'O'
)

const (
	HitWall     int = 0
	Moved       int = 1
	FoundOxySys int = 2
)

func move(x, y, dir int) (newX, newY int) {
	switch dir {
	case 1:
		y--
	case 2:
		y++
	case 3:
		x--
	case 4:
		x++
	default:
		panic("Invalid move!")
	}
	return x, y
}

type State struct {
	iCPU    *icpu.IntComputer
	path    *stack.Stack
	visited [][]bool
	field   [][]rune
	width   int
	height  int
	steps   int

	oxyX    int
	oxyY    int
	oxySteps int
}

func draw(field [][]rune) {
	for _, line := range field {
		fmt.Println(string(line))
	}
}

func drawState(s *State, x, y int) {
	s.field[y][x] = Drone
	draw(s.field)
	s.field[y][x] = Free
	time.Sleep(100 * time.Millisecond)
}

func sendMove(iCPU *icpu.IntComputer, dir int) {
	<-icpu.RequestedInput(iCPU)
	icpu.Send(iCPU, dir)
}

func explore(s *State, x, y int) {
	s.steps++
	s.field[y][x] = Free
	s.visited[y][x] = true
	//drawState(s, x, y)
	for dir := 1; dir <= 4; dir++ {
		newX, newY := move(x, y, dir)
		if newX < 0 || newX >= s.width || newY < 0 || newY >= s.height {
			panic("Out of range!")
		}
		if !s.visited[newY][newX] {
			sendMove(s.iCPU, dir)
			switch <-icpu.Receive(s.iCPU) {
			case HitWall:
				s.field[newY][newX] = Wall
			case FoundOxySys:
				s.oxyX = newX
				s.oxyY = newY
				s.oxySteps = s.steps
				fallthrough
			case Moved:
				explore(s, newX, newY)
				sendMove(s.iCPU, []int{0, 2, 1, 4, 3}[dir])
				s.steps--
				if <-icpu.Receive(s.iCPU) == HitWall {
					panic("Invalid move!")
				}
				//drawState(s, x, y)
			}
		}
	}
}

func NewState(iCPU *icpu.IntComputer, width, height int) (st *State) {
	visited := make([][]bool, height)
	for i := range visited {
		visited[i] = make([]bool, width)
	}
	field := make([][]rune, height)
	for i := range field {
		field[i] = make([]rune, width)
		for j := range field[i] {
			field[i][j] = Unexplored
		}
	}

	s := State{
		iCPU:    iCPU,
		width:   width,
		height:  height,
		visited: visited,
		field:   field,
		path:    stack.New(),
		oxyX:    -1,
		oxyY:    -1}
	return &s
}

func findLongestPath(s *State, x, y int) (len int) {
	moves := [4][2]int{
		{ x + 1, y    },
		{ x    , y + 1},
		{ x - 1, y    },
		{ x    , y - 1}}
	len = 0
	maxSubLen := 0
	for _, move := range moves {
		if s.field[move[1]][move[0]] == Free && !s.visited[move[1]][move[0]] {
			s.field[move[1]][move[0]] = Oxygen
			s.visited[move[1]][move[0]] = true
			subLen := findLongestPath(s, move[0], move[1]) + 1
			if subLen > maxSubLen {
				maxSubLen = subLen
			}
		}
	}
	return len + maxSubLen
}

func part1(s *State) {
	go icpu.Run(s.iCPU)
	startX, startY := s.width/2, s.height/2
	start := time.Now()
	explore(s, startX, startY)
	delta := time.Since(start)
	s.field[s.oxyY][s.oxyX] = Oxygen
	s.field[startY][startX] = Start
	draw(s.field)
	s.field[startY][startX] = Free
	fmt.Printf("It took the drone %d steps to reach the oxygen system.\n", s.oxySteps)
	fmt.Println(delta)
}

func part2(s *State) {
	for j := range s.visited {
		for i := range s.visited[j] {
			s.visited[j][i] = false
		}
	}
	s.visited[s.oxyY][s.oxyX] = true
	totalTime := findLongestPath(s, s.oxyX, s.oxyY)
	fmt.Printf("It will take %d minutes to fill the area with oxygen.\n", totalTime)
}

func main() {
	width, height := 42, 42
	intCode := icpu.ReadProgram("input.txt")
	iCPU := icpu.LoadProgram(intCode, 1000)
	s := NewState(iCPU, width, height)
	part1(s)
	part2(s)
}
