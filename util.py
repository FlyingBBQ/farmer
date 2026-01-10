def create_tile_list(initial_value):
    tile_list = []
    world_size = get_world_size()
    for i in range(world_size):
        tile_list.append([])
        for j in range(world_size):
            tile_list[i].append(initial_value)
    return tile_list

def goto(x, y):
    diff_x = x - get_pos_x()
    diff_y = y - get_pos_y()

    half_world = (get_world_size() / 2)
    flip = {West: East, East: West, South: North, North: South}

    dir_x = West
    if diff_x > 0:
        dir_x = East
    if abs(diff_x) > half_world:
        dir_x = flip[dir_x]

    dir_y = South
    if diff_y > 0:
        dir_y = North
    if abs(diff_y) > half_world:
        dir_y = flip[dir_y]

    while x != get_pos_x():
        move(dir_x)
    while y != get_pos_y():
        move(dir_y)

def get_item_totals():
    return {
        "Items.Hay": num_items(Items.Hay),
        "Items.Wood": num_items(Items.Wood),
        "Items.Carrot": num_items(Items.Carrot),
        "Items.Pumpkin": num_items(Items.Pumpkin),
        "Items.Water": num_items(Items.Water),
        "Items.Fertilizer": num_items(Items.Fertilizer),
    }

def item_to_entity(item):
    convert = {
        Items.Carrot: Entities.Carrot,
        Items.Hay: Entities.Grass,
        Items.Pumpkin: Entities.Pumpkin,
        Items.Power: Entities.Sunflower,
        Items.Wood: Entities.Tree,
    }
    return convert[item]

def get_item_cost(relation_dict, entity, weight):
    entity_cost = get_cost(entity)
    for item in entity_cost:
        cost = entity_cost[item] * weight
        relation_dict[item] = cost
        get_item_cost(relation_dict, item_to_entity(item), cost)
    return relation_dict

