package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"strings"
	"time"
)

const (
	Width  int = 5
	Height int = 5
)

type Level struct {
	field       [2][Height][Width]bool
	parent      *Level
	child       *Level
	needsUpdate bool
}

func NewLevel() *Level {
	return &Level{}
}

func (level *Level) Load(input string, readBuf int) {
	scanner := bufio.NewScanner(strings.NewReader(input))
	for j := range level.field[readBuf] {
		scanner.Scan()
		row := scanner.Text()
		for i := range level.field[readBuf][j] {
			var v bool
			if row[i] == '#' {
				v = true
			}
			level.field[readBuf][j][i] = v
		}
	}
}

func (level *Level) ToString(buf int) string {
	var b strings.Builder
	for j := range level.field[buf] {
		for i := range level.field[buf][j] {
			if level.field[buf][j][i] {
				b.WriteByte('#')
			} else {
				b.WriteByte('.')
			}
		}
		b.WriteByte('\n')
	}
	return b.String()
}

func (level *Level) GetRating(buf int) int {
	var rating int
	value := 1
	for j := range level.field[buf] {
		for i := range level.field[buf][j] {
			if level.field[buf][j][i] {
				rating += value
			}
			value <<= 1
		}
	}
	return rating
}

func (level *Level) UpdateCell(readBuf, writeBuf, i, j, adjacent int) {
	if level.field[readBuf][j][i] && adjacent != 1 {
		level.field[writeBuf][j][i] = false
	} else if !level.field[readBuf][j][i] && (adjacent == 1 || adjacent == 2) {
		level.field[writeBuf][j][i] = true
	} else {
		level.field[writeBuf][j][i] = level.field[readBuf][j][i]
	}
}

func (level *Level) Update(readBuf, writeBuf int) {
	offsets := [4][2]int{{0, -1}, {-1, 0}, {1, 0}, {0, 1}}
	for j := range level.field[readBuf] {
		for i := range level.field[readBuf][j] {
			var adjacent int
			for _, offset := range offsets {
				x, y := i+offset[0], j+offset[1]
				if x >= 0 && x < Width && y >= 0 && y < Height && level.field[readBuf][y][x] {
					adjacent++
				}
			}
			level.UpdateCell(readBuf, writeBuf, i, j, adjacent)
		}
	}
}

func (root *Level) PreparePlutonianUpdate() {
	for p := root; p != nil; p = p.child {
		p.needsUpdate = true
	}
}

func (level *Level) AddChild() *Level {
	if level.child != nil {
		panic("Overwriting child!")
	}
	child := NewLevel()
	level.child = child
	child.parent = level
	return child
}

func (level *Level) AddParent() *Level {
	if level.parent != nil {
		panic("Overwriting parent!")
	}
	parent := NewLevel()
	level.parent = parent
	parent.child = level
	return parent
}

func (level *Level) CountChildAdjacency(readBuf, dx, dy int) int {
	var adjacent int
	if level.child != nil {
		switch dx {
		case -1:
			for k := 0; k < Height; k++ {
				if level.child.field[readBuf][k][Width-1] {
					adjacent++
				}
			}
		case 0:
			switch dy {
			case -1:
				for k := 0; k < Width; k++ {
					if level.child.field[readBuf][Height-1][k] {
						adjacent++
					}
				}
			case 1:
				for k := 0; k < Width; k++ {
					if level.child.field[readBuf][0][k] {
						adjacent++
					}
				}
			default:
				panic("Invalid offset!")
			}
		case 1:
			for k := 0; k < Height; k++ {
				if level.child.field[readBuf][k][0] {
					adjacent++
				}
			}
		default:
			panic("Invalid offset!")
		}
	}
	return adjacent
}

func (level *Level) CountParentAdjacency(readBuf, dx, dy int) int {
	var adjacent int
	if level.parent != nil {
		switch dx {
		case -1:
			if level.parent.field[readBuf][2][1] {
				adjacent++
			}
		case 0:
			switch dy {
			case -1:
				if level.parent.field[readBuf][1][2] {
					adjacent++
				}
			case 1:
				if level.parent.field[readBuf][3][2] {
					adjacent++
				}
			default:
				panic("Invalid offset!")
			}
		case 1:
			if level.parent.field[readBuf][2][3] {
				adjacent++
			}
		default:
			panic("Invalid offset!")
		}
	}
	return adjacent
}

func (level *Level) UpdatePlutonian(readBuf, writeBuf int) {
	level.needsUpdate = false
	offsets := [4][2]int{{0, -1}, {-1, 0}, {1, 0}, {0, 1}}
	for j := range level.field[readBuf] {
		for i := range level.field[readBuf][j] {
			if i == 2 && j == 2 {
				continue
			}
			var adjacent int
			for _, offset := range offsets {
				x, y := i+offset[0], j+offset[1]
				if x == 2 && y == 2 {
					adjacent += level.CountChildAdjacency(readBuf, offset[0], offset[1])
				} else if x >= 0 && x < Width && y >= 0 && y < Height {
					if level.field[readBuf][y][x] {
						adjacent++
					}
				} else {
					adjacent += level.CountParentAdjacency(readBuf, offset[0], offset[1])
				}
			}
			level.UpdateCell(readBuf, writeBuf, i, j, adjacent)
		}
	}

	bugs := level.CountBugs(writeBuf)
	tryUpdate := func(p *Level) bool {
		if p != nil {
			if p.needsUpdate {
				p.UpdatePlutonian(readBuf, writeBuf)
			}
		}
		return p != nil
	}
	if exists := tryUpdate(level.parent); !exists && bugs > 0 {
		level.AddParent()
	}
	if exists := tryUpdate(level.child); !exists && bugs > 0 {
		level.AddChild()
	}
}

func (level *Level) CountBugs(buf int) int {
	var count int
	for j := range level.field[buf] {
		for i := range level.field[buf][j] {
			if i == 2 && j == 2 {
				continue
			}
			if level.field[buf][j][i] {
				count++
			}
		}
	}
	return count
}

func (root *Level) CountAllBugs(buf int) int {
	var count int
	for p := root; p != nil; p = p.child {
		count += p.CountBugs(buf)
	}
	return count
}

func (level *Level) DrawChildren(buf, depth int) {
	fmt.Printf("Depth %d:\n", depth)
	fmt.Println(level.ToString(buf))
	if level.child != nil {
		level.child.DrawChildren(buf, depth+1)
	}
}

func (level *Level) FindRoot(baseDepth int) (*Level, int) {
	root := level
	depth := baseDepth
	for p := root.parent; p != nil; p = p.parent {
		root = p
		depth--
	}
	return root, depth
}

func part1(input5x5 string) {
	readBuf := 0
	level := NewLevel()
	level.Load(input5x5, readBuf)
	states := map[int]bool{}
	n := 0
	for {
		writeBuf := 1 - readBuf
		rating := level.GetRating(readBuf)
		if states[rating] {
			fmt.Printf("Biodiversity rating after %d minutes: %d\n", n, rating)
			return
		}
		states[rating] = true
		level.Update(readBuf, writeBuf)
		readBuf, writeBuf = writeBuf, readBuf
		n++
	}
}

func part2(input5x5 string, count int) {
	start := time.Now()
	readBuf := 0
	level0 := NewLevel()
	level0.Load(input5x5, readBuf)
	level0.AddParent()
	level0.AddChild()
	for n := 0; n < count; n++ {
		writeBuf := 1 - readBuf
		root, _ := level0.FindRoot(0)
		root.PreparePlutonianUpdate()
		level0.UpdatePlutonian(readBuf, writeBuf)
		readBuf, writeBuf = writeBuf, readBuf
	}
	root, depth := level0.FindRoot(0)
	root.DrawChildren(readBuf, depth)
	fmt.Printf("After %d minutes, there are %d bugs present\n", count, root.CountAllBugs(readBuf))
	fmt.Println(time.Since(start))
}

func main() {
	input5x5, err := ioutil.ReadFile("input.txt")
	if err != nil {
		panic(err)
	}

	part1(string(input5x5))
	part2(string(input5x5), 200)
}
