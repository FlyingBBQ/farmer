import util

def till_entity(entity):
    needs_soil = {Entities.Pumpkin, Entities.Carrot}
    should_be_soil = (entity in needs_soil)
    is_soil = (get_ground_type() == Grounds.Soil)

    if should_be_soil != is_soil:
        till()

def harvest_plant(type):
    if can_harvest():
        harvest()
    if get_entity_type() == None:
        till_entity()
        plant(type)

def get_item_yield(item):
    start_amount = num_items(item)
    entity = util.item_to_entity(item)
    till_entity(entity)
    plant(entity)
    while not can_harvest():
        pass
    harvest()
    return num_items(item) - start_amount

def grass():
    harvest_plant(Entities.Grass)

def wood():
    if (get_pos_y() + get_pos_x()) % 2 == 0:
        harvest_plant(Entities.Bush)
    else:
        harvest_plant(Entities.Tree)

def carrot():
    harvest_plant(Entities.Carrot)

def pumpkin():
    if get_entity_type() == Entities.Dead_Pumpkin:
        plant(Entities.Pumpkin)
    elif get_ground_type() == Grounds.Soil and get_entity_type() != Entities.Pumpkin:
        plant(Entities.Pumpkin)
    else:
        harvest_plant(Entities.Pumpkin)

def pumpkin_all():
    world_size = 8
    for x in range(world_size):
        for y in range(world_size):
            if can_harvest():
                harvest()
                if get_ground_type() != Grounds.Soil:
                    till()
                plant(Entities.Pumpkin)
            move(North)
        move(East)

    for i in range(2):
        for x in range(world_size):
            for y in range(world_size):
                if get_entity_type() == Entities.Dead_Pumpkin:
                    plant(Entities.Pumpkin)
                move(North)
            move(East)

