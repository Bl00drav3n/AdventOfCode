package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strings"
	"time"
)

type location [2]int
type locmap map[byte]location

func readInput(f *bufio.Reader) (maze [][]byte) {
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		buf := scanner.Bytes()
		row := make([]byte, len(buf))
		copy(row, buf)
		maze = append(maze, row)
	}
	return
}

func isKey(b byte) bool {
	return b >= 'a' && b <= 'z'
}

func isDoor(b byte) bool {
	return b >= 'A' && b <= 'A'
}

func isTraversable(b byte) bool {
	return isKey(b) || b == '.' || b == '@'
}

func getDoorForKey(b byte) byte {
	if isKey(b) {
		return 'A' + (b - 'a')
	}
	panic("Invalid key!")
}

func openDoor(maze [][]byte, loc locmap, key byte) {
	p := loc[getDoorForKey(key)]
	x, y := p[0], p[1]
	maze[y][x] = '.'
}

func printState(maze [][]byte, visited [][]bool, x, y int) {
	var b strings.Builder
	for iy := range maze {
		for ix, value := range maze[iy] {
			if visited[iy][ix] {
				value = '*'
			}
			if x == ix && y == iy {
				value = '@'
			}
			b.WriteByte(value)
		}
		b.WriteByte('\n')
	}
	fmt.Print(b.String())
	//time.Sleep(1 * time.Millisecond)
}

type walker struct {
	distances [][]int
	reachable []byte
	maze      [][]byte
	visited   [][]bool
	from      byte
	to        byte
	found     bool
}

func keyToIdx(key byte) byte {
	if key == '@' {
		return 0
	}
	return key - 'a' + 1
}

func distance(w *walker, x, y, steps int) {
	if !w.found {
		if !w.visited[y][x] && w.maze[y][x] != '#' {
			w.visited[y][x] = true
			if w.maze[y][x] == w.to {
				i, j := keyToIdx(w.from), keyToIdx(w.to)
				w.distances[i][j] = steps
				w.distances[j][i] = steps
				w.found = true
				return
			}
			distance(w, x-1, y, steps+1)
			distance(w, x+1, y, steps+1)
			distance(w, x, y-1, steps+1)
			distance(w, x, y+1, steps+1)
		}
	}
}

func traverse(w *walker, x, y int) {
	if !w.visited[y][x] && isTraversable(w.maze[y][x]) {
		w.visited[y][x] = true
		if isKey(w.maze[y][x]) {
			w.reachable = append(w.reachable, w.maze[y][x])
		}
		traverse(w, x-1, y)
		traverse(w, x+1, y)
		traverse(w, x, y-1)
		traverse(w, x, y+1)
	}
}

func copyMaze(src [][]byte) (dst [][]byte) {
	dst = make([][]byte, len(src))
	for i := range src {
		dst[i] = make([]byte, len(src[i]))
		copy(dst[i], src[i])
	}
	return
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

type cacheval struct {
	currentKey byte
	keys       string
}

type cache map[cacheval]int

func distanceToCollectKeys(distances [][]int, maze [][]byte, loc locmap, currentKey byte, keys string, c *cache) int {
	if len(keys) == 0 {
		return 0
	}

	cacheKey := cacheval{currentKey: currentKey, keys: keys}
	if val, ok := (*c)[cacheKey]; ok {
		return val
	}

	result := 0x7fffffffffffffff
	var w walker
	w.distances = distances
	w.maze = copyMaze(maze)
	w.visited = make([][]bool, len(maze))
	w.from = currentKey
	p := loc[currentKey]
	x, y := p[0], p[1]
	w.maze[y][x] = '.'
	if currentKey != '@' {
		openDoor(w.maze, loc, currentKey)
	}
	for i := range w.visited {
		w.visited[i] = make([]bool, len(maze[i]))
	}
	// NOTE: Find reachable keys for current state
	traverse(&w, p[0], p[1])
	sort.Slice(w.reachable, func(i, j int) bool { return w.reachable[i] < w.reachable[j] })
	reachableStr := string(w.reachable)
	for _, key := range reachableStr {
		newKeys := strings.ReplaceAll(keys, string(key), "")
		d := w.distances[keyToIdx(currentKey)][keyToIdx(byte(key))] + distanceToCollectKeys(distances, w.maze, loc, byte(key), newKeys, c)
		result = min(result, d)
	}
	(*c)[cacheKey] = result
	return result
}

func main() {
	f, err := os.Open("input.txt")
	if err != nil {
		panic(err)
	}
	defer f.Close()

	/*
			f := strings.NewReader(`########################
		#@..............ac.GI.b#
		###d#e#f################
		###A#B#C################
		###g#h#i################
		########################`)
	*/

	start := time.Now()
	maze := readInput(bufio.NewReader(f))
	loc := make(locmap)
	for y := range maze {
		for x, id := range maze[y] {
			if id != '#' && id != '.' {
				var p location
				p[0], p[1] = x, y
				loc[id] = p
			}
		}
	}

	var w walker
	w.maze = maze
	w.visited = make([][]bool, len(maze))
	w.distances = make([][]int, 27)
	for i := range w.distances {
		w.distances[i] = make([]int, 27)
	}
	for a := byte('a'); a <= 'z'; a++ {
		x, y := loc[a][0], loc[a][1]
		for b := a + 1; b <= 'z'; b++ {
			w.from = a
			w.to = b
			w.found = false
			for i := range w.visited {
				w.visited[i] = make([]bool, len(maze[i]))
			}
			w.distances[keyToIdx(a)][keyToIdx(a)] = 0
			distance(&w, x, y, 0)
		}
		w.from = a
		w.to = '@'
		w.found = false
		for i := range w.visited {
			w.visited[i] = make([]bool, len(maze[i]))
		}
		w.distances[keyToIdx(a)][keyToIdx(a)] = 0
		distance(&w, x, y, 0)
	}
	c := cache{}
	keys := []byte{}
	for key := range loc {
		if key != '@' && key >= 'a' && key <= 'z' {
			keys = append(keys, key)
		}
	}
	sort.Slice(keys, func(i, j int) bool { return keys[i] < keys[j] })
	fmt.Println("Minimal length:", distanceToCollectKeys(w.distances, maze, loc, '@', string(keys), &c))
	fmt.Println(time.Since(start))
}
