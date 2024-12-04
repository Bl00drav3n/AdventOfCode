const std = @import("std");

//const test_input = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))";
const test_input = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))";

const TokenType = enum { Identifier, OpenParen, CloseParen, Numeric, Comma, Unknown };
const Token = union(TokenType) { Identifier: []const u8, OpenParen: u8, CloseParen: u8, Numeric: u64, Comma: u8, Unknown: u8 };

fn read_identifier(p: *Parser, identifier: []const u8) Token {
    var token = Token{ .Unknown = p.data[p.index] };
    if (p.index + identifier.len < p.data.len) {
        if (std.mem.eql(u8, p.data[p.index .. p.index + identifier.len], identifier)) {
            token = Token{ .Identifier = identifier[0 .. identifier.len - 1] };
            p.index += identifier.len - 2;
        }
    }
    return token;
}

fn read_do(p: *Parser) Token {
    var tk = read_identifier(p, "do(");
    if (tk != .Identifier) {
        tk = read_identifier(p, "don't(");
    }
    return tk;
}

fn read_numeric(p: *Parser) Token {
    var sum: u64 = 0;
    while (p.index < p.data.len) {
        const byte: u8 = p.data[p.index];
        switch (byte) {
            '0'...'9' => {
                sum = 10 * sum + byte - '0';
                p.index += 1;
            },
            else => {
                break;
            },
        }
    }
    p.index -= 1;
    return Token{ .Numeric = sum };
}

fn print_token(tk: Token) void {
    switch (tk) {
        .CloseParen => std.debug.print(") ", .{}),
        .OpenParen => std.debug.print("( ", .{}),
        .Comma => std.debug.print(", ", .{}),
        .Identifier => std.debug.print("{s} ", .{tk.Identifier}),
        .Numeric => std.debug.print("{d} ", .{tk.Numeric}),
        .Unknown => std.debug.print("{c} ", .{tk.Unknown}),
    }
}

const Parser = struct { data: []const u8, index: usize };

fn parse(allocator: std.mem.Allocator, input_data: []const u8) !std.ArrayList(Token) {
    var tokens = std.ArrayList(Token).init(allocator);
    var p = Parser{ .data = input_data, .index = 0 };
    while (p.index < p.data.len) {
        const byte: u8 = p.data[p.index];
        const token: Token = switch (byte) {
            'm' => read_identifier(&p, "mul("),
            'd' => read_do(&p),
            '1'...'9' => read_numeric(&p),
            '(' => Token{ .OpenParen = byte },
            ')' => Token{ .CloseParen = byte },
            ',' => Token{ .Comma = byte },
            else => Token{ .Unknown = byte },
        };
        p.index += 1;
        try tokens.append(token);
    }

    return tokens;
}

fn check_sequence(tokens: std.ArrayList(Token), index: usize, sequence: []const TokenType) bool {
    if (index + sequence.len >= tokens.items.len) {
        return false;
    }
    for (0..sequence.len) |i| {
        if (tokens.items[index + i + 1] != sequence[i]) {
            return false;
        }
    }
    return true;
}

fn part1(allocator: std.mem.Allocator, input_data: []const u8) !void {
    const tokens = try parse(allocator, input_data);
    var total: u64 = 0;
    var index: usize = 0;
    while (index < tokens.items.len) {
        const tk = tokens.items[index];
        switch (tk) {
            .Identifier => {
                if (std.mem.eql(u8, tk.Identifier, "mul")) {
                    const seq = [_]TokenType{ .OpenParen, .Numeric, .Comma, .Numeric, .CloseParen };
                    if (check_sequence(tokens, index, &seq)) {
                        const a: u64 = tokens.items[index + 2].Numeric;
                        const b: u64 = tokens.items[index + 4].Numeric;
                        total += a * b;
                        index += seq.len + 1;
                        continue;
                    }
                }
                index += 1;
            },
            else => {
                index += 1;
            },
        }
    }

    std.debug.print("Part1: The result of adding up all uncorrupted mul instructions is {d}.\n", .{total});
}

fn part2(allocator: std.mem.Allocator, input_data: []const u8) !void {
    const tokens = try parse(allocator, input_data);
    var enabled: bool = true;
    var total: u64 = 0;
    var index: usize = 0;
    while (index < tokens.items.len) {
        const tk = tokens.items[index];
        switch (tk) {
            .Identifier => {
                if (std.mem.eql(u8, tk.Identifier, "mul")) {
                    const seq = [_]TokenType{ .OpenParen, .Numeric, .Comma, .Numeric, .CloseParen };
                    if (check_sequence(tokens, index, &seq)) {
                        const a: u64 = tokens.items[index + 2].Numeric;
                        const b: u64 = tokens.items[index + 4].Numeric;
                        if (enabled) {
                            total += a * b;
                        }
                        index += seq.len + 1;
                        continue;
                    }
                } else if (std.mem.eql(u8, tk.Identifier, "do")) {
                    if (index + 2 < tokens.items.len) {
                        if (tokens.items[index + 1] == .OpenParen and tokens.items[index + 2] == .CloseParen) {
                            enabled = true;
                            index += 3;
                            continue;
                        }
                    }
                } else if (std.mem.eql(u8, tk.Identifier, "don't")) {
                    if (index + 2 < tokens.items.len) {
                        if (tokens.items[index + 1] == .OpenParen and tokens.items[index + 2] == .CloseParen) {
                            enabled = false;
                            index += 3;
                            continue;
                        }
                    }
                }
                index += 1;
            },
            else => {
                index += 1;
            },
        }
    }

    std.debug.print("Part2: The result of adding up all enabled uncorrupted mul instructions is {d}.\n", .{total});
}

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const allocator = gpa.allocator();
    const buffer: []u8 = try allocator.alloc(u8, 1024 * 1024 * 1024);

    // The input data
    var file = try std.fs.cwd().openFile("input.txt", .{});
    const size = try file.readAll(buffer);
    const input_data = buffer[0..size];

    std.debug.print("---TEST DATA---\n", .{});
    try part1(allocator, test_input);
    try part2(allocator, test_input);

    std.debug.print("---INPUT DATA---\n", .{});
    try part1(allocator, input_data);
    try part2(allocator, input_data);
}
