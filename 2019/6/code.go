package main

import (
	"fmt"
	"bufio"
	"strings"
	"io"
	"os"
)

type node struct {
	name   string
	parent *node
	childs []*node
	depth  int
}

func getOrbitalMap(r io.Reader) map[string][]string {
	result := map[string][]string{}
	scanner := bufio.NewScanner(r)
	for scanner.Scan() {
		orbit := strings.Split(scanner.Text(), ")")
		if result[orbit[0]] != nil {
			result[orbit[0]] = append(result[orbit[0]], orbit[1])
		} else {
			result[orbit[0]] = []string{orbit[1]}
		}
	}
	return result
}

func buildTree(m *map[string][]string, name string, parent *node, depth int) *node {
	elem := node{name: name, parent: parent, childs: []*node{}, depth: depth}
	for _, child := range (*m)[name] {
		elem.childs = append(elem.childs, buildTree(m, child, &elem, depth+1))
	}
	return &elem
}

func find(elem *node, name string) *node {
	if elem.name == name {
		return elem
	}
	for _, child := range elem.childs {
		test := find(child, name)
		if test != nil {
			return test
		}
	}
	return nil
}

func getParentOrbits(elem *node) []*node {
	parents := []*node{}
	for n := elem.parent; n != nil; n = n.parent {
		parents = append(parents, n)
	}
	return parents
}

func findClosestCommonOrbit(nodeA, nodeB *node) *node {
	var result *node
	closestDistance := 0
	pA := getParentOrbits(nodeA)
	pB := getParentOrbits(nodeB)
	for _, a := range pA {
		for _, b := range pB {
			if a.name == b.name && a.depth > closestDistance {
				result = a
				closestDistance = a.depth
			}
		}
	}
	return result
}

func countDirect(m *map[string][]string, elem string) int {
	orbits := (*m)[elem]
	childs := len(orbits)
	for _, child := range orbits {
		childs += countDirect(m, child)
	}
	return childs
}

func countAll(m *map[string][]string, elem string) int {
	sum := countDirect(m, elem)
	orbits := (*m)[elem]
	for _, child := range orbits {
		sum += countAll(m, child)
	}
	return sum
}

func orbitCountChecksum(r io.Reader) {
	orbitalMap := getOrbitalMap(r)
	fmt.Printf("Orbit count checksum: %d\n", countAll(&orbitalMap, "COM"))
}

func orbitTransfer(r io.Reader) {
	orbitalMap := getOrbitalMap(r)
	tree := buildTree(&orbitalMap, "COM", nil, 0)
	san := find(tree, "SAN")
	you := find(tree, "YOU")
	common := findClosestCommonOrbit(san, you)
	fmt.Printf("Number of orbital transfers: %d\n", (san.depth - common.depth - 1) + (you.depth - common.depth - 1))
}

func test() {
	r := strings.NewReader("COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L")
	orbitCountChecksum(r)
	
	r = strings.NewReader("COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\nK)YOU\nI)SAN\n")
	orbitTransfer(r)
}

func part1() {
	f, err := os.Open("input.txt")
	if err != nil {
		panic(err)
	}
	defer f.Close()
	orbitCountChecksum(f)
}

func part2() {
	f, err := os.Open("input.txt")
	if err != nil {
		panic(err)
	}
	defer f.Close()
	orbitTransfer(f)
}

func main() {
	//test()
	part1()
	part2()
}
