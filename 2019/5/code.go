package main

import (
	"fmt"
	"io"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
)

type registers struct {
	modes [3]int
	r     [3]int
	pc    int
}

type intComputer struct {
	reg    registers
	mem    []int
	halted bool
	input  []int
	output []int
}

type instruction struct {
	op int
}

func fetch(c *intComputer) int {
	result := c.mem[c.reg.pc]
	c.reg.pc++
	return result
}

var opParamMap = [100]int{
//  0  1  2  3  4  5  6  7  8  9  
	0, 3, 3, 1, 1, 2, 2, 3, 3, 0, // 0
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 1
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 2
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 3
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 4
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 5
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 6
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 7
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 8
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 9
}

func fetchInstructionInputs(c *intComputer, op int) {
	// TODO: ensure we are not going out of bounds!
	for i := 0; i < opParamMap[op]; i++ {
		c.reg.r[i] = fetch(c)
	}
}

func getInput(c *intComputer) int {
	var value int
	value, c.input = c.input[0], c.input[1:]
	return value
}

func store(c *intComputer, addr, value int) {
	c.mem[addr] = value
}

func load(c *intComputer, addr int) int {
	return c.mem[addr]
}

func loadParam(c *intComputer, n int) int {
	switch c.reg.modes[n] {
	case 0:
		return load(c, c.reg.r[n])
	case 1:
		return c.reg.r[n]
	default:
		panic("Invalid mode")
	}
}

func insAdd(c *intComputer) {
	a := loadParam(c, 0)
	b := loadParam(c, 1)
	store(c, c.reg.r[2], a+b)
}

func insMul(c *intComputer) {
	a := loadParam(c, 0)
	b := loadParam(c, 1)
	store(c, c.reg.r[2], a*b)
}

func insInput(c *intComputer) {
	value := getInput(c)
	addr := c.reg.r[0]
	store(c, addr, value)
}

func insOutput(c *intComputer) {
	value := loadParam(c, 0)
	c.output = append(c.output, value)
	fmt.Printf("Output: %d\n", value)
}

func insCondJump(c *intComputer, jumpIfTrue bool) {
	a := loadParam(c, 0)
	if (jumpIfTrue && a != 0) || (!jumpIfTrue  && a == 0) {
		c.reg.pc = loadParam(c, 1)
	}
}

func insCompare(c *intComputer, cmp func(int, int) bool) {
	a := loadParam(c, 0)
	b := loadParam(c, 1)
	value := 0
	if cmp(a, b) {
		value = 1
	}
	store(c, c.reg.r[2], value)
}

func insHalt(c *intComputer) {
	c.halted = true
}

func decodeModes(c *intComputer, code int) {
	for i := 0; i < len(c.reg.r); i++ {
		c.reg.modes[i] = code % 10
		code /= 10
	}
}

func decode(c *intComputer, opcode int) instruction {
	op := opcode % 100
	decodeModes(c, opcode/100)
	fetchInstructionInputs(c, op)
	return instruction{op}
}

func exec(c *intComputer, ins instruction) {
	switch ins.op {
	case 1:
		insAdd(c)
	case 2:
		insMul(c)
	case 3:
		insInput(c)
	case 4:
		insOutput(c)
	case 5:
		insCondJump(c, true)
	case 6:
		insCondJump(c, false)
	case 7:
		insCompare(c, func(a, b int) bool { return a < b })
	case 8:
		insCompare(c, func(a, b int) bool { return a == b })
	case 99:
		insHalt(c)
	default:
		fmt.Println(c.mem)
		panic(fmt.Errorf("Invalid opcode %d", ins.op))
	}
}

func run(c *intComputer) {
	for c.halted = false; c.halted == false; {
		opcode := fetch(c)
		ins := decode(c, opcode)
		exec(c, ins)
	}
}

func runProgram(Intcode []int, inputs []int) {
	c := intComputer{registers{}, Intcode, false, inputs, []int{}}
	run(&c)
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

func readProgram() []int {
	f, err := os.Open("input.txt")
	if err != nil {
		panic(err)
	}
	return readIntcode(f, ",")
}

func runTEST(input int) {
	fmt.Printf("Running TEST[%d]\n", input)
	runProgram(readProgram(), []int{input})
	fmt.Println("Progam halted.\n")
}

func debug() {
	for i := 0; i < 16; i++ {
		r := strings.NewReader("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99")
		fmt.Printf("Testing %d:\n", i)
		runProgram(readIntcode(r, ","), []int{i})
		fmt.Println("Progam halted.\n")
	}
}

func main() {
	//debug()
	runTEST(1)
	runTEST(5)
}
