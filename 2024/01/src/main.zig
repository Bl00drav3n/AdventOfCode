const std = @import("std");

const test_input =
    \\3   4
    \\4   3
    \\2   5
    \\1   3
    \\3   9
    \\3   3
    \\
;

const Pair = struct { a: i32, b: i32 };
const Lists = struct { left: []i32, right: []i32, count: usize };

fn pair_from_line(line: []const u8) !Pair {
    var it = std.mem.splitSequence(u8, line, "   ");
    return Pair{
        .a = try std.fmt.parseInt(i32, it.next() orelse "", 10),
        .b = try std.fmt.parseInt(i32, it.next() orelse "", 10),
    };
}

fn count_occurences(items: []const i32, value: i32) i32 {
    var sum: i32 = 0;
    for (items) |item| {
        if (item == value) {
            sum += 1;
        }
    }
    return sum;
}

fn init(allocator: std.mem.Allocator, input_data: []const u8) !Lists {
    var pairs = std.ArrayList(Pair).init(allocator);
    var it = std.mem.splitScalar(u8, input_data, '\n');
    while (it.next()) |line| {
        if (line.len > 0) {
            const pair = try pair_from_line(line);
            try pairs.append(pair);
        }
    }
    pairs = pairs;
    var lvalues: []i32 = try allocator.alloc(i32, pairs.items.len);
    var rvalues: []i32 = try allocator.alloc(i32, pairs.items.len);
    for (pairs.items, 0..) |pair, i| {
        lvalues[i] = pair.a;
        rvalues[i] = pair.b;
    }

    std.mem.sort(i32, lvalues, {}, std.sort.asc(i32));
    std.mem.sort(i32, rvalues, {}, std.sort.asc(i32));

    return .{ .left = lvalues, .right = rvalues, .count = pairs.items.len };
}

fn part1(allocator: std.mem.Allocator, input_data: []const u8) !void {
    const lists = try init(allocator, input_data);
    var sum: u32 = 0;
    for (0..lists.count) |i| {
        sum += @abs(lists.left[i] - lists.right[i]);
    }
    std.debug.print("Part1: The total distance between the lists is {d}.\n", .{sum});
}

fn part2(allocator: std.mem.Allocator, input_data: []const u8) !void {
    const lists = try init(allocator, input_data);
    var score: i32 = 0;
    for (lists.left) |lvalue| {
        const count = count_occurences(lists.right, lvalue);
        score += count * lvalue;
    }
    std.debug.print("Part2: The similarity score of the lists is {d}.\n", .{score});
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
