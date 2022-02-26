class Shoe:
    def __init__(self, a):
        self.one = 4 * a
        self.two = 4 * a
        self.three = 4 * a
        self.four = 4 * a
        self.five = 4 * a
        self.six = 4 * a
        self.seven = 4 * a
        self.eight = 4 * a
        self.nine = 4 * a
        self.ten = 16 * a
        self.total = 52 * a

    def update_card(self, card):
        if card == 11:
            self.one -= 1
        elif card == 2:
            self.two -= 1
        elif card == 3:
            self.three -= 1
        elif card == 4:
            self.four -= 1
        elif card == 5:
            self.five -= 1
        elif card == 6:
            self.six -= 1
        elif card == 7:
            self.seven -= 1
        elif card == 8:
            self.eight -= 1
        elif card == 9:
            self.nine -= 1
        else:
            self.ten -= 1

        self.total -= 1

    def cards_left(self, card):
        if card == 1:
            return self.one
        elif card == 2:
            return self.two
        elif card == 3:
            return self.three
        elif card == 4:
            return self.four
        elif card == 5:
            return self.five
        elif card == 6:
            return self.six
        elif card == 7:
            return self.seven
        elif card == 8:
            return self.eight
        elif card == 9:
            return self.nine
        elif card == 11:
            return self.one
        else:
            return self.ten

    def good_count(self):
        for i in range(2, 7):
            while self.cards_left(i) > 0:
                self.update_card(i)

    def bad_count(self):
        for i in range(10, 12):
            while self.cards_left(i) > 0:
                self.update_card(i)
