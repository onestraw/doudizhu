# -*- coding: utf-8 -*-

import random
from engine import Doudizhu
from card import Card


Doudizhu.init_doudizhu_dict()


def new_game():
    """随机打乱54张牌，分成四组:17,17,17,3"""
    all_cards = []
    for c in Card.STR_RANKS:
        all_cards.extend(Card.card_rank_to_real_card(c))

    all_cards = [Card.new(card_str) for card_str in all_cards]
    random.seed()
    result = []
    for group_idx in range(3):
        group = []
        for card_idx in range(17):
            card = random.choice(all_cards)
            all_cards.remove(card)
            group.append(card)
        result.append(group)

    result.append(all_cards)
    return result


def check_card_type(cards):
    """判断手牌是否符合斗地主规则
    cards: Card类型的列表
    return: bool, type
    """
    cards_no_suit = Card.cards_without_suit(cards)
    return Doudizhu.check_card_type(cards_no_suit)


def cards_greater(cards_x, cards_y):
    """判断手牌cards_x 是否大于cards_y
    cards_x/y: Cards类型的列表
    return: bool, cards_x 的牌型
    """
    cards_x_no_suit = Card.cards_without_suit(cards_x)
    cards_y_no_suit = Card.cards_without_suit(cards_y)
    return Doudizhu.cards_greater(cards_x_no_suit, cards_y_no_suit)
