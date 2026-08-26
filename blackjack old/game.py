from shoe import shoe, stack

while True:
    try:
        d = int(input('How many decks are you playing?'))
        break
    except ValueError:
        print("Please enter a valid number")

while True:
    try:
        ss = float(input('How many chips are you buying?'))
        break
    except ValueError:
        print("Please enter a fraction")

stack = stack(ss)
shoe1 = shoe(d)
shoe1.shuffle()

while 1==1:

    ############################################################
    # INITIAL DEAL AND BET
    ############################################################
    shoe1.deal()
    print(f"\n\nNEW DEAL\n\n")
    print(f'You have {stack.size} chips')

    while True:
        try:
            bet = float(input('What is your bet?'))
            break
        except ValueError:
            print("Please enter a number")

    stack.entbet(bet)


    print(f'You bet {bet} chips')

    print(f'You Are Dealt {shoe1.cards}')
    print(f'Dealer Shows {shoe1.dealerup}')

    ############################################################
    # CHECK FOR BLACKJACKS
    ############################################################

    shoe1.bjcheck()

    if shoe1.playerbj and shoe1.dealerbj:
        print('Two Blackjacks, Push')
        stack.push()
        continue

    elif shoe1.playerbj:
        print('Blackjack!')
        stack.blackjack(1.5)
        continue

    elif shoe1.dealerbj:
        print(f'Dealer Shows {shoe1.dealerdown}')
        print('FUCK YOU')
        stack.lose()
        continue

    else:
        print('No Blackjack')

    ############################################################
    # CHECK IF SPLITS ARE AVAILABLE // RESOLVE SPLITS
    ############################################################

    shoe1.splcheck()
    nose = []

    while shoe1.spavailable:

        shoe1.spvloc = [x for x in shoe1.spvloc if x not in nose]
        if shoe1.spvloc == []:
            break

        for i in shoe1.spvloc:
            item = shoe1.cards[i]

            spl = input(f"Would you like to split hand {i}: {item}? (y/n)")

            if spl == 'y':
                shoe1.split(i)
                print(f'Your Cards Are {shoe1.cards}')
            elif spl == 'n':
                nose.append(i)
            else:
                print("Error, Return (y/n)")

        shoe1.splcheck()

    ############################################################
    # DOUBLES
    ############################################################

    bustcounter = 0

    for i in range(len(shoe1.cards)):
        item = shoe1.cards[i]
        dbl = input(f"Would you like to double on hand {i}: {item}? (y/n)")

        if dbl == "y":
            print("Your bet has been doubled!")
            shoe1.double(i)
            print(f"Your Hand is {shoe1.cards[i]}")
            shoe1.valchk(i)

            if shoe1.value > 21:
                print("BUST")

                stack.lose()
                stack.lose()

                del shoe1.cards[i]
                bustcounter += 1

        elif dbl == "n":
            continue

        else:
            print("Please Enter (y/n)")


    if bustcounter >= len(shoe1.cards):
        continue

    ############################################################
    # HIT OR STAND
    ############################################################

    for i in range(len(shoe1.cards)):
        item = shoe1.cards[i]

        if i not in shoe1.doublist:

            while 1 == 1:
                ans = input(f"Hit or Stand on hand {i}: {item}")
                if ans.lower() == "hit":
                    shoe1.hit(i)
                    print(f'Your Cards Are {shoe1.cards}')
                    shoe1.valchk(i)
                    if shoe1.value > 21:
                        print("BUST (rip bozo)")     
                        stack.lose()
                        del shoe1.cards[i]
                        bustcounter += 1
                        break
                elif ans.lower() == "stand":
                    shoe1.valchk(i)        
                    break
                else:
                    print("Please Enter Either Hit or Stand.")

    if bustcounter >= len(shoe1.cards):
        continue

    ############################################################
    # DEALER PLAY
    ############################################################

    print(f'Dealer shows {shoe1.dlist}')

    shoe1.dchk()

    print(f'Dealer ends with {shoe1.dlist}')

    ############################################################
    # SETTLE WINS AND LOSSES
    ############################################################

    if shoe1.dvalue > 21:
        print("Dealer Busts!")
        for i in range(len(shoe1.cards)):
            stack.win()
            if i in shoe1.doublist:
                stack.win()
                print("Nice Double!")
        print(f"You now have {stack.size} chips")
    else:
        for i in range(len(shoe1.cards)):
            item = shoe1.cards[i]
            shoe1.valchk(i)
            if shoe1.value > shoe1.dvalue:
                print(f"You win with {item}")
                stack.win()
                if i in shoe1.doublist:
                    stack.win()
                    print("Nice Double!")
            elif shoe1.value == shoe1.dvalue:
                print(f"Push with {item}")
            else:
                print(f"You lose with {item}")
                stack.lose()
                if i in shoe1.doublist:
                    stack.lose()
                    print("Bad Double!")