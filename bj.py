from random import shuffle

SUIT = {1: 'ハート', 2: 'スペード', 3: 'ダイヤ', 4: 'クローバー'}

RANK = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}


class Deck:
    def __init__(self):
        self.deck = []
        for suit in range(1, 5):
            for rank in range(1, 14):
                self.deck.append(suit * 100 + rank)
        shuffle(self.deck)

    def draw_card(self):
        return self.deck.pop()


class Participant:
    def __init__(self, name):
        self.name = name
        self.rank = []
        self.draw_card_history = []

    def get_sum(self):
        return sum(self.rank)

    def get_suit_rank(self, card):
        num_suit = card // 100
        num_rank = card % 100
        display_suit = SUIT[num_suit]
        display_rank = RANK.get(num_rank, str(num_rank))
        return num_suit, num_rank, display_suit, display_rank

    def set_hand(self, card, *, display=True):
        _, num_rank, display_suit, display_rank = self.get_suit_rank(card)
        if display:
            print('{} の引いたカードは {} の {} です'.format(self.name, display_suit,
                                                  display_rank))
        else:
            print('{} の引いたカードはわかりません'.format(self.name))
        self.rank.append(min(num_rank, 10))
        self.draw_card_history.append(card)

    def over_twenty_one(self):
        if sum(self.rank) > 21:
            return True
        return False

    def display_suit_rank(self, n):
        card = self.draw_card_history[n - 1]
        _, _, display_suit, display_rank = self.get_suit_rank(card)
        print('{} が引いた {} 枚目のカードは {} の {} です'.format(self.name, n,
                                                     display_suit,
                                                     display_rank))


class Player(Participant):
    def is_continue(self):
        print('{} のスコアは {}'.format(self.name, sum(self.rank)))
        if input('引く場合は y, やめる場合は n\n>') == 'y':
            return True
        return False


class Dealer(Participant):
    def is_continue(self):
        print('{} のスコアは {}'.format(self.name, sum(self.rank)))
        if self.get_sum() < 17:
            return True
        return False


def main():
    deck = Deck()
    player = Player('player')
    dealer = Dealer('dealer')

    player.set_hand(deck.draw_card())
    player.set_hand(deck.draw_card())
    dealer.set_hand(deck.draw_card())
    dealer.set_hand(deck.draw_card(), display=False)

    print()

    while player.is_continue():
        player.set_hand(deck.draw_card())
        if player.over_twenty_one():
            print('21 を越えました')
            print('あなたの負けです')
            break

    print()

    if not player.over_twenty_one():
        dealer.display_suit_rank(2)
        while dealer.is_continue():
            dealer.set_hand(deck.draw_card())

        if dealer.over_twenty_one() or player.get_sum() >= dealer.get_sum():
            print('あなたの勝ちです')
        else:
            print('あなたの負けです')


main()
