const std = @import("std");

const test_input =
    \\7 6 4 2 1
    \\1 2 7 8 9
    \\9 7 6 2 1
    \\1 3 2 4 5
    \\8 6 4 4 1
    \\1 3 6 7 9
;

const Report = struct {
    data: []i32,
    valid: bool,

    fn check(self: *Report) bool {
        self.valid = true;

        var delta: i32 = self.data[1] - self.data[0];
        if (delta == 0) {
            self.valid = false;
        } else {
            const inc: bool = delta > 0;
            for (1..self.data.len) |i| {
                delta = self.data[i] - self.data[i - 1];
                if (delta == 0 or delta < 0 and inc or delta > 0 and !inc) {
                    self.valid = false;
                    break;
                } else if (inc and delta > 3 or !inc and delta < -3) {
                    self.valid = false;
                    break;
                }
            }
        }

        return self.valid;
    }
};

fn read_report(allocator: std.mem.Allocator, line: []const u8) !Report {
    var it = std.mem.splitScalar(u8, line, ' ');
    var count: usize = 0;
    while (it.next()) |val| {
        _ = val;
        count += 1;
    }
    it.reset();

    var data = try allocator.alloc(i32, count);
    for (0..count) |i| {
        data[i] = try std.fmt.parseInt(i32, it.next().?, 10);
    }

    return .{ .data = data, .valid = false };
}

fn read_input(allocator: std.mem.Allocator, input_data: []const u8, reports: *std.ArrayList(Report)) !void {
    const input_data_trimmed = std.mem.trim(u8, input_data, "\n");
    var lineit = std.mem.splitScalar(u8, input_data_trimmed, '\n');
    while (lineit.next()) |line| {
        var report = try read_report(allocator, line);
        _ = report.check();
        try reports.append(report);
    }
}

fn part1(allocator: std.mem.Allocator, input_data: []const u8) !void {
    var reports = std.ArrayList(Report).init(allocator);
    try read_input(allocator, input_data, &reports);

    var valid_reports: u32 = 0;
    for (reports.items) |item| {
        if (item.valid) {
            valid_reports += 1;
        }
    }

    std.debug.print("Part1: The number of valid reports is {d}.\n", .{valid_reports});
}

fn part2(allocator: std.mem.Allocator, input_data: []const u8) !void {
    var reports = std.ArrayList(Report).init(allocator);
    try read_input(allocator, input_data, &reports);

    var buffer: [4096]u8 = undefined;
    var fba = std.heap.FixedBufferAllocator.init(&buffer);
    const buf_alloc = fba.allocator();

    var valid_reports: u32 = 0;
    for (reports.items) |report| {
        if (report.valid) {
            valid_reports += 1;
        } else {
            for (0..report.data.len) |i| {
                var arena_allocator = std.heap.ArenaAllocator.init(buf_alloc);
                defer arena_allocator.deinit();

                var new_report = Report{ .data = try arena_allocator.allocator().alloc(i32, report.data.len - 1), .valid = false };
                for (0..i) |k| {
                    new_report.data[k] = report.data[k];
                }
                for (0..report.data.len - i - 1) |k| {
                    new_report.data[i + k] = report.data[i + k + 1];
                }
                if (new_report.check()) {
                    valid_reports += 1;
                    break;
                }
            }
        }
    }

    std.debug.print("Part2: The number of valid reports is {d}.\n", .{valid_reports});
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
