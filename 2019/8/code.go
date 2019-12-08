package main

import (
	"fmt"
	"io/ioutil"
)

type imageSIF struct {
	layers [][]byte
	width  int
	height int
}

func readSIF(img []byte, width, height int) imageSIF {
	layerSize := width * height
	layerCount := len(img) / layerSize
	layers := make([][]byte, layerCount)
	for i := 0; i < layerCount; i++ {
		offset := i * layerSize
		layers[i] = img[offset:offset+layerSize]
	}
	return imageSIF{layers, width, height}
}

func validateSIF(img imageSIF) int {
	counts := make([][]int, len(img.layers))
	for i, layer := range(img.layers) {
		count := make([]int, 3)
		for _, c := range(layer) {
			switch c {
			case '0': count[0]++
			case '1': count[1]++
			case '2': count[2]++
			}
		}
		counts[i] = count
	}

	minIdx := -1
	minValue := 0x7fffffff
	for i, count := range(counts) {
		if count[0] < minValue {
			minValue = count[0]
			minIdx = i
		}
	}
	return counts[minIdx][1] * counts[minIdx][2]
}

func decodeSIF(img imageSIF) [][]byte {
	decoded := make([][]byte, img.height)
	for y := 0; y < img.height; y++ {
		row := make([]byte, img.width)
		for x := 0; x < img.width; x++ {
			var code byte = '2'
			for layer := len(img.layers) - 1; layer >= 0; layer-- {
				newCode := img.layers[layer][y * img.width + x]
				if newCode != '2' {
					code = newCode
				}
			}
			switch code {
			case '0': row[x] = ' '
			case '1': row[x] = '*'
			default: panic("Invalid color")
			}
		}
		decoded[y] = row
	}
	return decoded
}

func main() {
	img, _ := ioutil.ReadFile("input.txt")
	layers := readSIF(img, 25, 6)
	fmt.Printf("Validation: %d\n", validateSIF(layers))
	decoded := decodeSIF(layers)
	for _, row := range(decoded) {
		fmt.Println(string(row))
	}
}