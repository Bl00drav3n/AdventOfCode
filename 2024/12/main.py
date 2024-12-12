test_input = '''
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
'''

def int_seq_to_ranges(seq):
    # Not pretty, but works. Converts a sequence of strictly increasing integers to a list of ranges
    runs = []
    if seq:
        last = seq[0]
        run = last
        for i in range(1, len(seq)):
            if seq[i] - seq[i-1] > 1:
                runs.append((last, run + 1))
                last = seq[i]
                run = last
            else:
                run += 1
        if not runs:
            runs.append((seq[0], seq[-1] + 1))
        else:
            runs.append((last, run + 1))
    return runs

class Gardens:
    def __init__(self, input):
        self.grid = [line for line in input.strip().split('\n')]
        self.bounds = len(self.grid[0]), len(self.grid)
        self.plots_map = self.create_plots_map()
        self.regions_map = self.create_regions()

    def create_plots_map(self):
        plots_map = {}
        for y, line in enumerate(self.grid):
            for x, plot in enumerate(line):
                if not plot in plots_map:
                    plots_map[plot] = set()
                plots_map[plot].add((x,y))
        return plots_map
    
    def create_regions(self):
        region_map = {key: [] for key in self.plots_map.keys()}
        for plant, plots in self.plots_map.items():
            while plots:
                region = set()
                plot = plots.pop()
                plots.add(plot)
                self.find_connected_regions(region, plots, plot)
                region_map[plant].append(region)
        return region_map

    def get_region_bounds(self, region):
        min_x = self.bounds[0]
        min_y = self.bounds[1]
        max_x = 0
        max_y = 0
        for plot in region:
            min_x = min(plot[0], min_x)
            min_y = min(plot[1], min_y)
            max_x = max(plot[0], max_x)
            max_y = max(plot[1], max_y)
        return (min_x, min_y), (max_x + 1, max_y + 1)

    def find_connected_regions(self, result, plots, plot):
        if not plots:
            return
        elif plot[0] < 0 or plot[0] >= self.bounds[0] or plot[1] < 0 or plot[1] >= self.bounds[1]:
            return

        if plot in plots:
            result.add(plot)
            plots.remove(plot)
        
            self.find_connected_regions(result, plots, (plot[0] - 1, plot[1]))
            self.find_connected_regions(result, plots, (plot[0] + 1, plot[1]))
            self.find_connected_regions(result, plots, (plot[0], plot[1] - 1))
            self.find_connected_regions(result, plots, (plot[0], plot[1] + 1))
    
    def calculate_fencing_price(self):
        offsets = ((-1, 0), (1, 0), (0, -1), (0, 1))
        region_prices = {key: 0 for key in self.regions_map.keys()}
        for plant, regions in self.regions_map.items():
            prices = 0
            for region in regions:
                area = len(region)
                fences = 0
                for plot in region:
                    # Amount of fences = 4 - amount of neighbors
                    fences += 4 - sum([1 for neighbor in ((plot[0] + offset[0], plot[1] + offset[1]) for offset in offsets) if neighbor in region])
                prices += area * fences
            region_prices[plant] = prices
        return sum(region_prices.values())
    
    def calculate_bulk_discounted_fencing_price(self):
        # We are stuck with our datastructure, so let there be pain!
        region_prices = {key: 0 for key in self.regions_map.keys()}
        for plant, regions in self.regions_map.items():
            prices = 0
            for region in regions:
                bounding_box = self.get_region_bounds(region)
                area = len(region)
                fence_segments = 0
                # We run scanlines vertically and horizontally and count the connected segments on either side
                for y in range(bounding_box[0][1], bounding_box[1][1]):
                    runs_top = int_seq_to_ranges([x for x in range(bounding_box[0][0], bounding_box[1][0]) if (x, y) in region and not (x, y - 1) in region])
                    runs_bottom = int_seq_to_ranges([x for x in range(bounding_box[0][0], bounding_box[1][0]) if (x, y) in region and not (x, y + 1) in region])
                    fence_segments += len(runs_top) + len(runs_bottom)
                for x in range(bounding_box[0][0], bounding_box[1][0]):
                    runs_left = int_seq_to_ranges([y for y in range(bounding_box[0][1], bounding_box[1][1]) if (x, y) in region and not (x - 1, y) in region])
                    runs_right = int_seq_to_ranges([y for y in range(bounding_box[0][1], bounding_box[1][1]) if (x, y) in region and not (x + 1, y) in region])
                    fence_segments += len(runs_left) + len(runs_right)
                prices += fence_segments * area
            region_prices[plant] = prices
        return sum(region_prices.values())

def part1(input):
    print("Part 1: The total price of fencing all regions is {}.".format(Gardens(input).calculate_fencing_price()))

def part2(input):
    print("Part 2: The total discounted price of fencing all regions is {}.".format(Gardens(input).calculate_bulk_discounted_fencing_price()))

print('---TEST---')
part1(test_input)
part2(test_input)
with open('input.txt') as f:
    input = f.read()
    print('---INPUT---')
    part1(input)
    part2(input)