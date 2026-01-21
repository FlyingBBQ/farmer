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


def multi_poly(entity):
    def get_drone_positions():
        drone_positions = []
        world_size = get_world_size()
        space = 8
        offset = space // 2
        positions = world_size // space

        for i in range(positions):
            for j in range(positions):
                x = offset + (i * space)
                y = offset + (j * space)
                drone_positions.append((x, y))
        return drone_positions

    def start_drone_at(entity, x, y):
        def task():
            util.goto(x, y)
            farming.polyculture3(entity)
        return task

    drone_positions = get_drone_positions()
    for x, y in drone_positions:
        spawn_drone(start_drone_at(entity, x, y))


def main():
    change_hat(Hats.Wizard_Hat)
    util.goto(0, 0)

    multi_poly(Entities.Carrot)
    
    # def drone_poly(entity):
    #     def redirect():
    #         for _ in range(get_pos_x() % 2):
    #             move(North)
    #         while True:
    #             farming.polyculture4(entity)
    #     return redirect
    #
    # for x in range(get_world_size() - 1):
    #     #spawn_drone(drone_poly(Entities.Carrot))
    #     spawn_drone(farming.grass2)
    #     move(East)

    # while True:
    #     farming.polyculture4(Entities.Tree)



main()
