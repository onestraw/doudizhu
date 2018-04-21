import unittest

import doudizhu
from doudizhu import Card


def CardStrListToCardIntSet(cards):
        return set([Card.new(card_str) for card_str in cards])


def CardStrListToCardIntList(cards):
        return [Card.new(card_str) for card_str in cards]


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

    def test_doudizhu_list_greater_cards(self):
        cards_target = CardStrListToCardIntList(
            ['6c', '6d', '6h', '6s', '8h', '8s'])
        cards_candidate = CardStrListToCardIntList(
            ['5c', '5d', '5h', '5s', '9h', '9s', '9c', '9d', 'BJ', 'CJ'])
        exp = {'bomb': [CardStrListToCardIntSet(['5c', '5d', '5h', '5s']),
                        CardStrListToCardIntSet(['9c', '9d', '9h', '9s'])],
               'rocket': [CardStrListToCardIntSet(['BJ', 'CJ'])],
               'four_two_solo': [CardStrListToCardIntSet(['9h', '9s', '9c', '9d', 'BJ', 'CJ']),
                                 CardStrListToCardIntSet(['9h', '9s', '9c', '9d', 'CJ', '5h']),
                                 CardStrListToCardIntSet(['9h', '9s', '9c', '9d', 'BJ', '5h']),
                                 CardStrListToCardIntSet(['9h', '9s', '9c', '9d', '5s', '5h'])]}
        ret = doudizhu.list_greater_cards(cards_target, cards_candidate)
        # print exp, ret
        for card_type, cards_list in ret.iteritems():
            ret[card_type] = [set(cards) for cards in cards_list]

        self.assertTrue(cmp(ret, exp) == 0)

        cards_target = CardStrListToCardIntList(['Js', 'Qh', 'Qd', 'Qc'])
        cards_candidate = CardStrListToCardIntList(['2h', '2s', '2d', '2c', '3d', 'BJ'])
        exp = {'bomb': [CardStrListToCardIntSet(['2h', '2s', '2d', '2c'])],
               'trio_solo': [
                   CardStrListToCardIntSet(['2h', '2s', '2c', 'BJ']),
                   CardStrListToCardIntSet(['3d', '2h', '2s', '2c']),
                   ]
               }
        ret = doudizhu.list_greater_cards(cards_target, cards_candidate)
        for card_type, cards_list in ret.iteritems():
            ret[card_type] = [set(cards) for cards in cards_list]
        self.assertTrue(cmp(ret, exp) == 0)
