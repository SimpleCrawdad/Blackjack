from evcalc import evcalc

ev = evcalc('A', '4')

for i, card in enumerate(ev.order):
    ev.dlrnum(card)
    print (f'''\n\n
    If the dealer shows a {card}, the dealer outcomes are as follows:
    a {round((ev.totals[0] * 100), 1)}% chance of 17
    a {round((ev.totals[1] * 100), 1)}% chance of 18
    a {round((ev.totals[2] * 100), 1)}% chance of 19
    a {round((ev.totals[3] * 100), 1)}% chance of 20
    a {round((ev.totals[4] * 100), 1)}% chance of 21
    a {round((ev.totals[5] * 100), 1)}% chance of busting
    a {round((ev.totals[6] * 100), 1)}% chance of blackjack\n\n
    ''')

print('** note that infinite deck is assumed in this simulation **\n')