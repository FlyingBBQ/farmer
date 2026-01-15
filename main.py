#clear()

import farming
import util


def main():
    change_hat(Hats.Wizard_Hat)
    while True:
        util.goto(0, 0)
        lowest_item = util.get_lowest_item()
        func = farming.item_to_grow(lowest_item)
        func()


main()
