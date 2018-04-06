import unittest
from doudizhu import Doudizhu, sort_cards, cards2str, str2cards


class TestDoudizhu(unittest.TestCase):
    INIT_FLAG = False

    def setUp(self):
        Doudizhu.init_doudizhu_dict()
        self.assertEqual(Doudizhu.TOTAL, 34152)

    def test_sort_cards(self):
        cards = '3-4-5-6-7-8-9-10-J-Q-K-A-2-BJ-CJ'
        reverse_cards = str2cards(cards)[::-1]
        rst = sort_cards(reverse_cards)
        self.assertEqual(cards2str(rst), cards)

    def test_compare_cards(self):
        # cards_x, cards_y, expected_result
        test_cases = [
            ('2', 'K', True),
            ('CJ', 'BJ', True),
            ('4-5-6-7-8', '3-4-5-6-7', True),

            ('A-A', 'K-K', True),
            ('Q-Q-K-K-A-A', 'J-J-Q-Q-K-K', True),
            ('A-A-Q-Q-K-K', 'J-J-10-10-9-9', True),

            ('9-9-9-2-2', 'A-A-8-8-8', True),

            ('8-8-8-9-9-9-BJ-CJ', '3-3-3-4-4-4-K-K', True),
            ('8-8-8-9-9-9-10-10-10-J-J-J', '3-3-3-4-4-4-5-5-5-K-K-K', True),
            ('8-8-8-9-9-9-10-10-10-J-J-J-2-2-2-2',
             '3-3-3-4-4-4-5-5-5-6-6-6-K-K-K-K', True),
            ('8-8-8-9-9-9-10-10-10-J-J-J-Q-Q-Q-A-2-2-2-2',
             '3-3-3-4-4-4-5-5-5-6-6-6-7-7-7-Q-K-K-K-K', True),

            ('7-7-7-8-8-8-A-A-A-A', '3-3-3-4-4-4-K-K-K-K', True),
            ('7-7-7-8-8-8-9-9-9-A-A-A-A-2-2',
             '3-3-3-4-4-4-5-5-5-Q-Q-K-K-K-K', True),
            ('7-7-7-8-8-8-9-9-9-10-10-10-A-A-A-A-2-2-2-2',
             '3-3-3-4-4-4-5-5-5-6-6-6-Q-Q-Q-Q-K-K-K-K', True),

            ('Q-Q-Q-Q-J-J', '9-9-9-9-BJ-CJ', True),
            ('3-3-3-3-J-J-J-J', '9-9-9-9-8-8-8-8', True),

            ('3-3-3-3', '7-7-7-8-8-8-9-9-9-10-10-10-A-A-A-A-2-2-2-2', True),
            ('3-3-3-3', '2-2-2-2-BJ-CJ', True),
            ('BJ-CJ', '2-2-2-2', True),

            # false
            ('3', 'CJ', False),
            ('2-2', '2', False),
            ('2-2', 'A-A-A', False),
        ]
        for case in test_cases:
            cards_x, cards_y, exp = case
            result = Doudizhu.cards_greater(cards_x, cards_y)
            print case, result
            self.assertEqual(result[0], exp)

    def test_valid_card_type(self):
        # cards, expected_result
        test_cases = [
            ('3', True),
            ('2', True),
            ('CJ', True),
            ('4-5-6-7-8', True),
            ('8-4-5-6-7', True),

            ('4-5-6-7', False),
            ('2-3-4-5-6', False),
            ('3-4-5-6-8', False),

            ('A-A', True),
            ('A-A-Q-Q-K-K', True),

            ('Q-Q-K-K', False),
            ('A-A-2-2-3-3', False),
            ('2-2-A-A-K-K', False),

            ('9-9-9-BJ-CJ', False),
            ('9-9-9-2-2', True),
            ('8-8-8-9-9-9-BJ-CJ', True),
            ('3-3-3-4-4-4-5-5-5-K-K-K', True),
            ('3-3-3-4-4-4-5-5-5-6-6-6-K-K-K-K', True),
            ('3-3-3-4-4-4-5-5-5-6-6-6-7-7-7-Q-K-K-K-K', True),
            ('3-3-3-4-4-4-K-K-K-K', True),
            ('3-3-3-4-4-4-5-5-5-Q-Q-K-K-K-K', True),
            ('3-3-3-4-4-4-5-5-5-6-6-6-Q-Q-Q-Q-K-K-K-K', True),

            ('2-2-2-2-BJ-CJ', True),
            ('Q-Q-Q-Q-J-J', True),
            ('3-3-3-3-J-J-J-J', True),
            ('9-9-9-9', True),
            ('BJ-CJ', True),
        ]
        for case in test_cases:
            cards, exp = case
            result = Doudizhu.check_card_type(cards)
            print case, result
            self.assertEqual(result[0], exp)
