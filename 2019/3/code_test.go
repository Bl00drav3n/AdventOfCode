package main

import (
	"fmt"
	"testing"
)

var findClosestIntersectionDistanceCases = []struct {
	name     string
	wire1    string
	wire2    string
	expected int
}{
	{
		wire1:    "R8,U5,L5,D3",
		wire2:    "U7,R6,D4,L4",
		expected: 6,
	},
	{
		wire1:    "R75,D30,R83,U83,L12,D49,R71,U7,L72",
		wire2:    "U62,R66,U55,R34,D71,R55,D58,R83",
		expected: 159,
	},
	{
		wire1:    "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
		wire2:    "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
		expected: 135,
	},
}

var findShortestPathCases = []struct {
	name     string
	wire1    string
	wire2    string
	expected int
}{
	{
		wire1:    "R8,U5,L5,D3",
		wire2:    "U7,R6,D4,L4",
		expected: 30,
	},
	{
		wire1:    "R75,D30,R83,U83,L12,D49,R71,U7,L72",
		wire2:    "U62,R66,U55,R34,D71,R55,D58,R83",
		expected: 610,
	},
	{
		wire1:    "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
		wire2:    "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
		expected: 410,
	},
}

func TestNaive_findClosestIntersectionDistance(t *testing.T) {
	for i, c := range findClosestIntersectionDistanceCases {
		t.Run(fmt.Sprintf("test %d", i), func(t *testing.T) {
			if findClosestIntersectionDistance(parseNaive(c.wire1), parseNaive(c.wire2)) != c.expected {
				t.Error("did not match")
			}
		})
	}
}

func TestNaive_findShortestPathNaive(t *testing.T) {
	for i, c := range findShortestPathCases {
		t.Run(fmt.Sprintf("test %d", i), func(t *testing.T) {
			if findShortestPathNaive(parseNaive(c.wire1), parseNaive(c.wire2)) != c.expected {
				t.Error("did not match")
			}
		})
	}
}

func Test_findClosestIntersectionDistance(t *testing.T) {
	for i, c := range findClosestIntersectionDistanceCases {
		t.Run(fmt.Sprintf("test %d", i), func(t *testing.T) {
			if findClosestIntersection(parse(c.wire1), parse(c.wire2)) != c.expected {
				t.Error("did not match")
			}
		})
	}
}

func Test_c(t *testing.T) {
	for i, c := range findShortestPathCases {
		t.Run(fmt.Sprintf("test %d", i), func(t *testing.T) {
			if findShortestPath(parse(c.wire1), parse(c.wire2)) != c.expected {
				t.Error("did not match")
			}
		})
	}
}

func Benchmark3(b *testing.B) {
	// run the Fib function b.N times
	for n := 0; n < b.N; n++ {
		findClosestIntersection(parse(findClosestIntersectionDistanceCases[0].wire1), parse(findClosestIntersectionDistanceCases[0].wire2))
		findShortestPath(parse(findShortestPathCases[0].wire1), parse(findShortestPathCases[0].wire2))
	}
}

func Benchmark3Naive(b *testing.B) {
	// run the Fib function b.N times
	for n := 0; n < b.N; n++ {
		findClosestIntersectionDistance(parseNaive(findClosestIntersectionDistanceCases[0].wire1), parseNaive(findClosestIntersectionDistanceCases[0].wire2))
		findShortestPathNaive(parseNaive(findShortestPathCases[0].wire1), parseNaive(findShortestPathCases[0].wire2))
	}
}
