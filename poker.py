print("")
print("   _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")
print(" # Реализуйте функцию Best_hand, которая принимает на вход ")
print(" # покерную 'руку' (hand) из 7ми карт и возвращает лучшую")
print(" # (Относительно значения, возвращаемого hand_rank)")
print(" # 'руку' из 5ти карт. У каждой карты есть масть(suit) и")
print(" # ранг(rank)")
print("")
print(" # Масти: Трефы(Clubs, C), пики(Spades, S), черви(Hearts, H), бубны(Diamonds, D)")
print(" # Ранги: 2,3,4,5,6,7,8,9,10(Ten, T), Валет(Jack, J), Дама(queen, Q), Король(King, K), Туз(Ace, A)")
print(" # Например: AS - Туз пик(Ace od Spades), TH - Десятка червь(Ten of Hearts), 3C - Тройка треф(Three of Clubs)")
print("")
print(" # Задание со *")
print(" # Реализуйте функцию Best_Wild_Hand, которая принимает на вход")
print(" # покерную 'руку'(hand) из 7ми карт и возвращает лучшую")
print(" # (Относительно значения, возвращаемого hand_rank)")
print(" # 'руку' из 5ти карт. Кроме прочего в данном варианте 'рука'")
print(" # может включать джокера. Джокеры могут заменить карту любой")
print(" # масти и ранга того же цвета. Чёрный джокер '?B' может быть")
print(" # использован в качестве треф или пик любого ранга, красный ")
print(" # джокер '?R' - в качестве черв и бубен любого ранга.")
print("")
print(" # Одна функция уже реализована, сигнатуры и описания других даны.")
print(" # Вам неверняка пригодится itertools.")
print(" # Можно свободно определять свои функции и т.п.")
print("   _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")
print("")
import itertools
from collections import Counter

def hand_rank(hand):
    """Возвращает значение определяющее ранг 'руки'"""
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind (4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind (3, ranks) and kind (2, ranks):
        return (6, (3, ranks) and kind (2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)

def card_ranks(hand):
    """Возвращает список рангов, отчортированный от большого к меньшему"""
    return sorted(["23456789TJQKA".index(rank) for rank,suit in hand], reverse = True)

def flush(hand):
    """Возвращает TRUE, если все карты одной масти"""
    return len(set([suit for rank, suit in hand])) == 1

def straight(ranks):
    """Возвращает TRUE, если отсортированные ранги формируют последовательность 5ти,
    где у 5ти карт ранги идут по порядку (стрит)"""
    return ranks == list(range(max(ranks), min(ranks)-1, -1))

def kind(n, ranks):
    """Возвращает первый ранг, который n раз встречается в данной руке
    Возвращает None, если ничего не найдено"""
    for rank, group in itertools.groupby (ranks):
        if len(list(group)) == n:
            return rank
    return None

def two_pair(ranks):
    """Если есть две пары, то возвращает два соответствующих ранга
    Иначе возвращает None"""
    r1, r2 = kind(2, ranks), kind(2, ranks[::-1])
    return (r1, r2) if r1 and (r1 != r2) else None

def best_hand(hand):
    """Из 'руки' в 7 карт возвращает лучшую 'руку' в 5 карт"""
    handa5 = itertools.combinations(hand, 5)
    return max(handa5, key = hand_rank)

def best_wild_hand(hand):
    """Best_Hand но с джокерами"""
    jokers = {"?B" : "CS", "?R" : "HD"}
    clear_hand = [card for card in hand if card not in jokers]
    joker_suits = [jokers[card] for card in hand if card in jokers]
    hands = [clear_hand]
    for joker_suit in joker_suits:
        cards = ["%s%s"%(r, s) for r,s in itertools.product("23456789TJQKA", joker_suit)]
        cards = [card for card in cards if card not in clear_hand]
        hands = [h + [card] for h in hands for card in cards]
    return max(set([best_hand(h) for h in hands]), key=hand_rank)

def test_best_hand():
    print("test_best_hand...")
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print("OK")

def test_best_wild_hand():
    print("test_best_wild_hunt...")
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print("OK")

if __name__ == '__main__':
    test_best_hand()
    test_best_wild_hand()

    input()

    input("")
