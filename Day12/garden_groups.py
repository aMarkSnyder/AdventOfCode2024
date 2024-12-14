from argparse import ArgumentParser
from dataclasses import dataclass
from collections import defaultdict

def neighbors(loc):
    directions = [(1,0),(-1,0),(0,1),(0,-1)]
    neighbors = []
    for direction in directions:
        neighbors.append((loc[0]+direction[0], loc[1]+direction[1]))
    return neighbors

@dataclass
class Region:
    id: int
    plant: str
    plots: set

    def area(self):
        return len(self.plots)
    
    def perimeter(self):
        total = 0
        for plot in self.plots:
            for neighbor in neighbors(plot):
                if neighbor not in self.plots:
                    total += 1
        return total
    
    def price(self):
        return self.area() * self.perimeter()
    
    def perimeter_plots(self):
        internal_pplots = defaultdict(int)
        external_pplots = defaultdict(int)
        for plot in self.plots:
            for neighbor in neighbors(plot):
                if neighbor not in self.plots:
                    internal_pplots[plot] += 1
                    external_pplots[neighbor] += 1
        return internal_pplots, external_pplots

    def sides(self):
        internal_pplots, external_pplots = self.perimeter_plots()

        sides = 0
        for plot, count in internal_pplots.items():
            # this region is a single plot
            if count == 4:
                sides += 4
            # this plot has a one-long side on one edge and a set of parallel sides on the other two
            # it'll take responsibility for one of the parallel sides
            elif count == 3:
                sides += 2
            # this plot could either be a convex corner or in the middle of two parallel sides
            # if it's in the middle of two parallel sides, the ends will take responsibility
            elif count == 2:
                top = (plot[0]-1,plot[1])
                bottom = (plot[0]+1,plot[1])
                # this plot is a corner and will take responsibility for one of its sides
                if (top in self.plots) ^ (bottom in self.plots):
                    sides += 1

        for plot, count in external_pplots.items():
            # this region has a one-plot hole in it
            if count == 4:
                sides += 4
            # this external plot is at the end of a tunnel into the region, with a one-long side at the end
            # and two parallel sides of the tunnel. it'll take responsibility for one of the parallel sides
            elif count == 3:
                sides += 2
            # this external plot could either touch a concave corner or be in between two parallel sides
            # if it's in the middle of two parallel sides, the ends will take responsibility
            elif count == 2:
                top = (plot[0]-1,plot[1])
                bottom = (plot[0]+1,plot[1])
                # this plot is a corner and will take responsibility for one of its sides
                if (top in self.plots) ^ (bottom in self.plots):
                    sides += 1

        # if one region borders on two different areas that touch each other diagonally, the one region will have two spots
        # that are treated as both concave and convex corners by the previous logic. An additional side will erroneously be added for each of the spots.
        # we can correct for this by detecting when those "x" patterns occur.
        x_correction = 0
        for plot, count in internal_pplots.items():
            if (plot[0]+1,plot[1]+1) in self.plots:
                if (plot[0]+1,plot[1]) not in self.plots and (plot[0],plot[1]+1) not in self.plots:
                    x_correction += 2
            if (plot[0]+1,plot[1]-1) in self.plots:
                if (plot[0]+1,plot[1]) not in self.plots and (plot[0],plot[1]-1) not in self.plots:
                    x_correction += 2

        return sides - x_correction

    def price2(self):
        return self.area() * self.sides()


def main(data):
    plots = {}
    for row_idx, row in enumerate(data):
        for col_idx, val in enumerate(row):
            plots[(row_idx, col_idx)] = val

    regions = []
    region_id = 0
    for loc, val in plots.items():
        if any(loc in region.plots for region in regions):
            continue

        new_region_plots = {loc}
        plant = val
        plots_to_check = neighbors(loc)
        while plots_to_check:
            curr_plot = plots_to_check.pop()
            if curr_plot in plots and plots[curr_plot] == plant and curr_plot not in new_region_plots:
                new_region_plots.add(curr_plot)
                plots_to_check.extend(neighbors(curr_plot))

        regions.append(Region(region_id, plant, new_region_plots))
        region_id += 1

    print(sum(region.price() for region in regions))
    print(sum(region.price2() for region in regions))

def read_input(input_file):
    data = []
    with open(input_file, 'r') as input:
        for line in input:
            data.append(line.strip())
    return data

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('input_file', nargs='?', default='input.txt')
    args = parser.parse_args()
    data = read_input(args.input_file)
    main(data)
