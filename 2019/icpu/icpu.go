package icpu

import (
	"fmt"
	"io"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
)

type IntComputer struct {
	reg struct {
		modes [3]int
		r     [3]int
		x     int
		pc    int
	}
	mem    []int
	prog   []int
	halted bool

	sigInput  chan int
	sigOutput chan int
}

func ReadIntcode(r io.Reader, sep string) []int {
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

func ReadProgram(filename string) []int {
	f, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	return ReadIntcode(f, ",")
}

func LoadProgram(intCode []int, memsize int) *IntComputer {
	var c IntComputer
	c.prog = intCode
	c.mem = make([]int, memsize+len(intCode))
	c.sigInput = make(chan int, 1)
	c.sigOutput = make(chan int, 1)
	copy(c.mem, intCode)
	return &c
}

func Send(iCPU *IntComputer, value int) {
	iCPU.sigInput <- value
}

func Receive(iCPU *IntComputer) int {
	return <-iCPU.sigOutput
}

func Halted(iCPU *IntComputer) bool {
	return iCPU.halted
}

func Run(c *IntComputer) {
	for c.halted = false; c.halted == false; {
		opcode := fetch(c)
		ins := decode(c, opcode)
		exec(c, ins)
	}
}

type instruction struct {
	op int
}

func fetch(c *IntComputer) int {
	result := load(c, c.reg.pc)
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

func fetchInstructionInputs(c *IntComputer, op int) {
	// TODO: ensure we are not going out of bounds!
	for i := 0; i < opParamMap[op]; i++ {
		c.reg.r[i] = fetch(c)
	}
}

func store(c *IntComputer, addr, value int) {
	c.mem[addr] = value
}

func load(c *IntComputer, addr int) int {
	return c.mem[addr]
}

func loadParam(c *IntComputer, n int) int {
	switch c.reg.modes[n] {
	case 0:
		return load(c, c.reg.r[n])
	case 1:
		return c.reg.r[n]
	case 2:
		return load(c, c.reg.x+c.reg.r[n])
	default:
		panic("Invalid mode")
	}
}

func getAddress(c *IntComputer, n int) int {
	if c.reg.modes[n] == 2 {
		return c.reg.x + c.reg.r[n]
	}
	return c.reg.r[n]
}

func insAdd(c *IntComputer) {
	a := loadParam(c, 0)
	b := loadParam(c, 1)
	store(c, getAddress(c, 2), a+b)
}

func insMul(c *IntComputer) {
	a := loadParam(c, 0)
	b := loadParam(c, 1)
	store(c, getAddress(c, 2), a*b)
}

func insInput(c *IntComputer) {
	value := <-c.sigInput
	addr := getAddress(c, 0)
	store(c, addr, value)
}

func insOutput(c *IntComputer) {
	c.sigOutput <- loadParam(c, 0)
}

func insCondJump(c *IntComputer, jumpIfTrue bool) {
	a := loadParam(c, 0)
	if (jumpIfTrue && a != 0) || (!jumpIfTrue && a == 0) {
		c.reg.pc = loadParam(c, 1)
	}
}

func insCompare(c *IntComputer, cmp func(int, int) bool) {
	a := loadParam(c, 0)
	b := loadParam(c, 1)
	value := 0
	if cmp(a, b) {
		value = 1
	}
	store(c, getAddress(c, 2), value)
}

func insRelBase(c *IntComputer) {
	c.reg.x += loadParam(c, 0)
}

func insHalt(c *IntComputer) {
	c.halted = true
}

func decodeModes(c *IntComputer, code int) {
	for i := 0; i < len(c.reg.r); i++ {
		c.reg.modes[i] = code % 10
		code /= 10
	}
}

func decode(c *IntComputer, opcode int) instruction {
	op := opcode % 100
	decodeModes(c, opcode/100)
	fetchInstructionInputs(c, op)
	return instruction{op}
}

func exec(c *IntComputer, ins instruction) {
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
