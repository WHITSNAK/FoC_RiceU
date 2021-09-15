"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level

Upper level:
ones, twos, threes, fours, fives, sixes
"""
def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all possible
    sequences of outcomes of given length.

    parameter
    ---------
    outcomes: a set of unique outcomes/states
    length: int, number of sequence to generate

    return
    ------
    set([(..), (..), ....])
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    parameter
    ---------
    hand: sorted tuple, full yahtzee hand

    return
    -------
    an integer score 
    """
    max_score = 0
    for die in set(hand):
        max_score = max(hand.count(die) * die, max_score)

    return max_score


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    parameter
    ---------
    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    return
    ------
    expected value of the entire hand
        # of held_dice + num_free_dice = # of entire hand of dice
    """
    exv = 0.0
    prob = (1./num_die_sides) ** num_free_dice  # iid prob for each possibile pair

    for pair in gen_all_sequences(range(1, num_die_sides+1), num_free_dice):
        hand = held_dice + pair
        pair_score = score(hand)
        exv += pair_score * prob

    return exv


def gen_all_holds(hand):
    """
    Generate all possible hold choices of dice given a hand.
    A hand does not neccessary need to be unique values, ex. [1,1,2,2,3]

    parameter
    ---------
    hand: full yahtzee hand

    return
    ------
    a set of tuples, where each tuple is a set of dice to hold
    """
    all_holds = set([()])  # start with empty subset
    hand_die_cnt = {die:hand.count(die) for die in set(hand)}

    for length in range(1, len(hand) + 1):
        all_seq = gen_all_sequences(hand, length)
        cor_seq = []
        for seq in all_seq:
            # remove all seq with impossible dice count
            # ex. hand(2,1), seq(2,2)
            skip = False
            for die in set(seq):
                if seq.count(die) > hand_die_cnt[die]:
                    skip = True
                    break
            
            if not skip:
                # order does not matter, remove duplicates
                sorted_seq = tuple(sorted(seq))
                cor_seq.append(sorted_seq)

        all_holds.update(cor_seq)

    return all_holds


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    parameter
    ---------
    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    return
    ------
    (expected score, a tuple of the dice to hold)
    """
    sides = num_die_sides

    best_stgy, best_val = None, None
    for hold in gen_all_holds(hand):
        nfree = len(hand) - len(hold)
        val = expected_value(hold, sides, nfree)
        
        if best_stgy is None or best_val is None or val > best_val:
            best_stgy, best_val = hold, val

    return best_val, best_stgy


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    


# run_example()
