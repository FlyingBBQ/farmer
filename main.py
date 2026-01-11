from __builtins__ import get_world_size
clear()

import farming
import util

def temp():
    # farm combi
    for _ in range(3):
        world_size = get_world_size()
        for _ in range(world_size):
            for _ in range(world_size):
                pos_x = get_pos_x()
                if pos_x == 0:
                    grass()
                elif pos_x < (world_size / 2):
                    wood()
                else:
                    carrot()
                move(North)
            move(East)

        # farm pumpkin
        #pumpkin_all()


def main():
    change_hat(Hats.Wizard_Hat)
    while True:
        lowest_item = util.get_lowest_item()
        func = farming.item_to_grow(lowest_item)
        farming.move_and_plant(func)


main()
