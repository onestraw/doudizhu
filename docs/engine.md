# 斗地主规则检查及比较器
枚举了37种细分牌型，制作一个花色无关、顺序无关的字典，能够在O(1)时间内判断出牌是否有效，在O(1)时间内比较大小

扑克出牌是54张牌的组合，牌型和排列顺序无关，在斗地主游戏中除了两个王，花色也无关大小。
因为与花色无关，按用以下字符表示

    3-4-5-6-7-8-9-10-J-Q-K-A-2-BJ-CJ

    BJ is Black Joker
    CJ is Colored Joker

这里只讨论3人游戏，一副牌，每人最多20张手牌

王炸是特殊，但不算对子，它和2不能参与连顺牌型。侧面看，单牌时CJ能压BJ，同点数不同花色的两张大小相同，才算是对子。

- 一些[corner case](#corner_case)
- 程序跑出`468`种多意的出牌组合
    - 如`A-A-A-A-K-K-K-K`，可以是四个A带两对K，也可以是四个K带两对A
    - 如`6-8-9-9-9-10-10-10-J-J-J-Q-Q-Q-K-K-K-A-A-A`，可以是5连三9-K带`6-8-A-A-A`，也可以是5连三10-A带`6-8-9-9-9`

## 主牌型

| 分类 |      |      | 描述 | 举例 |      |
| ---- | ---- | ---- | ---- | ---- | ---- |
| Primal   | with kicker | Chain    | Description               | Lowest rank and/or shortest chain | Highest rank and/or longest chain possible |
| Solo     | X           | -        | Any single card           | 3 | Colored joker |
| Solo     | X           | Chain    | ≥ Five consecutive individual cards   | 3-4-5-6-7 | 3-4-5-6-7-8-9-10-J-Q-K-A |
| Pair     | X           | -        | Two matching cards of equal rank      | 3-3 | 2-2 |
| Pair     | X           | Sisters  | ≥ Three consecutive pairs             | 3-3-4-4-5-5 | 5-5-6-6-7-7-8-8-9-9-10-10-J-J-Q-Q-K-K-A-A |
| Trio     | -           | -        | Three-of-a-kind: Three individual cards of the same rank  | 3-3-3 | 2-2-2 |
| Airplane | —           | Chain    | ≥ Two consecutive trios               |  3-3-3-4-4-4 | 9-9-9-10-10-10-J-J-J-Q-Q-Q-K-K-K-A-A-A |
| Trio     | Solo        | -        | Three cards of the same rank with a solo as the kicker    | 3-3-3 + 4 | 2-2-2 + colored joker |
| Trio     | Solo        | Airplane | ≥ Two consecutive trios with each carries a distinct individual card as the kicker    | 3-3-3-4-4-4 + 5-6 | 10-10-10-J-J-J-Q-Q-Q-K-K-K-A-A-A + 7-8-9-2-colored joker |
| Trio     | Pair        | -        | Full house: Three cards of the same rank with a pair as the kicker | 3-3-3 + 4-4 | 2-2-2 + A-A |
| Trio     | Pair        | Chain    | ≥ Two consecutive trios with each carrying a pair as the kicker   | 3-3-3-4-4-4 + 5-5-6-6 | J-J-J-Q-Q-Q-K-K-K-A-A-A + 8-8-9-9-10-10-2-2 |
| Four     | Dual solo   | X        | Four-of-a-kind with two distinct individual cards as the kicker   | 3-3-3-3 + 4 + 5 | 2-2-2-2 + A + colored joker |
| Four     | Dual pair   | X        | Four-of-a-kind with two sets of pair as the kicker                | 3-3-3-3 + 4-4 + 5-5 | 2-2-2-2 + K-K + A-A |
| Bomb     |             |          | Four cards of the same rank without the kicker is called a bomb. It can beat any other category and individual card except Rocket or another Bomb with a higher or equal rank. | 3-3-3-3 | 2-2-2-2 |
| Rocket   |             |          | Colored Joker and black-and-white Joker, It can beat everything in the game. | | |

[参考](https://en.wikipedia.org/wiki/Dou_dizhu)

## corner case
 <span id="corner_case"></span>

只讨论符合规则的边界

### 三带一

~~5-5-5-5~~ //不能理解成三张5带一张5

### 2连三带一

    3-3-3-4-4-4-K-K
    3-3-3-4-4-4-BJ-CJ

### 3连三带一

    3-3-3-4-4-4-5-5-5-6-6-6
    3-3-3-4-4-4-5-5-5-K-K-K

    //带了3张同样的, 甚至是4连顺三张

### 4连三带一

    3-3-3-4-4-4-5-5-5-6-6-6-K-K-K-K     //带了一个炸

### 5连三带一

    3-3-3-4-4-4-5-5-5-6-6-6-7-7-7-K-K-K-K-A     //带了一个炸

### 三带一对

~~3-3-3-BJ-CJ~~   //不合法

### 2连三带一对

    3-3-3-4-4-4-K-K-K-K     //带2对K

### 3连三带一对

    3-3-3-4-4-4-5-5-5-Q-Q-Q-Q-A-A   //2对Q，1对A

~~3-3-3-4-4-4-5-5-5-Q-Q-Q-Q-BJ-CJ~~   //2对Q，1对王，不合规


### 4连三带一对

    3-3-3-4-4-4-5-5-5-6-6-6-Q-Q-Q-Q-K-K-K-K
    // 3-4-5-6是4连，带了2个炸，算4对

### 四带二单

    3-3-3-3-BJ-CJ
    3-3-3-3-J-J     //带一对

### 四带二对

~~3-3-3-3-2-2-BJ-CJ~~   //不合规则，双王不能看作一对

    3-3-3-3-A-A-A-A     //一个炸可看作两对被带出去，QQ斗地主验证过
    A-A-A-A-3-3-3-3     //它与上面不同，这是四个A带两对3 

## 各牌型组合数
- n个元素不可重复的选取k个：C(n, k) = P(n) / {P(k) P(n-k)}
- n个元素可重复的选取k个：H(n, k) = P(n+k-1) / {P(k) P(n-1)}
- [组合数计算公式](https://en.wikipedia.org/wiki/Combination)
- [在线计算器](https://www.mathsisfun.com/combinatorics/combinations-permutations-calculator.html)
- 2,BJ,CJ不参与连顺(Chain)
- BJ,CJ不能作为对子使用，3-3-3-BJ-CJ, 4-4-4-4-BJ-CJ-5-5不符合规则，4-4-4-4-BJ-CJ合规，算是两张单牌
- 下面讨论的是每种牌型的种类，不讨论出现的概率，所以不看花色

    3-4-5-6-7-8-9-10-J-Q-K-A-2-BJ-CJ

- 同一组出牌，可能作为不同的牌型
    - 如四带两对中的3-3-3-3-4-4-4-4和4-4-4-4-3-3-3-3
    - 如3连三带一 3-3-3-4-4-4-5-5-5-6-6-6，也可作为四连三张
- 目标是做一个花色无关、顺序无关的字典，能够在O(1)时间内判断出牌是否有效，在O(1)时间内比较大小
- 总共37种牌型，除了炸弹和火箭之外，其余牌型只能各自比较大小.

### 单牌
- 1连
    - C(15,1)=15
    - 3-4-...-K-A-2-BJ-CJ共15张不同值
- 5连
    - C(8,1)=8
    - 3-4-5-6-7,...,10-J-Q-K-A
- 6连
    - C(7,1)
- 7连
    - C(6,1)
- 8连
    - C(5,1)
- 9连
    - C(4,1)
- 10连
    - C(3,1)
- 11连
    - C(2,1)
- 12连
    - C(1,1)

### 对子
- 1连
    - C(13,1) = 13
    - 不考虑王炸 BJ-CJ
- 3连
    - C(10,1)
- 4连
    - C(9,1)
- 5连
    - C(8,1)
- 6连
    - C(7,1)
- 7连
    - C(6,1)
- 8连
    - C(5,1)
- 9连
    - C(4,1)
- 10连
    - C(3,1)

### 三张
- 1连
    - C(13,1) = 13
- 2连
    - C(11,1)
    - 只能是{34,45,...,KA} 11种组合之一
- 3连
    - C(10,1)
- 4连
    - C(9,1)
- 5连
    - C(8,1)
- 6连
    - C(7,1)

### 三带一
基数参考前一节的三张组合数，所带牌型再组合

- 1连
    - C(13,1) x C(14,1) = 182
    - 13张非Joker中选一种作`三`，另外12张+Jokers作`一`
- 2连
    - C(11,1) x [C(13,2) + 11] = 979
    - 带的两张可以相同，可以是Joker，但不能组成四张，如3-3-3-4-4-4-x-y
    - 1.{x,y}是从{5,6,...,2,BJ,CJ}中取两个值，即C(13,2)
    - 2.如果x=y, 可选择集合是另外11张非Joker
- 3连
    - C(10,1) x [C(12,3) + 10 + 10x11] = 3400
    - 如3-3-3-4-4-4-5-5-5-x-y-z
    - 1.{x,y,z}各不相同，C(12,3)
    - 2.三张一样x=y=z, C(10,1)
    - 3.有两张一样，这里不认为两张Joker相同，先抽出一对，再抽另外一张(可以有Joker)，C(10,1) x C(11,1)
    - 因为Joker只有两张，还不相同，所以不能用下面方法：在集合{6,7,...,2,BJ,CJ}中可重复性抽取3张
    - 另一种方式：
    - 1.先选取{BJ, CJ},另外10种牌中选取1张, 10
    - 2.选取{BJ, CJ}之一,再从另外可重复性选取的10种牌中取2张，2 x H(10,2) = 110
    - 3.不选取{BJ, CJ},从另外可重复性选取的10种牌中取3张，H(10, 3) = 220
- 4连
    - C(9,1) x [45 + 330 + 495] = 7830
    - 如3-3-3-4-4-4-5-5-5-6-6-6-x-y-z-u, {x,y,z,u}选取方式分3类:
    - 1.先选取{BJ, CJ},另外9种牌中选取2张, H(9,2) = 45
    - 2.选取{BJ, CJ}之一,再从另外可重复性选取的9种牌中取3张，2 x H(9,3) = 330
    - 3.不选取{BJ, CJ},从另外可重复性选取的9种牌中取4张，H(9, 4) = 495
- 5连
    - C(8,1) x [120 + 660 + 784] = 12512
    - 如3-3-3-4-4-4-5-5-5-6-6-6-7-7-7-x-y-z-u-v, {x,y,z,u,v} 选取方式分3类
    - 1.先选取{BJ, CJ},另外8种牌中选取3张, H(8,3) = 120
    - 2.选取{BJ, CJ}之一,再从另外可重复性选取的8种牌中取4张，2 x H(8,4) = 660
    - 3.不选取{BJ, CJ},从另外可重复性选取的8种牌中取5张，一张牌最多重复4次，减去5张同样的组合，H(8, 5) - 8 = 784

### 三带二
- 1连
    - C(13,1) x C(12,1) = 156
- 2连
    - C(11,1) x H(11,2) = 726
    - 从11种牌（每种可构成2对）可重复性选取2种，H(11,2) = 66
- 3连
    - C(10,1) x H(10,3) = 2100
    - 从10种牌（每种可构成2对）可重复性选取3种，除去所取3种都相同的数目10，H(10,3) - 10 = 210
- 4连
    - C(9,1) x 414 = 3726
    - 选完4连三之后，从另外9种牌18对中选取4对，减去3对或4对同点数的组合，H(9,4) - 9 - C(9,1) x 8 = 414

### 四带二单

- C(13,1) x [H(14,2) - 2] = 1339
- 3,4,...,A,2选一作四，从另外12张+Jokers中选两单，从14张中可重复性选2张，再减去2（BJ-BJ, CJ-CJ），H(14,2) - 2

### 四带二对

- C(13,1) x H(12,2) = 1014
- 从12种牌（每种可构成2对）可重复性选取2种，H(12,2) = 78

### 四张（炸弹）
压制点数比其小的炸弹及非王炸，上面所有牌型

- 13

### 俩王（火箭, 王炸）
压制一切

- 1
