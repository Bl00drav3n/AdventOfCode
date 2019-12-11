package main

const SINT32_MAX int = 0x7fffffff

type Point struct {
	x int
	y int
}

func getDistance(a, b Point) int {
	return Abs(a.x-b.x) + Abs(a.y-b.y)
}

func Min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func Abs(v int) int {
	if v < 0 {
		return -v
	}
	return v
}
