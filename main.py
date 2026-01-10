clear()

import plant
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
    relation_dict = {Items.Pumpkin: 1}
    relation_dict = util.get_item_cost(relation_dict, Entities.Pumpkin, 1)
    print(relation_dict)

    #print(util.get_item_yield(Items.Hay))
    #print(util.get_item_yield(Items.Wood))
    print(util.get_item_yield(Items.Carrot))


main()
