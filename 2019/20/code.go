package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type loc [2]int
type locmap map[string][]portal

type portal struct {
	enterPos loc
	exitPos  loc
}

type donut struct {
	data     [][]byte
	innerDim int
	outerDim int
	offset   int
	portals  locmap
}

func loadInput(r *bufio.Reader) donut {
	var m donut
	m.data = [][]byte{}
	scanner := bufio.NewScanner(r)
	for scanner.Scan() {
		row := []byte(scanner.Text())
		m.data = append(m.data, row)
	}
	m.offset = 2
	m.outerDim = len(m.data[0]) - 2*m.offset
	m.innerDim = (m.outerDim - 5) / 4 // TODO: Fix for other inputs!
	m.portals = locmap{}
	return m
}

func isLetter(b byte) bool {
	return b >= 'A' && b <= 'Z'
}

func getPortalID(first, second byte) string {
	var builder strings.Builder
	builder.WriteByte(first)
	builder.WriteByte(second)
	return builder.String()
}

func insertPortal(m *donut, first, second byte, enterPos, exitPos loc) {
	id := getPortalID(first, second)
	var entry []portal
	p := portal{exitPos: exitPos, enterPos: enterPos}
	if e, ok := m.portals[id]; ok {
		entry = append(e, p)
	} else {
		entry = []portal{p}
	}
	m.portals[id] = entry
}

func scanPortals(m *donut) {
	for _, j := range [2]int{0, m.outerDim - m.innerDim} {
		for i := m.offset; i < m.offset+m.outerDim; i++ {
			k := m.offset + m.innerDim
			if isLetter(m.data[i][j]) && isLetter(m.data[i][j+1]) {
				insertPortal(m, m.data[i][j], m.data[i][j+1], loc{j + 1, i}, loc{j + 2, i})
			}
			if isLetter(m.data[i][k+j]) && isLetter(m.data[i][k+j+1]) {
				insertPortal(m, m.data[i][k+j], m.data[i][k+j+1], loc{k + j, i}, loc{k + j - 1, i})
			}
			if isLetter(m.data[j][i]) && isLetter(m.data[j+1][i]) {
				insertPortal(m, m.data[j][i], m.data[j+1][i], loc{i, j + 1}, loc{i, j + 2})
			}
			if isLetter(m.data[k+j][i]) && isLetter(m.data[k+j+1][i]) {
				insertPortal(m, m.data[k+j][i], m.data[k+j+1][i], loc{i, k + j}, loc{i, k + j - 1})
			}
		}
	}
}

const (
	North = 0
	East  = 1
	South = 2
	West  = 3
)

func isWalkable(m *donut, x, y int) bool {
	return m.data[y][x] == '.'
}

func printState(m *donut, visited [][]bool, x, y, step int) {
	var builder strings.Builder
	for j := range m.data {
		for i := range m.data[j] {
			var byteToWrite byte
			if i == x && y == j {
				byteToWrite = '@'
			} else if visited[j][i] {
				byteToWrite = '*'
			} else {
				byteToWrite = m.data[j][i]
			}
			for _, plist := range m.portals {
				for _, p := range plist {
					if p.enterPos[0] == i && p.enterPos[1] == j {
						byteToWrite = 'o'
						break
					} else if p.exitPos[0] == i && p.exitPos[1] == j {
						byteToWrite = 'x'
						break
					}
				}
			}
			builder.WriteByte(byteToWrite)
		}
		builder.WriteByte('\n')
	}

	builder.WriteString("Current step: ")
	builder.WriteString(strconv.Itoa(step))
	builder.WriteByte('\n')
	fmt.Print(builder.String())
	/*
		reader := bufio.NewReader(os.Stdin)
		reader.ReadString('\n')
	*/
	//time.Sleep(1 * time.Millisecond)
}

func isWall(b byte) bool {
	return b == '#'
}

func checkPortals(m *donut) {
	for key, entry := range m.portals {
		if len(entry) == 2 && key != "AA" && key != "ZZ" {
			fmt.Println("portal", key, "ok", entry)
		} else if key == "AA" || key == "ZZ" {
			fmt.Println(" point", key, "ok", entry)
		} else {
			fmt.Println("portal", key, "failure", entry)
		}
	}
}

func getStartPosition(m *donut, id string, idx int) (x, y int) {
	p := m.portals[id][idx]
	return p.exitPos[0], p.exitPos[1]
}

type portalinfo struct {
	pathlen int
	idx     int
}

type area struct {
	from  string
	infos map[string]portalinfo
}

func getPortalIDFromEntranceLocation(m *donut, x, y int) (string, int) {
	for id, entry := range m.portals {
		for i := range entry {
			if entry[i].enterPos[0] == x && entry[i].enterPos[1] == y {
				return id, i
			}
		}
	}
	panic("Location not found!")
}

func NewArea(m *donut, from string) *area {
	a := area{}
	a.from = from
	a.infos = map[string]portalinfo{}
	return &a
}

func reachable(m *donut, a *area, visited [][]bool, x, y, step int) {
	if !isWall(m.data[y][x]) {
		if !visited[y][x] {
			//printState(m, visited, x, y, step)
			visited[y][x] = true
			if isLetter(m.data[y][x]) {
				id, idx := getPortalIDFromEntranceLocation(m, x, y)
				if id != a.from {
					a.infos[id] = portalinfo{pathlen: step, idx: idx}
				}
			} else {
				reachable(m, a, visited, x-1, y, step+1)
				reachable(m, a, visited, x+1, y, step+1)
				reachable(m, a, visited, x, y-1, step+1)
				reachable(m, a, visited, x, y+1, step+1)
			}
		}
	}
}

func traverse(m *donut, followed map[string]bool, g *Graph, fromID string, idx int) {
	followed[fromID] = true
	if fromID == "ZZ" {
		return
	}

	a := NewArea(m, fromID)
	visited := make([][]bool, len(m.data))
	for i := range m.data {
		visited[i] = make([]bool, len(m.data[i]))
	}
	startX, startY := getStartPosition(m, fromID, idx)
	reachable(m, a, visited, startX, startY, 0)
	for toID, info := range a.infos {
		g.AddEdge(fromID, toID, info.pathlen)
		g.AddEdge(toID, fromID, info.pathlen)
		if !followed[toID] {
			traverse(m, followed, g, toID, 1-info.idx)
		}
	}
	return
}

type Graph struct {
	edges []*Edge
	nodes []*Node
}

type Edge struct {
	parent *Node
	child  *Node
	len    int
}

type Node struct {
	id string
}

const Infinity = int(^uint(0) >> 1)

func (g *Graph) GetOrCreateNode(id string) *Node {
	if n := g.FindNode(id); n != nil {
		return n
	}
	n := &Node{id: id}
	g.nodes = append(g.nodes, n)
	return n
}

func (g *Graph) AddEdge(from, to string, length int) {
	parent := g.GetOrCreateNode(from)
	child := g.GetOrCreateNode(to)
	for _, edge := range g.edges {
		if edge.parent == parent && edge.child == child {
			if edge.len != length {
				panic("Tried to add inconsistent edge!")
			}
			return
		}
	}
	g.edges = append(g.edges, &Edge{parent: parent, child: child, len: length})
}

func (g *Graph) FindNode(id string) *Node {
	for _, n := range g.nodes {
		if n.id == id {
			return n
		}
	}
	return nil
}

func (g *Graph) NewLenTable(root *Node) map[*Node]int {
	lenTable := make(map[*Node]int)
	lenTable[root] = 0
	for _, node := range g.nodes {
		if node != root {
			lenTable[node] = Infinity
		}
	}
	return lenTable
}

func getNearestNode(lenTable map[*Node]int, visited map[*Node]bool) *Node {
	var result *Node
	minLen := Infinity
	for node, length := range lenTable {
		if !visited[node] {
			if length < minLen {
				minLen = length
				result = node
			}
		}
	}
	return result
}

func (g *Graph) GetNodeEdges(node *Node) (edges []*Edge) {
	for _, edge := range g.edges {
		if edge.parent == node {
			edges = append(edges, edge)
		}
	}
	return edges
}

func (g *Graph) Dijkstra(root *Node) {
	lenTable := g.NewLenTable(root)
	visited := map[*Node]bool{}
	for len(visited) != len(g.nodes) {
		node := getNearestNode(lenTable, visited)
		visited[node] = true
		edges := g.GetNodeEdges(node)
		for _, edge := range edges {
			distance := lenTable[node] + edge.len
			if distance < lenTable[edge.child] {
				lenTable[edge.child] = distance
			}
		}
	}
	for node, length := range lenTable {
		if node.id == "ZZ" {
			fmt.Printf("Distance from %s to %s: %d.\n", root.id, node.id, length)
		}
	}
}

func main() {
	f, _ := os.Open("input.txt")
	m := loadInput(bufio.NewReader(f))
	scanPortals(&m)
	visited := make([][]bool, len(m.data))
	for i := range m.data {
		visited[i] = make([]bool, len(m.data[i]))
	}
	for i := 0; i < 5; i++ {
		graph := Graph{}
		followed := map[string]bool{}
		traverse(&m, followed, &graph, "AA", 0)
		/*
		graph := Graph{}
		graph.AddEdge("AA", "BB", 10)
		graph.AddEdge("AA", "CC", 20)
		graph.AddEdge("BB", "DD", 5)
		graph.AddEdge("CC", "ZZ", 5)
		graph.AddEdge("DD", "ZZ", 50)
		*/
		graph.Dijkstra(graph.FindNode("AA"))
		/*
		for _, edge := range graph.edges {
			fmt.Println(edge.parent.id, edge.child.id, edge.len)
		}
		*/
	}
}
