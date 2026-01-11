def create_tile_list(initial_value):
    tile_list = []
    world_size = get_world_size()
    for i in range(world_size):
        tile_list.append([])
        for j in range(world_size):
            tile_list[i].append(initial_value)
    return tile_list


def flip_direction(dir):
    flip = {West: East, East: West, South: North, North: South}
    return flip[dir]


def goto(x, y):
    diff_x = x - get_pos_x()
    diff_y = y - get_pos_y()

    half_world = (get_world_size() / 2)

    dir_x = West
    if diff_x > 0:
        dir_x = East
    if abs(diff_x) > half_world:
        dir_x = flip_direction[dir_x]

    dir_y = South
    if diff_y > 0:
        dir_y = North
    if abs(diff_y) > half_world:
        dir_y = flip_direction[dir_y]

    while x != get_pos_x():
        move(dir_x)
    while y != get_pos_y():
        move(dir_y)


def get_item_totals():
    return {
        Items.Hay: num_items(Items.Hay),
        Items.Wood: num_items(Items.Wood),
        Items.Carrot: num_items(Items.Carrot),
        Items.Pumpkin: num_items(Items.Pumpkin),
        Items.Water: num_items(Items.Water),
        Items.Fertilizer: num_items(Items.Fertilizer),
    }


def get_lowest_item():
    items = {
        Items.Hay, 
        Items.Wood,
        Items.Carrot,
        Items.Pumpkin,
    }
    values = {}
    for key in items:
        values[num_items(key)] = key
    return values[min(values)]


def item_to_entity(item):
    convert = {
        Items.Carrot: Entities.Carrot,
        Items.Hay: Entities.Grass,
        Items.Power: Entities.Sunflower,
        Items.Pumpkin: Entities.Pumpkin,
        Items.Wood: Entities.Tree, # or bush
    }
    return convert[item]


def entity_to_item(entity):
    convert = {
        Entities.Bush: Items.Wood,
        Entities.Carrot: Items.Carrot,
        Entities.Grass: Items.Hay,
        Entities.Pumpkin: Items.Pumpkin,
        Entities.Sunflower: Items.Power,
        Entities.Tree: Items.Wood,
    }
    return convert[entity]


def get_item_cost(relation_dict, entity, weight):
    # Example:
    # relation_dict = {Items.Pumpkin: 1}
    # relation_dict = util.get_item_cost(relation_dict, Entities.Pumpkin, 1)
    entity_cost = get_cost(entity)
    for item in entity_cost:
        cost = entity_cost[item] * weight
        relation_dict[item] = cost
        get_item_cost(relation_dict, item_to_entity(item), cost)
    return relation_dict


