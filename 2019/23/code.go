package main

import (
	"AdventOfCode/icpu"
	"errors"
	"fmt"
	"sync"
)

type computer struct {
	queueMutex sync.Mutex
	packets    []*packet
	nic        *icpu.IntComputer
	idle       bool
}

type packet struct {
	addr int
	x    int
	y    int
}

func dequeue(c *computer) (*packet, error) {
	c.queueMutex.Lock()
	defer c.queueMutex.Unlock()
	if len(c.packets) == 0 {
		return &packet{}, errors.New("Queue is empty!")
	}
	p := c.packets[0]
	c.packets = c.packets[1:]
	return p, nil
}

func enqueue(c *computer, p *packet) {
	c.queueMutex.Lock()
	defer c.queueMutex.Unlock()
	c.packets = append(c.packets, p)
}

func runNIC(c *computer, addr int) {
	go icpu.Run(c.nic)
	<-icpu.RequestedInput(c.nic)
	icpu.Send(c.nic, addr)
	fmt.Println("Computer", addr, "connected.")
	for {
		select {
		case <-icpu.Halted(c.nic):
			fmt.Println("Computer", addr, "halted.")
			return
		default:
		}
		<-icpu.RequestedInput(c.nic)
		p, err := dequeue(c)
		if err != nil {
			icpu.Send(c.nic, -1)
			c.idle = true
		} else {
			icpu.Send(c.nic, p.x)
			<-icpu.RequestedInput(c.nic)
			icpu.Send(c.nic, p.y)
			fmt.Println("Computer", addr, "received packet", *p)
			c.idle = false
		}
	}
}

func main() {
	var NAT packet
	var computers [50]computer
	code := icpu.ReadProgram("input.txt")

	for i := range computers {
		computers[i].nic = icpu.LoadProgram(code, 1000)
		go runNIC(&computers[i], i)
	}

	NATavailable := false
	firstNAT := true
	var lastY int
	for {
		for i := range computers {
			c := &computers[i]
			select {
			case addr := <-icpu.Receive(c.nic):
				var p packet
				p.addr = addr
				p.x = <-icpu.Receive(c.nic)
				p.y = <-icpu.Receive(c.nic)
				if p.addr < len(computers) {
					fmt.Println("Sending packet", p, "from", i)
					enqueue(&computers[p.addr], &p)
				} else if p.addr == 255 {
					fmt.Println("Received NAT packet", p, "from", i)
					NAT = p
					NATavailable = true
				}
			default:
			}
		}
		idle := true
		for i := range computers {
			if !computers[i].idle {
				idle = false
				break
			}
		}
		if idle && NATavailable {
			fmt.Println("System is idle, NAT packet:", NAT)
			if firstNAT {
				firstNAT = false
			} else if lastY == NAT.y {
				fmt.Println("The first Y value delivered by the NAT to computer 0 twice in a row is", NAT.y)
				return
			}
			lastY = NAT.y
			p := packet{addr: 0, x: NAT.x, y: NAT.y}
			enqueue(&computers[0], &p)
			NATavailable = false
		}
	}
}
