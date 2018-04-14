import unittest

import doudizhu
from doudizhu import Card


class TestDoudizhuGame(unittest.TestCase):
    def test_doudizhu_new_game(self):
        cards_group = doudizhu.new_game()
        self.assertEqual(len(cards_group[0]), 17)
        self.assertEqual(len(cards_group[1]), 17)
        self.assertEqual(len(cards_group[2]), 17)
        self.assertEqual(len(cards_group[3]), 3)

        total = sum([len(cg) for cg in cards_group])
        self.assertEqual(total, 54)

        print ''
        for card_ints in cards_group:
            Card.print_pretty_cards(card_ints)

    def test_doudizhu_check_card_type(self):
        test_cards = [
            Card.new('10c'),
            Card.new('10d'),
            Card.new('10h'),
            Card.new('10s'),
            Card.new('BJ'),
            Card.new('CJ'),
        ]

        ret = doudizhu.check_card_type(test_cards)
        self.assertEqual(ret[0], True)

    def test_doudizhu_greater_cards(self):
        cards_x = [
            Card.new('10c'),
            Card.new('10d'),
            Card.new('10h'),
            Card.new('CJ'),
        ]
        cards_y = [
            Card.new('Kc'),
            Card.new('Kd'),
            Card.new('Kh'),
            Card.new('3s'),
        ]

        ret = doudizhu.cards_greater(cards_x, cards_y)
        self.assertEqual(ret[0], False)
        ret = doudizhu.cards_greater(cards_y, cards_x)
        self.assertEqual(ret[0], True)
