all: build

test:
	@go test ./... -v
.PHONY: test

dep:
	@go mod tidy
.PHONY: dep

build: dep
	@go build ./...
.PHONY: build

bench:
	@go test ./... --bench=. -v
.PHONY: bench
