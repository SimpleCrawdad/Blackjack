from gameclasses import *

# while True:
#     try:
#         d = int(input('How many decks are you playing?'))
#         break
#     except ValueError:
#         print("Please enter a valid number")

# while True:
#     try:
#         ss = float(input('How many chips are you buying?'))
#         break
#     except ValueError:
#         print("Please enter a valid number")

# while True:
#     try:
#         pen = float(input('What is the deck penetration (as a decimal)?'))
#         break
#     except ValueError:   
#         print("Please enter a valid number")

# while True:
#     h17 = input('Dealer hits on soft 17? (y/n)')
#     if h17.lower() == 'y':
#         h17 = True
#         break
#     elif h17.lower() == 'n':
#         h17 = False
#         break
#     else:
#         print("Please enter y or n")

d = 6
ss = 200
pen = .25
r = 1.5

h17 = True
das = True
spa = True
rsa = True
maxsplits = None


shoe = Shoe(d)
stack = Stack(ss)
action = Action(shoe)
dealer = Dealer()
player = Player(stack = stack, action = action)

game = Game(dealer = dealer, player = player, action = action, stack = stack)

while 1==1:

    player.acereset()
    action.reset()

    print(f'Your stack size is {stack.size}')

    # while True:
    #     try:
    #         bet = float(input('Please enter a bet'))
    #         break
    #     except ValueError:
    #         print("Please enter a valid number")

    bet = 5
    stack.bet(bet)
    print(f'You bet {bet} chips')

    action.deal()
    print(f'You Are Dealt {action.cards[0]}')
    print(f'Dealer Shows {action.dealerhand[0]}')
    


    bjc = game.blackjackcheck(r)
    if bjc == 'lose':
        print('Dealer Blackjack, skill issue')
    elif bjc == 'push':
        print('Two Blackjacks, push')
    elif bjc == 'win':
        print('Blackjack, nice hand!')


    
    if das == False:
        while True:
            dbl = input(f'Double on hand {0}: {action.cards[0]} (y/n)')
            if dbl.lower() == 'y':
                dbl = True
                break
            elif dbl.lower() == 'n':
                dbl = False
                break
            else:
                print("Please enter y or n")

        player.preseq(handid = 0, betid = 0, dbl = dbl, spl = False, das = das, spa = spa, rsa = rsa, maxsplits = maxsplits)



    if (das == False and dbl == False) or das == True:
        n = 0
        while n < len(action.cards):
            if action.cards[n][0] == action.cards[n][1] and player.acesplit_prohibiting == False and (maxsplits is None or action.splitcount < maxsplits):
                while True:
                    spl = input(f'Split on hand {n}: {action.cards[n]}? (y/n)')
                    if spl.lower() == 'y':
                        spl = True
                        break
                    elif spl.lower() == 'n':
                        spl = False
                        break
                    else:
                        print("Please enter y or n")

                player.preseq(handid = n, betid = n, dbl = False, spl = spl, das = das, spa = spa, rsa = rsa, maxsplits = maxsplits)
                print(f'Your new hands are {action.cards}')
                if spl == True:
                    continue
                else:
                    n += 1
            else:
                n += 1
        
        if action.splitcount == maxsplits:
            print('Maximum split amount reached')

            

    if das == True:
        for i, hand in enumerate(action.cards):
            while True:
                dbl = input(f'Double on hand {i}: {action.cards[i]}? (y/n)')
                if dbl.lower() == 'y':
                    dbl = True
                    break
                elif dbl.lower() == 'n':
                    dbl = False
                    break
                else:
                    print("Please enter y or n")

            player.preseq(handid = i, betid = i, dbl = dbl, spl = False, das = das, spa = spa, rsa = rsa, maxsplits = maxsplits)



    for i, hand in enumerate(action.cards):
        if i not in stack.doubles:
            while 6 != 7:
                yit = input(f'Hit or Stand on hand {i}: {action.cards[i]}?')
                if yit.lower() in ['hit', 'h']:
                    action.hit(i)
                    player.handval(hand)
                    if player.value > 21:
                        break
                    else:
                        continue
                elif yit.lower() in ['stand','s']:
                    break
                else:
                    print("Please enter hit (h) or stand (s)")



    for i, hand in enumerate(action.cards):
        res = game.endhand(i, h17)
        print(f'Hand {i} ends on {action.cards[i]}, {stack.bets[i]} wagered')
        if res == 'bust':
            print(f'You Busted! good boy.')
        else:
            print(f'Dealer shows {action.dealerhand[1]}')
            for i in range((len(action.dealerhand) - 2)):
                print(f'Dealer draws {action.dealerhand[i+2]}')
            print(f'Dealer ends on {action.dealerhand}')
            if res == 'dbust':
                print(f'The Dealer Busts! Nice!')
            elif res == 'lose':
                print(f'You Lose')
            elif res == 'push':
                print('Push')
            elif res == 'win':
                print('You Win!')






    if len(shoe.order)/(d*52) < pen:
        shoe.reset()