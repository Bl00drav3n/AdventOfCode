const std = @import("std");

const test_input =
    \\
;

fn part1(allocator: std.mem.Allocator, input_data: []const u8) !void {
    std.debug.print("Part1: .\n", .{});
}

fn part2(allocator: std.mem.Allocator, input_data: []const u8) !void {
    std.debug.print("Part2: .\n", .{});
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
