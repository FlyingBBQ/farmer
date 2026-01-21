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


def grass2():
    while True:
        harvest()
        move(North)


def carrot():
    polyculture(Entities.Carrot)


def wood():
    # Wood is a special case since it can be bush or tree
    polyculture("wood")


def polyculture2(entity):
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


# multi drone parallel
polyculture_entity = Entities.Grass
def polyculture(entity):
    util.goto(0, 0)
    world_size = get_world_size()

    global polyculture_entity
    polyculture_entity = entity

    def plant_companion():
        plant_type, (x, y) = get_companion()
        util.goto(x, y)
        if plant_type != get_entity_type():
            grow(plant_type)

    def plant_entity():
        global polyculture_entity
        for _ in range(get_world_size()):
            # Special case for planting wood
            if polyculture_entity == "wood":
                if (get_pos_x() + get_pos_y()) % 2 == 0:
                    grow(Entities.Bush)
                else:
                    if get_water() < 1:
                        use_item(Items.Water)
                    grow(Entities.Tree)
            # All others use the default
            else:
                grow(polyculture_entity)
            # Check if this tile has a companion
            plant_type, (xx, yy) = get_companion()
            if plant_type != polyculture_entity:
                drone = spawn_drone(plant_companion)
                if drone:
                    wait_for(drone)
            move(North)

    step = 8
    for start_pos in range(step):
        for x in range(start_pos, world_size, step):
            while num_drones() > 16:
                pass
            spawn_drone(plant_entity)
            for _ in range(step):
                move(East)


def polyculture3(entity):
    companions = {}

    def plant_companion():
        plant_type, (x, y) = get_companion()
        util.goto(x, y)
        if plant_type != get_entity_type():
            grow(plant_type)

    while True:
        while not can_harvest():
            pass
        grow(entity)
        # Always use water to speed up growth
        if get_water() < 0.95:
            use_item(Items.Water)
        # Check if the companion is already planted
        plant_type, (x, y) = get_companion()
        if ( (x, y) in companions ) and ( companions[(x, y)] == plant_type ):
            continue
        # Update the list and send a drone to plant the companion
        companions[(x, y)] = plant_type
        drone = spawn_drone(plant_companion)
        if drone:
            wait_for(drone)

        # if not can_harvest():
        #     use_item(Items.Fertilizer)



def polyculture4(entity):
    for x in range(get_world_size()):
        grow(entity)

        companion_entity = Entities.Grass
        plant_type = None
        while plant_type != companion_entity:
            plant_type, (x, y) = get_companion()
            if plant_type == companion_entity:
                if ((x % 2) == 1) and ((y % 2) == 0):
                    move(North)
                    move(North)
                elif ((x % 2) == 0) and ((y % 2) == 1):
                    move(North)
                    move(North)
                else:
                    harvest()
                    grow(entity)
            else:
                harvest()
                grow(entity)



def pumpkin():
    util.goto(0, 0)
    world_size = get_world_size()

    def plant_pumpkin():
        check_pumpkins = True
        # Keep looping until all pumpkins are good
        while check_pumpkins:
            check_pumpkins = False
            # Iterate once over the lane
            for x in range(get_world_size()):
                type = get_entity_type()
                # Harvest anything that is not a pumpkin
                if (type != Entities.Pumpkin) and (type != Entities.Dead_Pumpkin):
                    harvest()
                    till_entity(Entities.Pumpkin)
                    plant(Entities.Pumpkin)
                    check_pumpkins = True
                # Replant any dead pumpkin
                elif type == Entities.Dead_Pumpkin:
                    if get_water() < 1:
                        use_item(Items.Water)
                    plant(Entities.Pumpkin)
                    check_pumpkins = True
                # Wait till pumpkins are fully grown
                elif not can_harvest():
                    check_pumpkins = True

                move(North)


    # Spawn a drone for each column to plant pumpkins
    for x in range(world_size - 1):
        spawn_drone(plant_pumpkin)
        move(East)

    # Plant the last row
    plant_pumpkin()

    # Wait for all drones to finish
    while num_drones() > 1:
        pass

    harvest()


# Use a global to share state between spawn_drone()
power_level = 15
def power():
    util.goto(0, 0)
    world_size = get_world_size()

    def plant_sunflower():
        for x in range(get_world_size()):
            grow(Entities.Sunflower, 0.6)
            move(North)

    for x in range(world_size - 1):
        spawn_drone(plant_sunflower)
        move(East)
    plant_sunflower()

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


def plant_one_field(func, args):
    world_size = get_world_size()
    for x in range(world_size):
        for y in range(world_size):
            func(args)
            if y % 3 == 1:
                use_item(Items.Fertilizer)
            move(North)
        move(East)
