package main

import (
	"bufio"
	"time"
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

type chemical struct {
	amount int
	name   string
}

type reaction struct {
	reactants []chemical
	product   chemical
}

func ParseChemical(s string) chemical {
	part := strings.SplitN(s, " ", 2)
	amount, err := strconv.Atoi(part[0])
	if err != nil {
		panic(err)
	}
	return chemical{amount: amount, name: part[1]}
}

func GetReactions(r io.Reader) (reactions []reaction) {
	scanner := bufio.NewScanner(r)
	for scanner.Scan() {
		line := scanner.Text()
		react := []chemical{}
		part := strings.SplitN(line, " => ", 2)
		for _, c := range strings.Split(part[0], ",") {
			react = append(react, ParseChemical(strings.Trim(c, " ")))
		}
		prod := ParseChemical(strings.Trim(part[1], " "))
		reactions = append(reactions, reaction{reactants: react, product: prod})
	}
	return
}

func Produce(products map[string]int, reactions map[string]*reaction, name string, oreTotal *int) (produced int) {
	for _, r := range reactions[name].reactants {
		if r.name == "ORE" {
			*oreTotal += r.amount
		} else {
			toProduce := r.amount
			if val, exists := products[r.name]; exists && val > 0 {
				if toProduce <= val {
					toProduce = 0
				} else {
					toProduce -= val
				}
			}

			var amount int
			for amount < toProduce {
				amount += Produce(products, reactions, r.name, oreTotal)
			}
			products[r.name] -= r.amount
		}
	}
	p := reactions[name].product
	products[p.name] += p.amount
	return p.amount
}

func part1(reactions map[string]*reaction) {
	var total int
	products := map[string]int{}
	Produce(products, reactions, "FUEL", &total)
	fmt.Printf("%d ORE for 1 FUEL\n", total)
}

func part2(reactions map[string]*reaction) {
	var total, last int
	products := map[string]int{}
	start := time.Now()
	for total <= 1000000000000 {
		last = total
		Produce(products, reactions, "FUEL", &total)
	}
	fmt.Printf("%d ORE for %d FUEL\n", last, products["FUEL"])
	fmt.Println(time.Since(start))
}

func main() {
	f, _ := os.Open("input.txt")
	defer f.Close()

	/*
	   	   f := strings.NewReader(`10 ORE => 10 A
	   1 ORE => 1 B
	   7 A, 1 B => 1 C
	   7 A, 1 C => 1 D
	   7 A, 1 D => 1 E
	   7 A, 1 E => 1 FUEL`)
	*/

	/*
	   f := strings.NewReader(`9 ORE => 2 A
	   8 ORE => 3 B
	   7 ORE => 5 C
	   3 A, 4 B => 1 AB
	   5 B, 7 C => 1 BC
	   4 C, 1 A => 1 CA
	   2 AB, 3 BC, 4 CA => 1 FUEL`)
	*/

	/*
	   f := strings.NewReader(`157 ORE => 5 NZVS
	   165 ORE => 6 DCFZ
	   44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
	   12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
	   179 ORE => 7 PSHF
	   177 ORE => 5 HKGWZ
	   7 DCFZ, 7 PSHF => 2 XJWVT
	   165 ORE => 2 GPVTF
	   3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT`)
	*/

	/*
			f := strings.NewReader(`2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
		17 NVRVD, 3 JNWZP => 8 VPVL
		53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
		22 VJHF, 37 MNCFX => 5 FWMGM
		139 ORE => 4 NVRVD
		144 ORE => 7 JNWZP
		5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
		5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
		145 ORE => 6 MNCFX
		1 NVRVD => 8 CXFTF
		1 VJHF, 6 MNCFX => 4 RFSQX
		176 ORE => 6 VJHF`)
	*/
	/*
	   f := strings.NewReader(`171 ORE => 8 CNZTR
	   7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
	   114 ORE => 4 BHXH
	   14 VRPVC => 6 BMBT
	   6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
	   6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
	   15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
	   13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
	   5 BMBT => 4 WPTQ
	   189 ORE => 9 KTJDG
	   1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
	   12 VRPVC, 27 CNZTR => 2 XDBXC
	   15 KTJDG, 12 BHXH => 5 XCVML
	   3 BHXH, 2 VRPVC => 7 MZWV
	   121 ORE => 7 VRPVC
	   7 XCVML => 6 RJRHP
	   5 BHXH, 4 VRPVC => 5 LTCX`)
	*/	
	reactions := map[string]*reaction{}
	r := GetReactions(f)
	for i := range r {
		reactions[r[i].product.name] = &r[i]
	}
	part1(reactions)
	part2(reactions)
}
