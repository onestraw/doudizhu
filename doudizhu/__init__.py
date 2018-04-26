# -*- coding: utf-8 -*-

import random
from .engine import Doudizhu
from .card import Card


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
    result = [Card.sort_cards_by_rank_int(cards) for cards in result]
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


def list_greater_cards(cards_target, cards_candidate):
    """ 对于目标牌组合cards_target
    从候选牌cards_candidate中找出所有可以压制它的牌型
    不区分花色，返回结果是一个字典{card_type:[greater_cards,],}
    """
    ct_no_suit = Card.cards_without_suit(cards_target)
    cc_no_suit = Card.cards_without_suit(cards_candidate)
    cards_gt = Doudizhu.list_greater_cards(ct_no_suit, cc_no_suit)

    def render_suit(cards, candidate):
        result = set()
        candidate = set(candidate)
        for card in cards.split('-'):
            cards_suit = [Card.new(cs) for cs in
                          Card.card_rank_to_real_card(card)]
            for card_int in cards_suit:
                if card_int in candidate and card_int not in result:
                    result.add(card_int)
                    break
        return result

    result = {}
    for card_type, cards_list in iter(cards_gt.items()):
        result[card_type] = []
        for cards in cards_list:
            cards_with_suit = render_suit(cards, cards_candidate)
            sorted_cards = Card.sort_cards_by_rank_int(list(cards_with_suit))
            result[card_type].append(sorted_cards)

    return result


__all__ = ['Card', 'new_game', 'check_card_type',
           'cards_greater', 'list_greater_cards']
