from main import to_grid, tick, show_grid


def test_transformations():
    grid = (
        "#.##.##.##\n"
        "#######.##\n"
        "#.#.#..#..\n"
        "####.##.##\n"
        "#.##.##.##\n"
        "#.#####.##\n"
        "..#.#.....\n"
        "##########\n"
        "#.######.#\n"
        "#.#####.##"
    )

    expected_output = (
        "#.LL.L#.##\n"
        "#LLLLLL.L#\n"
        "L.L.L..L..\n"
        "#LLL.LL.L#\n"
        "#.LL.LL.LL\n"
        "#.LLLL#.##\n"
        "..L.L.....\n"
        "#LLLLLLLL#\n"
        "#.LLLLLL.L\n"
        "#.#LLLL.##"
    )
    grid = to_grid(grid)
    expected_grid = to_grid(expected_output)
    new_grid = tick(grid)
    show_grid(expected_grid)
    show_grid(new_grid)
    assert new_grid == expected_grid
