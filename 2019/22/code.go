package main

import (
	"bufio"
	"errors"
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
	"time"
)

type Deque struct {
	Items []interface{}
}

func NewDeque() *Deque {
	return &Deque{}
}

func (s *Deque) GetIndex(idx int) interface{} {
	if idx < 0 {
		return s.Items[s.Count()+idx]
	}
	return s.Items[idx]
}

func (s *Deque) FindFirst(item interface{}) (int, error) {
	for i := 0; i < s.Count(); i++ {
		if item == s.Items[i] {
			return i, nil
		}
	}
	return 0, errors.New("Item not found")
}

func (s *Deque) FindFirstRev(item interface{}) (int, error) {
	for i := 0; i < s.Count(); i++ {
		if item == s.Items[s.Count()-i-1] {
			return i, nil
		}
	}
	return 0, errors.New("Item not found")
}

func (s *Deque) PushLeft(item interface{}) {
	s.Items = append([]interface{}{item}, s.Items...)
}

func (s *Deque) Push(item interface{}) {
	s.Items = append(s.Items, item)
}

func (s *Deque) PopLeft() interface{} {
	defer func() {
		s.Items = s.Items[1:]
	}()
	return s.Items[0]
}

func (s *Deque) Pop() interface{} {
	last := s.Count() - 1
	defer func() {
		s.Items = s.Items[:last]
	}()
	return s.Items[last]
}

func (s *Deque) Reverse() {
	for i := 0; i < s.Count()/2; i++ {
		j := s.Count() - i - 1
		s.Items[i], s.Items[j] = s.Items[j], s.Items[i]
	}
}

func (s *Deque) Count() int {
	return len(s.Items)
}

func (s *Deque) IsEmpty() bool {
	return s.Count() == 0
}

func (s *Deque) Permute(perm []int) {
	if len(perm) != len(s.Items) {
		panic("Invalid permutation!")
	}
	tmp := make([]interface{}, len(perm))
	for i := 0; i < len(perm); i++ {
		tmp[perm[i]] = s.Items[i]
	}
	s.Items = tmp
}

type CardStack struct {
	Cards *Deque
}

func NewCardStack(count int) *CardStack {
	cards := NewDeque()
	for i := 0; i < count; i++ {
		cards.Push(count - i - 1)
	}
	return &CardStack{cards}
}

func (s *CardStack) DealNew() {
	s.Cards.Reverse()
}

func (s *CardStack) Cut(n int) {
	if n > 0 {
		for i := 0; i < n; i++ {
			s.Cards.PushLeft(s.Cards.Pop())
		}
	} else {
		for i := 0; i < -n; i++ {
			s.Cards.Push(s.Cards.PopLeft())
		}
	}
}

func (s *CardStack) DealWithIncrement(n int) {
	perm := make([]int, s.Cards.Count())
	for i := 0; i < s.Cards.Count(); i++ {
		perm[i] = ((i+1)*n - 1) % s.Cards.Count()
	}
	s.Cards.Permute(perm)
}

func shuffleAndFind(instructions string, cards, toFind int) {
	start := time.Now()
	s := NewCardStack(cards)
	scanner := bufio.NewScanner(strings.NewReader(instructions))
	for scanner.Scan() {
		var n int
		row := scanner.Text()
		fields := strings.Split(row, " ")
		if strings.Contains(row, "cut") {
			n, _ = strconv.Atoi(fields[len(fields)-1])
			s.Cut(n)
		} else if strings.Contains(row, "deal with increment") {
			n, _ = strconv.Atoi(fields[len(fields)-1])
			s.DealWithIncrement(n)
		} else if strings.Contains(row, "deal into new stack") {
			s.DealNew()
		} else {
			panic("Not implemented!")
		}
	}
	index, err := s.Cards.FindFirstRev(toFind)
	dt := time.Since(start)
	if err != nil {
		fmt.Printf("Card %d not found in deck!\n", toFind)
	} else {
		fmt.Printf("After shuffling the factory deck, the position of card %d is %d.\n", toFind, index)
	}
	fmt.Printf("Time: %v", dt)
}

func part1() {
	b, err := ioutil.ReadFile("input.txt")
	if err != nil {
		panic(err)
	}
	instructions := string(b)
	shuffleAndFind(instructions, 10007, 2019)
}

func main() {
	part1()
}
