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
    half_world = (get_world_size() / 2)

    def direction(diff, negative, positive):
        dir = negative
        if diff > 0:
            dir = positive
        if abs(diff) > half_world:
            dir = flip_direction(dir)
        return dir
    
    dir_x = direction(x - get_pos_x(), West, East)
    dir_y = direction(y - get_pos_y(), South, North)

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
        Items.Cactus: num_items(Items.Cactus),
    }


def get_lowest_item():
    # Check special items first
    if num_items(Items.Power) < 5000:
        return Items.Power

    # Check resources and get the minimal
    items = {
        Items.Cactus,
        Items.Carrot,
        Items.Hay, 
        Items.Pumpkin,
        Items.Wood,
    }
    values = {}
    for key in items:
        values[num_items(key)] = key
    return values[min(values)]


def item_to_entity(item):
    convert = {
        Items.Cactus: Entities.Cactus,
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
        Entities.Cactus: Items.Cactus,
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


def sort(direction):
    world_size = get_world_size()
    inverse_direction = flip_direction(direction)
    sorted_length = 1
    move(direction)

    while sorted_length < world_size:
        traverse_back = sorted_length

        while (traverse_back > 0) and (measure(inverse_direction) > measure()):
            swap(inverse_direction)
            move(inverse_direction)
            traverse_back -= 1

        sorted_length += 1
        for _ in range(sorted_length - traverse_back):
            move(direction)


def spawn_maze():
    harvest()
    plant(Entities.Bush)
    substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
    use_item(Items.Weird_Substance, substance)


def solve_maze():
    directions = [North, East, South, West]
    index = 0

    def turn_right(index):
        return (index + 1) % 4

    def turn_left(index):
        return (index - 1) % 4

    # Solve the maze by following the left wall
    while get_entity_type() != Entities.Treasure:
        # Turn left if there is no wall on the left hand side
        if can_move(directions[turn_left(index)]):
            index = turn_left(index)
        # If there is a wall in front of us turn right
        if not can_move(directions[index]):
            index = turn_right(index)
        else:
            # Otherwise we move forward
            move(directions[index])

    # The treasure has been found!
    harvest()


def solve_maze_loop():
    while True:
        solve_maze()
        spawn_maze()

