class evcalc:


    def __init__(self, c1, c2):
        self.inprob = 1/169
        if c1 != c2:
            self.inprob *= 2
        if c1 == '10':
            self.inprob *= 4
        if c2 == '10':
            self.inprob *= 4


        self.worder = {'2': 1, 
                       '3': 1, 
                       '4': 1, 
                       '5': 1, 
                       '6': 1, 
                       '7': 1, 
                       '8': 1, 
                       '9': 1, 
                       '10': 4, 
                       'A': 1}
        self.weights = list(self.worder.values())
        self.order = list(self.worder.keys())

    def tester(self, total, dprob, aces):

            value = total
            if aces > 0 and total + 10 <= 21:
                value += 10

            if value >= 17:
                newtotal = value
            if value >= 17:
                if value == 17:
                    self.svt += dprob
                elif value == 18:
                    self.egt += dprob
                elif value == 19:
                    self.ntn += dprob
                elif value == 20:
                    self.twy += dprob
                elif value == 21:
                    self.twn += dprob
                elif value > 21:
                    self.bust += dprob

                return value, dprob

            for card in self.order:

                newprob = dprob * self.weights[self.order.index(card)]* 1/13

                newtotal = total
                newaces = aces

                if card == 'A':
                    newaces += 1
                    newtotal += 1
                else:
                    newtotal += int(card)

            
                self.tester(newtotal, newprob, newaces)
            

    def dlrnum(self, d1):
        self.svt = 0
        self.egt = 0
        self.ntn = 0
        self.twy = 0
        self.twn = 0
        self.bust = 0
        self.bkjk = 0

        for i, card in enumerate(self.order):
            self.dealercards = []
            self.dealercards.append(d1)
            self.dealercards.append(self.order[i])
            self.static = 1/13 * self.weights[self.order.index(card)]
            total = 0
            aces = 0

            if 'A' in self.dealercards and '10' in self.dealercards:
                self.bkjk += self.static
                continue

            for j in self.dealercards:
                if j == 'A':
                    aces += 1
                    total += 1
                else:
                    total += int(j)
            
            self.tester(total, self.static, aces)

        self.totals = [self.svt, self.egt, self.ntn, self.twy, self.twn, self.bust, self.bkjk]




# tprob = 0
# for i, c1 in enumerate(order):
#     for c2 in order[i:]:
#         print(c1, c2)
#         ev = evcalc(c1, c2)
#         print(f"Probability of hand {c1, c2} = {ev.inprob}")         
#         tprob += ev.inprob
#         print(tprob)
    