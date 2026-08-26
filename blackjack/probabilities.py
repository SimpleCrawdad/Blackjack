from gameclasses import *
import pandas as pd
from pathlib import Path


output_dir = Path('CSV_output')
output_dir.mkdir(exist_ok=True)

order = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
decks = [1,2,4,6,8]



############################################################
# CREATE DECK PROBABILITIES for s17 and h17 -- j decks
############################################################

for j in decks:
    prob = Probability(j)
    df = pd.DataFrame()

    for i in order:
        dealer = Dealer()
        prob.dealerev(dealer, h17 = False, card = i)
        df[i] = prob.probtotals
        prob.setprob()

    df = round(df*100, 3)
    df.to_csv(f'CSV_output/s17_{j}deck.csv')

############################################################
# NEW CSV
############################################################

    df = pd.DataFrame()

    for i in order:
        dealer = Dealer()
        prob.dealerev(dealer, h17 = True, card = i)
        df[i] = prob.probtotals
        prob.setprob()


    df = round(df*100, 3)
    df.to_csv(f'CSV_output/h17_{j}deck.csv')