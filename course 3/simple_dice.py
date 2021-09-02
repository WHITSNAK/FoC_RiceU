"""
Simple dice game
Give out $10 to play the game
    3 dice
    roll doubles gain $10
    roll triple gain $200
    others deal keeps the $10

Good game to play?
"""

# %%
import random
from utils import gen_all_sequences

# exhasutive search and counting method
def search_all_expected_value(num_dice):
    DICE_OUTCOME = range(1, 7)

    total_val = 0
    cnt = 0
    for dice in gen_all_sequences(DICE_OUTCOME, num_dice):
        total_val += get_net_value(dice)
        cnt += 1

    expected = total_val / cnt
    return expected

# Monte Carlo Simulation method
def mc_trial():
    return [random.randrange(1,7), random.randrange(1,7), random.randrange(1,7)]

def get_net_value(dice):
    net = -10.
    unique_values = set(dice)
    for val in unique_values:
        if dice.count(val) == 2:
            net += 10.
        elif dice.count(val) == 3:
            net += 200.
        else:
            net += 0.
    return net

def mc_simu(ntrials):
    expected = 0.
    for _ in range(ntrials):
        expected += get_net_value(mc_trial())
    
    return expected / ntrials

# %%
import pandas as pd
import matplotlib.pyplot as plt

# run 500 times each with 10k trials
sr = pd.Series([mc_simu(1000) for _ in range(5000)])

# plot it out
print 'Mean', sr.mean()
sr.plot.hist(bins=15)
plt.show()

# %%
print search_all_expected_value(3)
