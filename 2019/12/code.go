package main

import (
	"fmt"
	"time"
)

type vec3i [3]int

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func gravity(a, b int) int {
	if a < b {
		return 1
	}
	if a == b {
		return 0
	}
	return -1
}

func step(moons []vec3i, vel []vec3i, moonCount int) {
	for i := 0; i < moonCount; i++ {
		for j := i + 1; j < moonCount; j++ {
			for e := 0; e < 3; e++ {
				g := gravity(moons[i][e], moons[j][e])
				vel[i][e] += g
				vel[j][e] -= g
			}
		}
	}
	for i := 0; i < moonCount; i++ {
		for e := 0; e < 3; e++ {
			moons[i][e] += vel[i][e]
		}
	}
}

func energy(moons []vec3i, vel []vec3i, moonCount int) int {
	var totalEnergy int
	for i := 0; i < moonCount; i++ {
		var pot, kin int
		for e := 0; e < 3; e++ {
			pot += abs(moons[i][e])
			kin += abs(vel[i][e])
		}
		totalEnergy += pot * kin
	}
	return totalEnergy
}

func compare(a, av, b, bv []vec3i, i, count int) bool {
	for j := 0; j < count; j++ {
		if !(a[j][i] == b[j][i] && av[j][i] == bv[j][i]) {
			return false
		}
	}
	return true
}

func gcd(a, b int) int {
	for b != 0 {
		t := b
		b = a % b
		a = t
	}
	return a
}

func lcm(a, b int) int {
	return a * b / gcd(a, b)
}

func part1(moonsInit, velInit []vec3i) {
	moonCount := len(moonsInit)
	moons := make([]vec3i, moonCount)
	vel := make([]vec3i, moonCount)
	copy(moons, moonsInit)
	copy(vel, velInit)
	for n := 0; n < 1000; n++ {
		step(moons, vel, moonCount)
		if (n + 1) % 10 == 0 {
			fmt.Printf("Total energy after %d steps: %d\n", n + 1, energy(moons, vel, moonCount))
		}
	}
}

func part2(moonsInit, velInit []vec3i) {
	var countX, countY, countZ int
	moonCount := len(moonsInit)
	moons := make([]vec3i, moonCount)
	vel := make([]vec3i, moonCount)
	copy(moons, moonsInit)
	copy(vel, velInit)
	start := time.Now()
	// NOTE: We can just look for each dimension to wrap individually, because they are not coupled.
	// NOTE: The total wrap around occurs at the least common multiple of x,y,z
	for count := 0;; count++{
		step(moons, vel, moonCount)
		if countX == 0 {
			if compare(moons, vel, moonsInit, velInit, 0, moonCount) {
				countX = count + 1
			}
		}
		if countY == 0 {
			if compare(moons, vel, moonsInit, velInit, 1, moonCount) {
				countY = count + 1
			}
		}
		if countZ == 0 {
			if compare(moons, vel, moonsInit, velInit, 2, moonCount) {
				countZ = count + 1
			}
		}
		if countX > 0 && countY > 0 && countZ > 0 {
			break
		}
	}
	dt := time.Since(start)
	fmt.Printf("Will return to initial state after %d steps\n", lcm(lcm(countX, countY), countZ))
	fmt.Println(dt)
}

func main() {
	//moonsInit := []vec3i{{-1, 0, 2},{2, -10, -7},{4, -8, 8},{3, 5, -1}}
	//moonsInit := []vec3i{{-8,-10,0},{5,5,10},{2,-7,3},{9,-8,-3}}
	moonsInit := []vec3i{{1, -4, 3}, {-14, 9, -4}, {-4, -6, 7}, {6, -9, -11}}
	velInit := make([]vec3i, len(moonsInit))
	part1(moonsInit, velInit)
	part2(moonsInit, velInit)
}
