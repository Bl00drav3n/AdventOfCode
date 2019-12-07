package main

import (
	"fmt"
	"io/ioutil"
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
	output int
	outputAvailable bool
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
	c.output = value
	c.outputAvailable = true
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

func run(c *intComputer) int {
	for c.halted = false; c.halted == false; {
		opcode := fetch(c)
		ins := decode(c, opcode)
		exec(c, ins)
		if c.outputAvailable {
			c.outputAvailable = false
			return c.output
		}
	}
	return c.output
}

func readIntcode(program string, sep string) []int {
	strs := strings.Split(program, sep)
	ints := make([]int, len(strs))
	for i, str := range strs {
		ints[i], _ = strconv.Atoi(str)
	}
	return ints
}

func readProgram() string {
	b, err := ioutil.ReadFile("input.txt")
	if err != nil {
		panic(err)
	}
	return string(b)
}

func createComputer(program string, inputs []int) intComputer {
	return intComputer{registers{}, readIntcode(program, ","), false, inputs, 0, false}
}

func amplify(program string, phase, input int) int {
	inputs := []int{phase, input}
	c := createComputer(program, inputs)
	for ; !c.halted; {
		run(&c)
	}
	return c.output
}

// Stolen from https://stackoverflow.com/a/30230552
func nextPerm(p []int) {
    for i := len(p) - 1; i >= 0; i-- {
        if i == 0 || p[i] < len(p)-i-1 {
            p[i]++
            return
        }
        p[i] = 0
    }
}

func getPerm(orig, p []int) []int {
    result := append([]int{}, orig...)
    for i, v := range p {
        result[i], result[i+v] = result[i+v], result[i]
    }
	return result
}

func part1() {
	program := readProgram()
	max_thrust := 0
	ampPhases := []int{0, 1, 2, 3, 4}
	for p := make([]int, len(ampPhases)); p[0] < len(p); nextPerm(p) {
		phasePerm := getPerm(ampPhases, p)
		thrust := 0
		for j := 0; j < len(ampPhases); j++ {
			thrust = amplify(program, phasePerm[j], thrust)
		}
		if thrust > max_thrust {
			max_thrust = thrust
		}
	}
	fmt.Printf("Maximum thrust: %d\n", max_thrust)
}

func part2() {
	program := readProgram()
	max_thrust := 0
	ampPhases := []int{5, 6, 7, 8, 9}
	for p := make([]int, len(ampPhases)); p[0] < len(p); nextPerm(p) {
		phasePerm := getPerm(ampPhases, p)
		comps := make([]intComputer, len(ampPhases))
		for j := 0; j < len(ampPhases); j++ {
			comps[j] = createComputer(program, []int{phasePerm[j]})
		}
		thrust := 0
		for ; !comps[len(ampPhases) - 1].halted; {
			for j := 0; j < len(ampPhases); j++ {
				comps[j].input = append(comps[j].input, thrust)
				thrust = run(&comps[j])
			}
		}
		if thrust > max_thrust {
			max_thrust = thrust
		}
	}
	fmt.Printf("Maximum thrust: %d\n", max_thrust)
}

func main() {
	part1()
	part2()
}