package main

import (
	"fmt"
	"bufio"
	"strings"
	"io/ioutil"
	"time"
	"math"
	"sort"
)

type vec2i struct {
	x int
	y int
}

type Vec2iSlice []vec2i

func (p Vec2iSlice)Len() int {
	return len(p)
}

func (p Vec2iSlice)Less(i, j int) bool {
	return math.Hypot(float64(p[i].x), float64(p[i].y)) < math.Hypot(float64(p[j].x), float64(p[j].y))
}

func (p Vec2iSlice)Swap(i, j int) {
	p[i], p[j] = p[j], p[i]
}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func gcd(a, b int) int {
	for b != 0 {
		t := b
		b = a % b
		a = t
	}
 	return a;
}

func getAsteroidsFromStarmap(m string) []vec2i {
	var asteroids []vec2i
	scanner := bufio.NewScanner(strings.NewReader(m))
	for y := 0; scanner.Scan(); y++ {
		line := scanner.Text()
		for x := 0; x < len(line); x++ {
			if line[x] == '#' {
				asteroids = append(asteroids, vec2i{x, y})
			}
		}
	}
	return asteroids
}

func countVisibleAsteroids(asteroids []vec2i, fromIdx int) int {
	count := 0
	asteroid := asteroids[fromIdx]
	xy := make(map[vec2i]bool)
	for j, other := range asteroids {
		if fromIdx != j {
			x, y := asteroid.x - other.x, asteroid.y - other.y
			g := abs(gcd(x, y))
			v := vec2i{x / g, y / g}
			if !xy[v] {
				xy[v] = true
				count++
			}
		}
	}
	return count
}

func getKeys(dMap map[float64]Vec2iSlice) []float64 {
	keys := make([]float64, len(dMap))
	i := 0
	for key := range dMap {
		keys[i] = key
		i++
	}
	return keys
}

func getDirectionalMap(asteroids Vec2iSlice, fromIdx int) map[float64]Vec2iSlice {
	result := make(map[float64]Vec2iSlice)
	for j, other := range asteroids {
		if fromIdx != j {
			x, y := other.x - asteroids[fromIdx].x, other.y - asteroids[fromIdx].y
			g := abs(gcd(x, y))
			v := vec2i{x / g, y / g}
			phi := math.Atan2(float64(v.y), float64(v.x))
			if result[phi] == nil {
				result[phi] = Vec2iSlice{}
			}
			result[phi] = append(result[phi], vec2i{x, y})
			sort.Sort(result[phi])
		}
	}
	return result
}

func findBestAsteroid(starmap string) int {
	asteroids := getAsteroidsFromStarmap(starmap)
	maximum, maxIdx := 0, -1
	for i := range asteroids {
		count := countVisibleAsteroids(asteroids, i)
		if count > maximum {
			maximum = count
			maxIdx = i
		}
	}
	fmt.Printf("Best is %d,%d with %d other asteroids detected\n", asteroids[maxIdx].x, asteroids[maxIdx].y, maximum)
	return maxIdx
}

func runTests() {
	testMaps := []string{
`.#..#
.....
#####
....#
...##`,
`......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####`,
`#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.`,
`.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..`,
`.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##`}
	fmt.Println("Starting tests...")
	for _, m := range testMaps {
		findBestAsteroid(m)
	}
	fmt.Println("Done.")
}

func part1(starmap string) int {
	fmt.Println("Searching for best base location...")
	start := time.Now()
	result := findBestAsteroid(starmap)
	fmt.Println("Done.")
	fmt.Println(time.Since(start))
	return result
}

func part2(starmap string, refIdx int) {
	fmt.Println("Vaporizing asteroids...")
	asteroids := getAsteroidsFromStarmap(starmap)
	// NOTE: It was at this point, that patience was lost
	dMap := getDirectionalMap(asteroids, refIdx)
	keys := getKeys(dMap)
	sort.Float64s(keys)
	var ast vec2i
	offset := 0
	for i := 0; i < len(keys); i++ {
		if keys[i] >= -math.Pi / 2 {
			offset = i
			break
		}
	}
	for i := 0; i < 200; {
		idx := (offset + i) % len(keys)
		astList := dMap[keys[idx]]
		if len(astList) > 0 {
			ast, dMap[keys[idx]] = astList[0], astList[1:]
			ast.x += asteroids[refIdx].x
			ast.y += asteroids[refIdx].y
			i++
			suffix := "th"
			switch i % 10 {
			case 1: suffix = "st"
			case 2: suffix = "nd"
			case 3: suffix = "rd"
			}
			fmt.Printf("The %d%s asteroid to be vaporized is at %d,%d.\n", i, suffix, ast.x, ast.y)
		}
	}
	fmt.Printf("Answer: %d\n", 100 * ast.x + ast.y);
}

func main() {
	//runTests()

	starmap, _ := ioutil.ReadFile("input.txt")
	idx := part1(string(starmap))
	part2(string(starmap), idx)
}