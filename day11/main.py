import os
from typing import List, Literal


BASE_DIR = os.path.dirname(__file__)

EMPTY_SEAT = "L"
OCCUPIED_SEAT = "#"
FLOOR = "."

Chars = Literal[EMPTY_SEAT, OCCUPIED_SEAT, FLOOR]
SeatGrid = List[List[Chars]]

OccupiedSeatCount = int
OccupancyGrid = List[List[OccupiedSeatCount]]


def count_adjacent_occupied_seats(row: int, col: int, grid: SeatGrid):
    count = 0
    for r in (row - 1, row, row + 1):
        for c in (col - 1, col, col + 1):
            if r == row and c == col:
                continue

            row_out_of_grid = not r in range(0, len(grid))
            col_out_of_grid = not c in range(0, len(grid))

            if row_out_of_grid or col_out_of_grid:
                continue

            if grid[r][c] == OCCUPIED_SEAT:
                count += 1
    return count

def count_visible_occupied_seats(row: int, col: int, grid: SeatGrid):
    count = 0

def to_occupancy_grid(grid: SeatGrid) -> OccupancyGrid:
    occupied_seat_grid = []
    for row in range(len(grid)):
        occupied_seat_row = []
        for col in range(len(grid[row])):
            count = count_adjacent_occupied_seats(row, col, grid)
            occupied_seat_row.append(count)
        occupied_seat_grid.append(occupied_seat_row)
    return occupied_seat_grid


def to_grid(data: str) -> SeatGrid:
    return [list(seat_row) for seat_row in data.split("\n")]


def transform_floor(adjacent_occupied_seat_count):
    return FLOOR


def transform_occupied_seat(adjacent_occupied_seat_count):
    if adjacent_occupied_seat_count >= 4:
        return EMPTY_SEAT
    return OCCUPIED_SEAT


def transform_empty_seat(adjacent_occupied_seat_count):
    if adjacent_occupied_seat_count == 0:
        return OCCUPIED_SEAT
    return EMPTY_SEAT


def count_occupied_seats(grid: SeatGrid):
    def is_occupied(seat):
        return seat == OCCUPIED_SEAT

    count = 0
    for seat_row in grid:
        count += sum((1 for seat in filter(is_occupied, seat_row)))

    return count


transformations = {
    FLOOR: transform_floor,
    EMPTY_SEAT: transform_empty_seat,
    OCCUPIED_SEAT: transform_occupied_seat,
}


def tick(grid: SeatGrid):
    occupancy_grid = to_occupancy_grid(grid)
    new_grid = []
    for seat_row, occupancy_row in zip(grid, occupancy_grid):
        new_row = []
        for seat, occupancy_count in zip(seat_row, occupancy_row):
            new_row.append(transformations[seat](occupancy_count))
        new_grid.append(new_row)
    return new_grid


def show_grid(grid: SeatGrid):
    print("\n".join(map(lambda row: "".join(row), grid)))


def stabilize_grid(grid: SeatGrid):
    new_grid = tick(grid)
    if new_grid == grid:
        return grid
    return stabilize_grid(new_grid)


with open(os.path.join(BASE_DIR, "data.in"), "r") as fp:
    grid = to_grid(fp.read())
    stabilized_grid = stabilize_grid(grid)
    count_1 = count_occupied_seats(stabilized_grid)
    print("Task 1 count:", count_1)