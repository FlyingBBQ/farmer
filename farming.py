import util

def till_entity(entity):
    needs_soil = {Entities.Pumpkin, Entities.Carrot, Entities.Sunflower}
    should_be_soil = (entity in needs_soil)
    is_soil = (get_ground_type() == Grounds.Soil)

    if should_be_soil != is_soil:
        till()


def grow(entity):
    if can_harvest():
        harvest()
    type = get_entity_type()
    if (type == None) or (type == Entities.Dead_Pumpkin) or (type == Entities.Grass):
        till_entity(entity)
        plant(entity)


def get_entity_yield(entity):
    item = util.entity_to_item(entity)
    start_amount = num_items(item)
    till_entity(entity)
    plant(entity)
    while not can_harvest():
        pass
    harvest()
    return num_items(item) - start_amount


def default_yield(update):
    default = {
        Entities.Bush: 80,
        Entities.Carrot: 80,
        Entities.Grass: 16,
        Entities.Pumpkin: 4, # multiply * 6
        Entities.Sunflower: 1,
        Entities.Tree: 400,
    }
    if update:
        for ent in default:
            default[ent] = get_entity_yield(ent)
    return default


def grass():
    grow(Entities.Grass)


def wood():
    if (get_pos_y() + get_pos_x()) % 2 == 0:
        grow(Entities.Bush)
    else:
        grow(Entities.Tree)


def carrot():
    grow(Entities.Carrot)


def pumpkin():
    if get_entity_type() == Entities.Dead_Pumpkin:
        plant(Entities.Pumpkin)
    elif (get_ground_type() == Grounds.Soil) and (get_entity_type() != Entities.Pumpkin):
        plant(Entities.Pumpkin)
    else:
        grow(Entities.Pumpkin)


def power():
    pass


def item_to_grow(item):
    convert = {
        Items.Carrot: carrot,
        Items.Hay: grass,
        Items.Power: power,
        Items.Pumpkin: pumpkin,
        Items.Wood: wood,
    }
    return convert[item]


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


def move_and_plant(func):
    world_size = get_world_size()
    for x in range(world_size):
        for y in range(world_size):
            func()
            move(North)
        move(East)
