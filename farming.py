import util

def till_entity(entity):
    needs_soil = {
        Entities.Pumpkin,
        Entities.Carrot,
        Entities.Sunflower,
        Entities.Cactus,
    }
    should_be_soil = (entity in needs_soil)
    is_soil = (get_ground_type() == Grounds.Soil)

    if should_be_soil != is_soil:
        till()


def grow(entity, water_level=0):
    if can_harvest():
        harvest()
    if get_water() <= water_level:
        use_item(Items.Water)
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
        Entities.Cactus: 1,
        Entities.Grass: 16,
        Entities.Pumpkin: 4, # multiply * 6
        Entities.Sunflower: 1,
        Entities.Tree: 400,
    }
    if update:
        for ent in default:
            default[ent] = get_entity_yield(ent)
    return default


def item_to_grow(item):
    convert = {
        Items.Carrot: carrot,
        Items.Hay: grass,
        Items.Power: power,
        Items.Pumpkin: pumpkin,
        Items.Wood: wood,
        Items.Cactus: cactus,
    }
    return convert[item]


def grass():
    polyculture(Entities.Grass)


def carrot():
    polyculture(Entities.Carrot)


def wood():
    # Wood is a special case since it can be bush or tree
    polyculture("wood")


def polyculture(entity):
    companions = {}
    world_size = get_world_size()

    for _ in range(world_size):
        x = get_pos_x()
        for _ in range(world_size):
            y = get_pos_y()
            # First, check if need to plant a companion on this position
            if (x, y) in companions:
                grow(companions[(x, y)])
                companions.pop((x, y))
            else:
                # Otherwise, we grow our resource
                if entity == "wood":
                    if (x + y) % 2 == 0:
                        grow(Entities.Bush)
                    else:
                        grow(Entities.Tree)
                else:
                    grow(entity)

                # And check if this resource has a companion
                plant_type, (xx, yy) = get_companion()
                if plant_type:
                    companions[(xx, yy)] = plant_type

            move(North)
        move(East)


def pumpkin():
    util.goto(0, 0)
    # Farm pumpkins in multiple cycles
    # 1. First loop, plant
    plant_one_field(grow, Entities.Pumpkin)

    # 2. Second loop, check pumpkins and create list.
    replaced_pumpkins = []
    world_size = get_world_size()
    for x in range(world_size):
        for y in range(world_size):
            ent = get_entity_type()
            if ent == Entities.Dead_Pumpkin:
                plant(Entities.Pumpkin)
                replaced_pumpkins.append((get_pos_x(), get_pos_y()))
            elif ent != Entities.Pumpkin:
                harvest()
                plant(Entities.Pumpkin)
                replaced_pumpkins.append((get_pos_x(), get_pos_y()))
            move(North)
        move(East)

    # 3. Only check the replaced pumpkins
    while len(replaced_pumpkins) > 0:
        # Iterate over copy of list to prevent index shifting after removing elements
        for pos in replaced_pumpkins[:]:
            util.goto(pos[0], pos[1])
            if get_entity_type() == Entities.Dead_Pumpkin:
                plant(Entities.Pumpkin)
            if can_harvest():
                replaced_pumpkins.remove(pos)

    # Harvest one big pumpkin
    harvest()


# Use a global to share state between spawn_drone()
power_level = 15
def power():
    util.goto(0, 0)
    world_size = get_world_size()

    def plant_power():
        plant_one_lane(grow, Entities.Sunflower, 0.6, North)

    for x in range(world_size):
        spawn_drone(plant_power)
        move(East)

    while num_drones() > 1:
        pass

    def harvest_power():
        # power_level is 'read-only'
        global power_level
        for x in range(get_world_size()):
            if power_level == measure():
                while not can_harvest():
                    pass
                harvest()
            move(North)

    global power_level
    power_level = 15
    while power_level >= 7:
        for x in range(world_size):
            spawn_drone(harvest_power)
            move(East)
        # Decrement the global power level
        power_level -= 1


def cactus():
    util.goto(0, 0)
    plant_one_field(grow, Entities.Cactus)

    # Rows
    util.goto(0, 0)
    for _ in range(get_world_size()):
        util.sort(East)
        move(North)

    # Columns
    util.goto(0, 0)
    for _ in range(get_world_size()):
        util.sort(North)
        move(East)

    harvest()


def plant_one_lane(func, arg1, arg2, direction):
    for x in range(get_world_size()):
        func(arg1, arg2)
        move(direction)


def plant_one_field(func, args):
    world_size = get_world_size()
    for x in range(world_size):
        for y in range(world_size):
            func(args)
            if y % 3 == 1:
                use_item(Items.Fertilizer)
            move(North)
        move(East)
