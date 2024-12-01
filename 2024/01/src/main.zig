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

fn get_next(comptime T: type, it: *T) []const u8 {
    if (it.*.next()) |string| {
        return string;
    }
    return "";
}

fn ordered_pair_from_line(line: []const u8) !Pair {
    var it = std.mem.splitSequence(u8, line, "   ");
    return Pair{
        .a = try std.fmt.parseInt(i32, get_next(@TypeOf(it), &it), 10),
        .b = try std.fmt.parseInt(i32, get_next(@TypeOf(it), &it), 10),
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

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const allocator = gpa.allocator();
    var pairs = std.ArrayList(Pair).init(allocator);

    // For testing uncomment this and comment out input data
    //var reader = std.io.fixedBufferStream(test_input);
    //var stream = reader.reader();

    // The input data
    var file = try std.fs.cwd().openFile("input.txt", .{});
    var reader = std.io.bufferedReader(file.reader());
    var stream = reader.reader();

    var line = std.ArrayList(u8).init(allocator);
    const line_writer = line.writer();
    while (stream.streamUntilDelimiter(line_writer, '\n', null)) {
        defer line.clearRetainingCapacity();
        try pairs.append(try ordered_pair_from_line(line.items));
    } else |err| switch (err) {
        error.EndOfStream => {},
        else => return err,
    }

    var lvalues: []i32 = try allocator.alloc(i32, pairs.items.len);
    var rvalues: []i32 = try allocator.alloc(i32, pairs.items.len);
    for (pairs.items, 0..) |pair, i| {
        lvalues[i] = pair.a;
        rvalues[i] = pair.b;
    }

    std.mem.sort(i32, lvalues, {}, std.sort.asc(i32));
    std.mem.sort(i32, rvalues, {}, std.sort.asc(i32));

    var sum: u32 = 0;
    for (0..pairs.items.len) |i| {
        sum += @abs(lvalues[i] - rvalues[i]);
    }
    std.debug.print("Part1: The total distance between the lists is {d}.\n", .{sum});

    var score: i32 = 0;
    for (lvalues) |lvalue| {
        const count = count_occurences(rvalues, lvalue);
        score += count * lvalue;
    }
    std.debug.print("Part2: The similarity score of the lists is {d}.\n", .{score});
}
