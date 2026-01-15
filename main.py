#clear()

import farming
import util


def farm_lowest_item():
    util.goto(0, 0)
    lowest_item = util.get_lowest_item()
    func = farming.item_to_grow(lowest_item)
    func()


def farm_mazes():
    util.spawn_maze()
    for _ in range(max_drones()):
        spawn_drone(util.solve_maze_loop)


def main():
    change_hat(Hats.Wizard_Hat)
    farm_mazes()


main()
