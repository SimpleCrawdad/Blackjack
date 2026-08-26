import random

class shoe:

    def __init__(self, decks):
        self.decks = decks
        self.downcount = 0
        self.order = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4 * decks
        self.splitcount = 0
        self.rest = False

    

    def shuffle(self):
        random.shuffle(self.order)

    def double(self, hand):
        self.cards[hand].append(self.order.pop())
        self.doublist.append(hand)

    def deal(self):
        self.cards = {0:[]}
        self.cards[0].append(self.order.pop())
        self.cards[0].append(self.order.pop())
        self.dealerup = self.order.pop()
        self.dealerdown = self.order.pop()
        self.dlist = [self.dealerup, self.dealerdown]
        self.downcount += 4
        self.doublist = []

    def bjcheck(self):
        self.dealerbj = False
        self.playerbj = False

        if self.dealerup in ['10', 'J', 'Q', 'K']:
            if self.dealerdown == 'A':
                self.dealerbj = True
        elif self.dealerup == 'A':
            if self.dealerdown in ['10', 'J', 'Q', 'K']:
                self.dealerbj = True

        if 'A' in self.cards[0] and any(card in ['10', 'J', 'Q', 'K'] for card in self.cards[0]):
            self.playerbj = True

    def splcheck(self):
        self.spavailable = False
        self.spvloc = []

        for i in range(len(self.cards)):
            if self.cards[i][0] == self.cards[i][1]:
                self.spavailable = True
                self.spvloc.append(i)

    def split(self,hand):
        self.splitcount += 1
        self.cards[self.splitcount] = [self.cards[hand].pop(), self.order.pop()]
        self.cards[hand].append(self.order.pop())

    def hit(self, hand):
        self.cards[hand].append(self.order.pop())

    def valchk(self, hand):
        self.value = 0
        Acount = 0
        for i in self.cards[hand]:
            try:
                int(i)
                self.value += int(i)
            except ValueError:
                if i in ['J', 'Q', 'K']:
                    self.value += 10 
                elif i == "A":
                    Acount += 1
                else:
                    print("Error, Unknown Card Value")
        for i in range(Acount):
            if self.value + Acount <= 11:
                self.value += 11
            else:
                self.value += 1
        return self.value

    def dchk(self):
        self.dvalue = 0
        Acount = 0

        while 1 == 1:
            self.dvalue = 0
            Acount = 0
            
            for i in self.dlist:
                try:
                    int(i)
                    self.dvalue += int(i)
                except ValueError:
                    if i in ['J', 'Q', 'K']:
                        self.dvalue += 10 
                    elif i == "A":
                        Acount += 1
                    else:
                        print("Error, Unknown Card Value")
            for i in range(Acount):
                if self.dvalue + Acount <= 11:
                    self.dvalue += 11
                else:
                    self.dvalue += 1
            if self.dvalue < 17:
                self.dlist.append(self.order.pop())
                print(f"Dealer Draws {self.dlist[-1]}")
            else:
                break







        
class stack:
    def __init__(self, size: float):
        self.size = size
        self.bets = []

    def entbet(self, bet):
        self.betsize = bet
    
    def lose(self):
        self.size = self.size - self.betsize

    def win(self):
        self.size = self.size + self.betsize

    def blackjack(self, ratio: float):
        self.size = self.size + (ratio * self.betsize)

    def bet(self):
        self.bets.append(self.betsize)
    

class scripts:

    def pl(self):
        self.ans = input("Play Another Hand? (y/n)")
        if self.ans == "y":
            self.rest == True
        elif self.ans == "n":
            exit()
        else:
            print("Please Enter y or n.")




        

# shoe1 = shoe(6)
# shoe1.shuffle()
# shoe1.deal()

# print(f'You Have {shoe1.cards[1]}')
# print(f'Dealer Shows {shoe1.dealerup}')
