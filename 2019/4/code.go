package main

import (
  "fmt"
  "strconv"
)

func asciiToDigit(c byte) int {
  return int(c - '0')
}

func checkPasswordRules1(n int) bool {
  result := false
  digits := strconv.Itoa(n)
  if len(digits) == 6 {
    last := -1
    for i := range(digits) {
      digit := asciiToDigit(digits[i])
      if digit < last {
        return false
      } else if digit == last {
        result = true
      }
      last = digit
    }
  } else {
    fmt.Printf("Number not in range: %d\n", n)
  }
  return result
}

func checkPasswordRules2(n int) bool {
  result := false
  digits := strconv.Itoa(n)
  var run int
  if len(digits) == 6 {
    last := -1
    for i := range(digits) {
      digit := asciiToDigit(digits[i])
      if digit < last {
        return false
      } else if digit == last {
        run++
      } else {
        if run == 2 {
          result = true
        }
        run = 1
      }
      last = digit
    }
  } else {
    fmt.Printf("Number not in range: %d\n", n)
  }
  return result || run == 2
}

func getPasswordsForRange(lower, upper int, check func(int) bool) []int {
  var pwds []int
  for n := lower; n <= upper; n++ {
    if check(n) {
      pwds = append(pwds, n)
    }
  }
  return pwds
}

func solve(lower, upper int, check func(int) bool) {
  pwds := getPasswordsForRange(lower, upper, check)
  fmt.Printf("Number of possible passwords: %d\n", len(pwds))
}

func main() {
  lower := 178416
  upper := 676461
  solve(lower, upper, checkPasswordRules1)
  solve(lower, upper, checkPasswordRules2)
}