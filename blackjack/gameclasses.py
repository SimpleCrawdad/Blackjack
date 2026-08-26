import random



class Shoe:

    def __init__(self, decks):
        self.decks = decks
        self.reset()

    def reset(self):
        self.order = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4 * self.decks
        self.removed = []   
        random.shuffle(self.order)
    
    def draw(self):
        self.removed.append(self.order.pop())
        return self.removed[-1]



class Stack:
    def __init__(self, size: float):
        self.size = size
        self.clearbets()
        self.bettracker = []

    def clearbets(self):
        self.bets = []
        self.doubles = []

    def bet(self, bet):
        self.bets.append(bet)
    
    def lose(self, handid):
        self.size = self.size - self.bets[handid]
        self.bettracker.append([f'-{self.bets[handid]}', 'lost'])

    def win(self, handid):
        self.size = self.size + self.bets[handid]
        self.bettracker.append([f'+{self.bets[handid]}', 'won'])

    def push(self):
        self.bettracker.append(['0', 'push'])

    def blackjack(self, ratio: float, handid):
        self.size = self.size + (ratio * self.bets[handid])
        self.bettracker.append([f'+{self.bets[handid]*1.5}', 'blackjack'])

    def double(self, betid):
        self.bets[betid] *= 2
        self.doubles.append(betid)
    


class Action:

    def __init__(self, shoe):
        self.reset()
        self.shoe = shoe

    def reset(self):
        self.splitcount = 0
        
    def deal(self):
        self.cards = [[self.shoe.draw(), self.shoe.draw()]]
        self.dealerhand = [self.shoe.draw(), self.shoe.draw()]

    def hit(self, handid):
        if type(handid) == int:
            self.cards[handid].append(self.shoe.draw())
        else:
            handid.append(self.shoe.draw())

    def split(self, handid):
        self.splitcount += 1
        self.cards.append([self.cards[handid].pop(), self.shoe.draw()])
        self.cards[handid].append(self.shoe.draw())



class Logic:

    def valuecalc(self, card):
        value = 0
        ace = False
        if card == 'A':
            ace = True
            value += 1
        elif card in ['J', 'Q', 'K']:
            value += 10
        else:
            try:
                value += int(card)
            except ValueError:
                exit("Error, Unknown Card Value")
        return [value, ace]
    
    def handval(self, hand):
        self.value = 0
        self.aces = 0
        self.hand = hand
        self.soft = False
        self.blackjack = False
        self.bust = False

        for card in self.hand:
            self.value += self.valuecalc(card)[0]
            if self.valuecalc(card)[1] == True:
                self.aces += 1
        if self.aces > 0 and self.value <= 11:
            self.value += 10
            self.soft = True
        if self.value == 21 and len(self.hand) == 2:
                self.blackjack = True
        if self.value > 21:
            self.bust == True

             

class Dealer(Logic):

    def dealerplay(self, h17: bool, hand: list, action: Action):
        while True:
            self.handval(hand)
            
            if self.dealerlogic(h17) == 'hit':
                action.hit(hand)
            else:
                return self.dealerlogic(h17)



    def dealerlogic(self, h17: bool):

            if self.value < 17 or (self.soft == True and h17 == True and self.value == 17):
                return 'hit'
            elif self.value <= 21:
                if self.blackjack == True:
                    return 'blackjack'
                else:
                    return self.value
            else: 
                return 'bust'



class Player(Logic):
    def __init__(self, action: Action, stack: Stack):
        self.action = action
        self.stack = stack
        self.split = True
        self.acereset()

    def acereset(self):
        self.acesplit_prohibiting = False

    def preseq(self, handid: int, betid: int, dbl: bool, spl: bool, das: bool, spa: bool, rsa: bool, maxsplits = None):
        hand = self.action.cards[handid]

        if das == False and dbl == True and self.action.splitcount == 0:
                self.stack.double(betid)
                self.action.hit(handid)

        if hand[0] == hand[1] and len(hand) == 2 and self.acesplit_prohibiting != True and spl == True:
            if maxsplits == None or self.action.splitcount < maxsplits:
                if spa == True or hand[0] != 'A':
                    if rsa == False and hand == ['A', 'A']:
                        self.acesplit_prohibiting = True
                    self.action.split(handid)
                    self.stack.bet(self.stack.bets[0])

        if das == True and dbl == True:
            self.stack.double(betid)
            self.action.hit(handid)



class Game:
    def __init__(self, dealer: Dealer, player: Player, action: Action, stack: Stack):
        self.dealer = dealer
        self.player = player
        self.action = action
        self.stack = stack

    def blackjackcheck(self, ratio):
        self.dealer.handval(self.action.dealerhand) 
        self.player.handval(self.action.cards[0])

        if self.dealer.blackjack == True and self.player.blackjack == True:
            self.stack.push()
            return 'push'
        elif self.dealer.blackjack == True:
            self.stack.lose(0)
            return 'lose'
        elif self.player.blackjack == True:
            self.stack.blackjack(ratio, 0)
            return 'win'
        else:
            return None

    def endhand(self, handid, h17):
        self.player.handval(self.action.cards[handid])
        self.dealer.handval(self.action.dealerhand)
        if self.player.bust == True:
            self.stack.lose(handid)
            return 'bust'
        else:
            self.dealer.dealerplay(h17 = h17, hand = self.action.dealerhand, action = self.action)
            if self.dealer.bust == True:
                self.stack.win(handid)
                return 'dbust'
            elif self.dealer.value > self.player.value:
                self.stack.lose(handid)
                return 'lose'
            elif self.dealer.value == self.player.value:
                self.stack.push()
                return 'push'
            elif self.dealer.value < self.player.value:
                self.stack.win(handid)
                return 'win'
        

        

class Cardcount:
    def __init__(self, decks):
        self.decks = decks
        self.reset()
        self.update()
        self.rank = list(self.weights.keys())



    def reset(self):

        self.denom = 52 * self.decks
        self.num = {
            '2': 4 * self.decks,
            '3': 4 * self.decks,
            '4': 4 * self.decks,
            '5': 4 * self.decks,
            '6': 4 * self.decks,
            '7': 4 * self.decks,
            '8': 4 * self.decks,
            '9': 4 * self.decks,
            '10': 4 * self.decks,
            'J': 4 * self.decks,
            'Q': 4 * self.decks,
            'K': 4 * self.decks,
            'A': 4 * self.decks,
        }
 


    def update(self):
                
        self.weights = {
            '2': self.num['2']/self.denom,
            '3': self.num['3']/self.denom,
            '4': self.num['4']/self.denom,
            '5': self.num['5']/self.denom,
            '6': self.num['6']/self.denom,
            '7': self.num['7']/self.denom,
            '8': self.num['8']/self.denom,
            '9': self.num['9']/self.denom,
            '10': self.num['10']/self.denom,
            'J': self.num['J']/self.denom,
            'Q': self.num['Q']/self.denom,
            'K': self.num['K']/self.denom,
            'A': self.num['A']/self.denom,
        }




    def runningcount(self, card):
        for i in self.rank:
            if i == card:
                self.num[i] -= 1
                self.denom -= 1
                self.update()



class Probability(Cardcount):

    def __init__(self,decks):

        super().__init__(decks)
        self.setprob()

    def setprob(self): 

        self.probtotals = {
            17: 0,
            18: 0,
            19: 0,
            20: 0,
            21: 0,
            'bust': 0,
            'blackjack': 0

        }

    def probadd(self, i, prob):
        self.probtotals[i] += prob

    def dealerev(self, dealer: Dealer, h17: bool, card: str, hand = None):

        if hand == None:
            hand = [card]
            self.initl = len(hand)

        dealer.handval(hand)

        if dealer.dealerlogic(h17) != 'hit':

            prob = 1
            self.reset()

            for card in hand[:self.initl]:
                self.runningcount(card)

            for card in hand[self.initl:]:
                prob *= self.weights[card]
                self.runningcount(card)

            self.probadd(dealer.dealerlogic(h17), prob)
            return
        
        for i in self.rank:
            newhand = hand.copy()
            newhand.append(i)
            self.dealerev(dealer, h17, card = None, hand = newhand)



