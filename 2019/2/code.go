package main

import (
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"os"
	"strconv"
	"strings"
)

type IntComputer struct {
	pc     int
	mem    []int
	halted bool
}

func exec(c *IntComputer) {
	switch c.mem[c.pc] {
	case 1:
		c.mem[c.mem[c.pc+3]] = c.mem[c.mem[c.pc+1]] + c.mem[c.mem[c.pc+2]]
	case 2:
		c.mem[c.mem[c.pc+3]] = c.mem[c.mem[c.pc+1]] * c.mem[c.mem[c.pc+2]]
	case 99:
		c.halted = true
	default:
		fmt.Println(c.mem)
		log.Fatalf("Invalid opcode %d at (%d)", c.mem[c.pc], c.pc)
	}
}

func run(c *IntComputer) {
	for c.halted = false; c.halted == false; c.pc += 4 {
		exec(c)
	}
}

func readIntcode(r io.Reader, sep string) []int {
	b, err := ioutil.ReadAll(r)
	if err != nil {
		panic(err)
	}
	strs := strings.Split(string(b), sep)
	ints := make([]int, len(strs))
	for i, str := range strs {
		ints[i], err = strconv.Atoi(str)
		if err != nil {
			panic(err)
		}
	}
	return ints
}

func runProgram(intCode []int) int {
	c := IntComputer{0, intCode, false}
	run(&c)
	return c.mem[0]
}

func patch(intCode []int, noun int, verb int) []int {
	patched := make([]int, len(intCode))
	copy(patched, intCode)
	patched[1] = noun
	patched[2] = verb
	return patched
}

func part1(program []int) {
	result := runProgram(patch(program, 12, 2))
	fmt.Printf("Part1 finished, result: %d\n", result)
}

func part2(program []int) {
	var finalResult int
	targetVal := 19690720
	for noun := 0; noun < 100; noun++ {
		for verb := 0; verb < 100; verb++ {
			result := runProgram(patch(program, noun, verb))
			if result == targetVal {
				finalResult = 100*noun + verb
				break
			}
		}
	}
	fmt.Printf("Part2 tests finished, result: %d\n.", finalResult)
}

func main() {
	f, err := os.Open("input.txt")
	if err != nil {
		panic(err)
	}
	program := readIntcode(f, ",")
	part1(program)
	part2(program)
}
