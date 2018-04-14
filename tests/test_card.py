import unittest
from doudizhu import Card


class TestCard(unittest.TestCase):
    def test_cards_without_suit(self):
        test_cards = [
            Card.new('3s'),
            Card.new('3h'),
            Card.new('3d'),
            Card.new('3c'),
            Card.new('10c'),
            Card.new('10d'),
            Card.new('10h'),
            Card.new('10s'),
            Card.new('BJ'),
            Card.new('CJ'),
        ]

        ret = Card.cards_without_suit(test_cards)
        self.assertEqual(ret, '3-3-3-3-10-10-10-10-BJ-CJ')


if __name__ == '__main__':
    unittest.main()
