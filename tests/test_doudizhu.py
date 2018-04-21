import unittest
from doudizhu import Doudizhu


class TestDoudizhu(unittest.TestCase):
    INIT_FLAG = False

    def setUp(self):
        Doudizhu.init_doudizhu_dict()
        self.assertEqual(Doudizhu.TOTAL, 34152)

    def test_list_all_gt_cards(self):
        # cards_target, cards_candidate, expected_result
        test_cases = [
            ('2', '3-K-BJ-CJ', {'solo': ['BJ', 'CJ'], 'rocket': ['BJ-CJ']}),
            ('CJ', '2-2-BJ', {}),
            ('J-Q-Q-Q', '2-2-2-2-3-BJ', {'trio_solo': ['2-2-2-BJ', '3-2-2-2'], 'bomb': ['2-2-2-2']}),
            ('10-10-J-J-Q-Q', 'J-J-Q-Q-K-K-K-K-A-A-A-A', {'pair_chain_3': ['J-J-Q-Q-K-K', 'Q-Q-K-K-A-A'], 'bomb': ['K-K-K-K', 'A-A-A-A']}),
            ('3-4-5-6-7', '3-4-5-6-7-8-9-10-J-Q-K-A-2-BJ-CJ', {'solo_chain_5': ['4-5-6-7-8', '5-6-7-8-9', '6-7-8-9-10', '7-8-9-10-J', '8-9-10-J-Q', '9-10-J-Q-K', '10-J-Q-K-A'], 'rocket': ['BJ-CJ']}),
            ('3-3-3-3-2-2-2-2', '5-5-5-5-6-6-6-6', {'bomb': ['5-5-5-5', '6-6-6-6']}),
            ('7-7-7-8-8-8-9-9-9-10-10-10', 'J-J-J-Q-Q-Q-K-K-K-A-A-A-3-3-3-Q-3', {'trio_chain_4': ['J-J-J-Q-Q-Q-K-K-K-A-A-A'], 'bomb': ['3-3-3-3', 'Q-Q-Q-Q'], 'trio_solo_chain_3': ['J-J-J-Q-Q-Q-K-K-K-A-A-A', '3-J-J-J-Q-Q-Q-K-K-K-A-A', '3-3-J-J-J-Q-Q-Q-K-K-K-A', '3-3-3-J-J-J-Q-Q-Q-K-K-K', '3-J-J-Q-Q-Q-K-K-K-A-A-A', '3-3-J-Q-Q-Q-K-K-K-A-A-A', '3-3-3-Q-Q-Q-K-K-K-A-A-A']}),
            ('3-4-5-6-7', '3-4-5-6-7-9', {}),
            ('3-4-5-6', '3-4-5-6-7-9', {}),
        ]
        for case in test_cases:
            cards_target, cards_candidate, exp = case
            result = Doudizhu.list_greater_cards(cards_target,
                                                 cards_candidate)
            print case, '--', result
            self.assertEqual(result, exp)
            print '#'*20

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
