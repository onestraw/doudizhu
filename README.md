# 斗地主引擎
[![Build Status](https://travis-ci.org/onestraw/doudizhu.svg)](https://travis-ci.org/onestraw/doudizhu)
[![Supported Python versions](https://img.shields.io/badge/Python-2%2C%203-green.svg)](https://pypi.org/project/doudizhu/)
[![PyPI Version](https://img.shields.io/badge/PyPI-0.1.5-orange.svg)](https://pypi.org/project/doudizhu/)

通过枚举37种细分牌型，制作一个花色无关、顺序无关的字典，字典规模大小是`34152`，能够在O(1)时间内判断出牌是否有效、比较大小。

基于组合数学，设计思路见[详细文档](docs/engine.md)

## Keep in mind
- 扑克出牌是54张牌的组合，牌型和排列顺序无关
- 在斗地主游戏中，牌型及大小和花色无关
- 两个王不算对子
- 同一手牌，可以作为不同牌型，如`3-3-3-3-2-2-2-2`和`3-3-3-4-4-4-5-5-5-6-6-6`

## 扑克的表示
### 15种点数

    '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2', 'BJ', 'CJ'

- BJ: Black Joker    小王/花/鬼
- CJ: Colored Joker  大王/花/鬼

### 4种花色

    's': spades   黑桃 ♠
    'h': hearts   红心 ❤
    'd': diamonds 方块 ♦
    'c': clubs    梅花 ♣

### 举例

    '2c': 单张[ 2 ♣ ]
    '2h-2s-2d-2c-BJ-CJ': 四个2带两王[ 2 ❤ ] , [ 2 ♠ ] , [ 2 ♦ ] , [ 2 ♣ ] , [ BJ  ] , [ CJ  ]
    '3c-4d-5h-6s-7s-8h-9h': 顺子[ 3 ♣ ] , [ 4 ♦ ] , [ 5 ❤ ] , [ 6 ♠ ] , [ 7 ♠ ] , [ 8 ❤ ] , [ 9 ❤ ]

## Quickstart
### Installing

`pip install doudizhu`

### 开始一局游戏
```python
>>> from doudizhu import Card, new_game
>>> cards_groups = new_game()
>>>
>>> cards_groups
[[44, 28, 27, 43, 42, 72, 39, 38, 37, 69, 132, 131, 19, 34, 66, 65, 33], [14, 75, 139, 138, 26, 25, 137, 23, 71, 135, 134, 20, 67, 130, 17, 16, 128], [13, 140, 76, 74, 41, 24, 22, 70, 133, 21, 68, 36, 35, 18, 129, 64, 32], [73, 40, 136]]
>>> for cards_group in cards_groups:
...     Card.print_pretty_cards(cards_group)
...
  [ 2 ❤ ] , [ 2 ♠ ] , [ A ♠ ] , [ A ❤ ] , [ K ❤ ] , [ J ♦ ] , [ 10 ❤ ] , [ 9 ❤ ] , [ 8 ❤ ] , [ 8 ♦ ] , [ 7 ♣ ] , [ 6 ♣ ] , [ 6 ♠ ] , [ 5 ❤ ] , [ 5 ♦ ] , [ 4 ♦ ] , [ 4 ❤ ]
  [ CJ  ] , [ A ♦ ] , [ A ♣ ] , [ K ♣ ] , [ K ♠ ] , [ Q ♠ ] , [ Q ♣ ] , [ 10 ♠ ] , [ 10 ♦ ] , [ 10 ♣ ] , [ 9 ♣ ] , [ 7 ♠ ] , [ 6 ♦ ] , [ 5 ♣ ] , [ 4 ♠ ] , [ 3 ♠ ] , [ 3 ♣ ]
  [ BJ  ] , [ 2 ♣ ] , [ 2 ♦ ] , [ K ♦ ] , [ Q ❤ ] , [ J ♠ ] , [ 9 ♠ ] , [ 9 ♦ ] , [ 8 ♣ ] , [ 8 ♠ ] , [ 7 ♦ ] , [ 7 ❤ ] , [ 6 ❤ ] , [ 5 ♠ ] , [ 4 ♣ ] , [ 3 ♦ ] , [ 3 ❤ ]
  [ Q ♦ ] , [ J ❤ ] , [ J ♣ ]
```

### 检查牌型
```python
>>> from doudizhu import Card, check_card_type
>>> test_chain = Card.card_ints_from_string('3c-4d-5h-6s-7s-8h')
>>> test_four_two = Card.card_ints_from_string('2c-2d-2h-2s-BJ-CJ')
>>>
>>> check_card_type(test_four_two)
(True, [('four_two_solo', 13)])
>>> check_card_type(test_chain)
(True, [('solo_chain_6', 0)])
>>> check_card_type(test_chain[:4])
(False, ValueError('invalid card type',))
```

### 比较大小
```python
>>> from doudizhu import Card, cards_greater
>>> chain = Card.card_ints_from_string('3c-4d-5h-6s-7s-8h-9h')
>>> bomb = Card.card_ints_from_string('8h-8s-8d-8c')
>>> rocket = Card.card_ints_from_string('BJ-CJ')
>>>
>>> cards_greater(chain, chain)
(False, 'solo_chain_7')
>>> cards_greater(chain[:6], chain[1:7])
(False, 'solo_chain_6')
>>>
>>> cards_greater(chain[1:7], chain[:6])
(True, 'solo_chain_6')
>>> cards_greater(bomb, chain)
(True, 'bomb')
>>> cards_greater(rocket, bomb)
(True, 'rocket')
```

### 牌型提示
```python
>>> from doudizhu import Card, list_greater_cards
>>> def PrettyPrint(cards_gt):
...     for card_type, cards_list in cards_gt.items():
...         print('card type: {}'.format(card_type))
...         for card_int in cards_list:
...             Card.print_pretty_cards(list(card_int))
...
>>> cards_candidate = Card.card_ints_from_string('CJ-Ah-As-Ac-Kh-Qs-Jc-10h-10s-10c-10d-9h-7c-7d-5c-5s')
>>> cards_two = Card.card_ints_from_string('Jh-Jc')
>>> cards_chain_solo = Card.card_ints_from_string('5h-6h-7s-8c-9d')
>>> cards_trio_two = Card.card_ints_from_string('6h-6s-6c-3d-3c')
>>>
>>> PrettyPrint(list_greater_cards(cards_two, cards_candidate))
card type: pair
  [ A ❤ ], [ A ♠ ]
card type: bomb
  [ 10 ♣ ], [ 10 ❤ ], [ 10 ♦ ], [ 10 ♠ ]
>>>
>>> PrettyPrint(list_greater_cards(cards_chain_solo, cards_candidate))
card type: solo_chain_5
  [ K ❤ ], [ Q ♠ ], [ J ♣ ], [ 10 ♠ ], [ 9 ❤ ]
  [ A ♠ ], [ K ❤ ], [ Q ♠ ], [ J ♣ ], [ 10 ♠ ]
card type: bomb
  [ 10 ♣ ], [ 10 ❤ ], [ 10 ♦ ], [ 10 ♠ ]
>>>
>>> PrettyPrint(list_greater_cards(cards_trio_two, cards_candidate))
card type: trio_pair
  [ 10 ❤ ], [ 10 ♦ ], [ 10 ♠ ], [ 5 ♣ ], [ 5 ♠ ]
  [ 10 ❤ ], [ 10 ♦ ], [ 10 ♠ ], [ 7 ♣ ], [ 7 ♦ ]
  [ A ❤ ], [ A ♠ ], [ 10 ❤ ], [ 10 ♦ ], [ 10 ♠ ]
  [ A ❤ ], [ A ♣ ], [ A ♠ ], [ 5 ♣ ], [ 5 ♠ ]
  [ A ♣ ], [ A ❤ ], [ A ♠ ], [ 7 ♣ ], [ 7 ♦ ]
  [ A ❤ ], [ A ♣ ], [ A ♠ ], [ 10 ❤ ], [ 10 ♠ ]
card type: bomb
  [ 10 ♣ ], [ 10 ❤ ], [ 10 ♦ ], [ 10 ♠ ]
```
