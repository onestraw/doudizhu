# -*- coding: utf-8 -*-

"""
斗地主规则检查及比较器
~~~~~~~~~~~~~~~~~~~~~
枚举所有37种牌型，制作一个花色无关、顺序无关的字典，
能够在O(1)时间内判断出牌是否有效，在O(1)时间内比较大小
"""
import itertools
import logging

from doudizhu.compat import is_py3, cmp_to_key

logging.basicConfig(level=logging.INFO)


CARDS = '3-4-5-6-7-8-9-10-J-Q-K-A-2-BJ-CJ'.split('-')
CARD_IDX = {c: w for w, c in enumerate(CARDS)}
CARDS_NO_JOKERS = CARDS[:-2]
CARD_PAIR = [[c] * 2 for c in CARDS_NO_JOKERS]
CARD_TRIO = [[c] * 3 for c in CARDS_NO_JOKERS]
CARD_FOUR = [[c] * 4 for c in CARDS_NO_JOKERS]


def cards2str(cards):
    return '-'.join(cards)


def str2cards(string):
    return string.split('-')


def str2cardmap(string):
    cards = str2cards(string)
    cardmap = {}
    for c in cards:
        if c in cardmap:
            cardmap[c] += 1
        else:
            cardmap[c] = 1
    return cardmap


def sort_cards(cards):
    if is_py3:
        return sorted(cards, key=cmp_to_key(
            lambda x, y: CARD_IDX[x] - CARD_IDX[y]))
    return sorted(cards, cmp=lambda x, y: CARD_IDX[x] - CARD_IDX[y])


def order_repeat(cards, n):
    """按序重复每一个元素n次
    ([a,b,c], 3)
    -->[a,a,a,b,b,b,c,c,c]
    """
    tmp = []
    for c in cards:
        tmp += [c] * n
    return tmp


def put_sorted_cards(result, cards, weight):
    """cards is a list of card
    sort, 2str, append
    """
    result.append((cards2str(sort_cards(cards)), weight))


def enum_solo():
    """枚举所有单牌，并附加权重，以便比较大小"""
    return [(c, w) for w, c in enumerate(CARDS)]


def enum_solo_chain(length):
    """枚举所有单连顺，并附加权重
    length 是连顺的张数，如5连
    """
    if length < 5 or length > 12:
        raise ValueError('chain length is in [5,12]')

    chain_range = [(5, 8), (12, 1)]
    count = chain_range[0][1] - (length - chain_range[0][0])

    def solo_chain_x():
        return [(cards2str(CARDS[i:i + length]), i) for i in range(count)]

    return solo_chain_x


def enum_pair():
    """枚举所有的对子"""
    return [(cards2str(pair), w) for w, pair in enumerate(CARD_PAIR)]


def enum_pair_chain(length):
    """枚举所有的连对"""
    if length < 3 or length > 10:
        raise ValueError('chain length is in [3,10]')

    chain_range = [(3, 10), (10, 3)]
    count = chain_range[0][1] - (length - chain_range[0][0])

    def pair_chain_x():
        solo_chain = [CARDS[i:i + length] for i in range(count)]
        pair_chain = []
        for w, sc in enumerate(solo_chain):
            tmp = []
            for c in sc:
                tmp += [c, c]
            pair_chain.append((cards2str(tmp), w))
        return pair_chain

    return pair_chain_x


def enum_trio_chain(length):
    """枚举所有的三张及连三"""
    if length < 1 or length > 7:
        raise ValueError('chain length is in [1,7]')

    chain_range = [(1, 13), (6, 7)]
    count = chain_range[0][1] - (length - chain_range[0][0])
    if length >= 2:
        # 2连以上不能用`2`
        count -= 1

    def trio_chain_x():
        solo_chain = [CARDS[i:i + length] for i in range(count)]
        trio_chain = []
        for w, sc in enumerate(solo_chain):
            tmp = []
            for c in sc:
                tmp += [c] * 3
            trio_chain.append((cards2str(tmp), w))
        return trio_chain

    return trio_chain_x


def enum_trio_solo():
    """枚举所有的三带一"""
    result = []
    weight = 0
    for trio in CARD_TRIO:
        weight += 1
        all_cards = [card for card in CARDS if card != trio[0]]
        for card in all_cards:
            put_sorted_cards(result, trio + [card], weight)

    logging.debug('trio_solo: {}'.format(len(result)))
    return result


def enum_trio_solo_chain(length):
    """x 连三连一"""
    if length < 2 or length > 5:
        raise ValueError('chain length is in [2,5]')

    def trio_solo_chain_x():
        result = []
        weight = 0
        solo_chain = [CARDS[i:i + length] for i in range(13 - length)]
        for chain in solo_chain:
            weight += 1
            trio_chain = order_repeat(chain, 3)
            avail_cards = [c for c in CARDS_NO_JOKERS if c not in set(chain)]

            # 1. select {BJ, CJ}
            it = itertools.combinations_with_replacement(avail_cards, length - 2)
            for e in it:
                kicker = list(e) + ['BJ', 'CJ']
                put_sorted_cards(result, trio_chain + kicker, weight)
            # 2. select BJ
            it = itertools.combinations_with_replacement(avail_cards, length - 1)
            for e in it:
                kicker = list(e) + ['BJ']
                put_sorted_cards(result, trio_chain + kicker, weight)
            # 3. select CJ
            it = itertools.combinations_with_replacement(avail_cards, length - 1)
            for e in it:
                kicker = list(e) + ['CJ']
                put_sorted_cards(result, trio_chain + kicker, weight)
            # 4. do not select {BJ, CJ}
            it = itertools.combinations_with_replacement(avail_cards, length)
            for e in it:
                if length == 5 and len(set(e)) == 1:
                    continue
                kicker = list(e)
                put_sorted_cards(result, trio_chain + kicker, weight)

        logging.debug('trio_solo_chain_{}: {}'.format(length, len(result)))
        return result

    return trio_solo_chain_x


def enum_trio_pair_chain(length):
    """x 连三连一对"""
    if length < 1 or length > 4:
        raise ValueError('chain length is in [1,4]')

    def check_repeat_num(arr, limit):
        """
            arr中每个元素最多重复的次数是limit
            如果超过limit，返回True
        """
        for i, e in enumerate(arr):
            count = 0
            for j in range(i, len(arr)):
                if e == arr[j]:
                    count += 1
                    if count > limit:
                        return True
        return False

    def trio_pair_chain_x():
        result = []
        weight = 0
        if length == 1:
            solo_chain = [[e] for e in CARDS_NO_JOKERS]
        else:
            solo_chain = [CARDS[i:i + length] for i in range(13 - length)]

        for chain in solo_chain:
            weight += 1
            trio_chain = order_repeat(chain, 3)
            avail_cards = [c for c in CARDS_NO_JOKERS if c not in set(chain)]

            it = itertools.combinations_with_replacement(avail_cards, length)
            for e in it:
                if length == 3 and len(set(e)) == 1:
                    # 排除3对重复的情形
                    continue
                if length == 4 and len(set(e)) <= 2 and check_repeat_num(e, 2):
                    # 排除3对或4对重复的情形
                    continue
                kicker = order_repeat(list(e), 2)
                put_sorted_cards(result, trio_chain + kicker, weight)

        logging.debug('trio_solo_chain_{}: {}'.format(length, len(result)))
        return result

    return trio_pair_chain_x


def enum_four_two_solo():
    """四带二单"""
    result = []
    weight = 0
    for four in CARD_FOUR:
        weight += 1
        all_cards = [card for card in CARDS if card != four[0]]
        it = itertools.combinations_with_replacement(all_cards, 2)
        for e in it:
            if e not in [('BJ', 'BJ'), ('CJ', 'CJ')]:
                put_sorted_cards(result, four + list(e), weight)
    logging.debug('four_solo: {}'.format(len(result)))
    return result


def enum_four_two_pair():
    """四带二对"""
    result = []
    weight = 0
    for four in CARD_FOUR:
        weight += 1
        all_cards = [card for card in CARDS_NO_JOKERS if card != four[0]]
        it = itertools.combinations_with_replacement(all_cards, 2)
        for e in it:
            put_sorted_cards(result, four + order_repeat(e, 2), weight)
    logging.debug('four_pair: {}'.format(len(result)))
    return result


def enum_bomb():
    """枚举所有的炸弹"""
    return [(cards2str(four), w) for w, four in enumerate(CARD_FOUR)]


def enum_rocket():
    """返回王炸"""
    return [('BJ-CJ', 0)]


class Doudizhu(object):
    """枚举所有牌型，生成花色无关、顺序无关字典
    提供的接口:
    - 规则检查
    - 牌型大小比较
    - 可出牌提示
    """
    CARD_TYPE = [
        {'name': 'solo', 'zh_name': u'单牌',
         'func': enum_solo, 'size': 15},
        {'name': 'solo_chain_5', 'zh_name': u'顺子5连',
         'func': enum_solo_chain(5), 'size': 8},
        {'name': 'solo_chain_6', 'zh_name': u'顺子6连',
         'func': enum_solo_chain(6), 'size': 7},
        {'name': 'solo_chain_7', 'zh_name': u'顺子7连',
         'func': enum_solo_chain(7), 'size': 6},
        {'name': 'solo_chain_8', 'zh_name': u'顺子8连',
         'func': enum_solo_chain(8), 'size': 5},
        {'name': 'solo_chain_9', 'zh_name': u'顺子9连',
         'func': enum_solo_chain(9), 'size': 4},
        {'name': 'solo_chain_10', 'zh_name': u'顺子10连',
         'func': enum_solo_chain(10), 'size': 3},
        {'name': 'solo_chain_11', 'zh_name': u'顺子11连',
         'func': enum_solo_chain(11), 'size': 2},
        {'name': 'solo_chain_12', 'zh_name': u'顺子12连',
         'func': enum_solo_chain(12), 'size': 1},

        {'name': 'pair', 'zh_name': u'对子',
         'func': enum_pair, 'size': 13},
        {'name': 'pair_chain_3', 'zh_name': u'连对3连',
         'func': enum_pair_chain(3), 'size': 10},
        {'name': 'pair_chain_4', 'zh_name': u'连对4连',
         'func': enum_pair_chain(4), 'size': 9},
        {'name': 'pair_chain_5', 'zh_name': u'连对5连',
         'func': enum_pair_chain(5), 'size': 8},
        {'name': 'pair_chain_6', 'zh_name': u'连对6连',
         'func': enum_pair_chain(6), 'size': 7},
        {'name': 'pair_chain_7', 'zh_name': u'连对7连',
         'func': enum_pair_chain(7), 'size': 6},
        {'name': 'pair_chain_8', 'zh_name': u'连对8连',
         'func': enum_pair_chain(8), 'size': 5},
        {'name': 'pair_chain_9', 'zh_name': u'连对9连',
         'func': enum_pair_chain(9), 'size': 4},
        {'name': 'pair_chain_10', 'zh_name': u'连对10连',
         'func': enum_pair_chain(10), 'size': 3},

        {'name': 'trio', 'zh_name': u'三张',
         'func': enum_trio_chain(1), 'size': 13},
        {'name': 'trio_chain_2', 'zh_name': u'连三2连',
         'func': enum_trio_chain(2), 'size': 11},
        {'name': 'trio_chain_3', 'zh_name': u'连三3连',
         'func': enum_trio_chain(3), 'size': 10},
        {'name': 'trio_chain_4', 'zh_name': u'连三4连',
         'func': enum_trio_chain(4), 'size': 9},
        {'name': 'trio_chain_5', 'zh_name': u'连三5连',
         'func': enum_trio_chain(5), 'size': 8},
        {'name': 'trio_chain_6', 'zh_name': u'连三6连',
         'func': enum_trio_chain(6), 'size': 7},

        {'name': 'trio_solo', 'zh_name': u'三带一',
         'func': enum_trio_solo, 'size': 182},
        {'name': 'trio_solo_chain_2', 'zh_name': u'连三带一2连',
         'func': enum_trio_solo_chain(2), 'size': 979},
        {'name': 'trio_solo_chain_3', 'zh_name': u'连三带一3连',
         'func': enum_trio_solo_chain(3), 'size': 3400},
        {'name': 'trio_solo_chain_4', 'zh_name': u'连三带一4连',
         'func': enum_trio_solo_chain(4), 'size': 7830},
        {'name': 'trio_solo_chain_5', 'zh_name': u'连三带一5连',
         'func': enum_trio_solo_chain(5), 'size': 12512},

        {'name': 'trio_pair', 'zh_name': u'三带一对',
         'func': enum_trio_pair_chain(1), 'size': 156},
        {'name': 'trio_pair_chain_2', 'zh_name': u'连三带一对2连',
         'func': enum_trio_pair_chain(2), 'size': 726},
        {'name': 'trio_pair_chain_3', 'zh_name': u'连三带一对3连',
         'func': enum_trio_pair_chain(3), 'size': 2100},
        {'name': 'trio_pair_chain_4', 'zh_name': u'连三带一对4连',
         'func': enum_trio_pair_chain(4), 'size': 3726},

        {'name': 'four_two_solo', 'zh_name': u'四带二单',
         'func': enum_four_two_solo, 'size': 1339},
        {'name': 'four_two_pair', 'zh_name': u'四带二对',
         'func': enum_four_two_pair, 'size': 1014},

        {'name': 'bomb', 'zh_name': u'炸弹',
         'func': enum_bomb, 'size': 13},
        {'name': 'rocket', 'zh_name': u'王炸',
         'func': enum_rocket, 'size': 1},
    ]

    """
        {cards: [(type, weight), ],}
        value 使用list是为了解决冲突
        - 如四带两对中的3-3-3-3-4-4-4-4和4-4-4-4-3-3-3-3
        - 如3连三带一 3-3-3-4-4-4-5-5-5-6-6-6，也可作为四连三张

        todo: covert the key to binary format
    """
    DATA = {}
    """
        {type:{weight:[cards,]},}
    """
    TYPE_CARDS = {}
    TOTAL = 0
    INIT_FLAG = False

    @staticmethod
    def init_doudizhu_dict():
        if Doudizhu.INIT_FLAG:
            return
        Doudizhu.INIT_FLAG = True
        for ct in Doudizhu.CARD_TYPE:
            rst = ct['func']()
            if len(rst) != ct['size']:
                logging.error(ct)
            Doudizhu.TOTAL += len(rst)

            card_type = ct['name']
            Doudizhu.TYPE_CARDS[card_type] = {}
            for item in rst:
                cards, weight = item
                if cards not in Doudizhu.DATA:
                    Doudizhu.DATA[cards] = [(ct['name'], weight)]
                else:
                    Doudizhu.DATA[cards].append((ct['name'], weight))

                if weight not in Doudizhu.TYPE_CARDS[card_type]:
                    Doudizhu.TYPE_CARDS[card_type][weight] = [cards]
                else:
                    Doudizhu.TYPE_CARDS[card_type][weight].append(cards)

        logging.debug(Doudizhu.TOTAL)

    @staticmethod
    def print_multiple_types_cards():
        for cards, value in iter(Doudizhu.DATA.items()):
            if len(value) > 2 or \
                    (len(value) > 1 and value[0][0] != value[1][0]):
                print(cards, value)

    @staticmethod
    def check_card_type(cards):
        """cards is str type"""
        if isinstance(cards, str):
            cards = str2cards(cards)
        if not isinstance(cards, list):
            return False, None
        sorted_cards = sort_cards(cards)
        value = Doudizhu.DATA.get(cards2str(sorted_cards))
        if value is None:
            return False, ValueError('invalid card type')

        return True, value

    @staticmethod
    def type_greater(type_x, type_y):
        """check if x is greater than y
        type_x/y: (type, weight)
          >0: x > y
          =0: x = y
          <0: x < y
        """
        if type_x[0] == type_y[0]:
            return type_x[1] - type_y[1]
        else:
            if type_x[0] == 'rocket':
                return 1
            elif type_y[0] == 'rocket':
                return -1
            elif type_x[0] == 'bomb':
                return 1

        return ValueError('Can not compare card type')

    @staticmethod
    def cards_greater(cards_x, cards_y):
        """check if x is greater than y
        x, y可能分别组成不同牌型
        只要有x一种牌型大于y，就返回True和牌型
        """
        ok, type_x = Doudizhu.check_card_type(cards_x)
        if not ok:
            return False, '{}: {}'.format(cards_x, type_x)

        ok, type_y = Doudizhu.check_card_type(cards_y)
        if not ok:
            return False, '{}: {}'.format(cards_y, type_y)

        for tx in type_x:
            for ty in type_y:
                flag = Doudizhu.type_greater(tx, ty)
                if not isinstance(flag, ValueError) and flag > 0:
                    return True, tx[0]
        return False, tx[0]

    @staticmethod
    def cards_contain(candidate_cardmap, cardmap):
        for k, v in iter(cardmap.items()):
            if k not in candidate_cardmap:
                return False
            if candidate_cardmap[k] < v:
                return False
        return True

    @staticmethod
    def list_greater_cards(cards_target, cards_candidate):
        """ 对于目标牌组合cards_target
        从候选牌cards_candidate中找出所有可以压制它的牌型

        1. 对于cards_taget同牌型的不同权重组合来说，按其最大权重计算
        如target='3-3-3-3-2-2-2-2', candidate='5-5-5-5-6-6-6-6'),
        这里target当作<四个2带2对3>，所以返回是：
        {'bomb': ['5-5-5-5', '6-6-6-6']}

        2. 对于candidate中一组牌可作不同组合压制cards_taget的场景，只返回一种组合
        如target='3-3-3-3-4-4-4-4', candidate='5-5-5-5-6-6-6-6'),
        <四个5带2对6>，<四个6带2对5> 均大于 <四个4带2对3>
        只返回一次'5-5-5-5-6-6-6-6',
        {'bomb': ['5-5-5-5', '6-6-6-6'], 'four_two_pair': ['5-5-5-5-6-6-6-6']}
        """
        ok, target_type = Doudizhu.check_card_type(cards_target)
        if not ok:
            logging.error('{}: {}'.format(cards_target, target_type))
            return {}

        # 对target_type去重，保留同type中weight最大的
        tmp_dict = {}
        for card_type, weight in target_type:
            if card_type not in tmp_dict or weight > tmp_dict[card_type]:
                tmp_dict[card_type] = weight
        target_type = [(k, v) for k, v in iter(tmp_dict.items())]

        # 如果目标牌型为rocket，则一定打不过，直接返回空
        if target_type[0][0] == 'rocket':
            return {}

        # 按牌型大小依次判断是否可用bomb, rocket
        if target_type[0][0] != 'rocket':
            if target_type[0][0] != 'bomb':
                target_type.append(('bomb', -1))
            target_type.append(('rocket', -1))
        elif target_type[0][0] != 'bomb':
            target_type.append(('bomb', -1))

        logging.debug('target_type: {}'.format(target_type))
        candidate_cardmap = str2cardmap(cards_candidate)
        cards_gt = {}
        for card_type, weight in target_type:
            weight_gt = [w for w in Doudizhu.TYPE_CARDS[card_type].keys()
                         if w > weight]
            if card_type not in cards_gt:
                cards_gt[card_type] = []
            logging.debug(weight_gt)
            logging.debug(candidate_cardmap)
            for w in sorted(weight_gt):
                for w_cards in Doudizhu.TYPE_CARDS[card_type][w]:
                    w_cardmap = str2cardmap(w_cards)
                    if Doudizhu.cards_contain(candidate_cardmap, w_cardmap) \
                            and w_cards not in cards_gt[card_type]:
                        cards_gt[card_type].append(w_cards)
            if not cards_gt[card_type]:
                cards_gt.pop(card_type)
        return cards_gt
