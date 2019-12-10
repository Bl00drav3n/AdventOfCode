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
  x     int
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
//0  1  2  3  4  5  6  7  8  9  
	0, 3, 3, 1, 1, 2, 2, 3, 3, 1, // 0
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
  case 2:
    return load(c, c.reg.x + c.reg.r[n])
	default:
		panic("Invalid mode")
	}
}

func getAddress(c *intComputer, n int) int {
  if c.reg.modes[n] == 2 {
    return c.reg.x + c.reg.r[n]
  }
  return c.reg.r[n]
}

func insAdd(c *intComputer) {
	a := loadParam(c, 0)
	b := loadParam(c, 1)
	store(c, getAddress(c, 2), a+b)
}

func insMul(c *intComputer) {
	a := loadParam(c, 0)
	b := loadParam(c, 1)
	store(c, getAddress(c, 2), a*b)
}

func insInput(c *intComputer) {
	value := getInput(c)
  addr := getAddress(c, 0)
	store(c, addr, value)
}

func insOutput(c *intComputer) {
	value := loadParam(c, 0)
	c.output = append(c.output, value)
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
	store(c, getAddress(c, 2), value)
}

func insRelBase(c *intComputer) {
  c.reg.x += loadParam(c, 0)
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
  case 9:
    insRelBase(c)
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

func runProgram(Intcode []int, inputs []int, memsize int) []int {
  mem := make([]int, memsize)
	c := intComputer{registers{}, append(Intcode, mem...), false, inputs, []int{}}
	run(&c)
  return c.output
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

func runBOOST(input int) {
  output := runProgram(readProgram(), []int{input}, 128)
  fmt.Println("Program halted.")
  fmt.Println(output)
}

func debug() {
  r := strings.NewReader("109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99")
  //r := strings.NewReader("1102,34915192,34915192,7,4,7,99,0")
  //r := strings.NewReader("104,1125899906842624,99")
  output := runProgram(readIntcode(r, ","), []int{}, 128)
  fmt.Println("Program halted.")
  fmt.Println(output)
}

func main() {
	//debug()
	runBOOST(1)
	runBOOST(2)
}