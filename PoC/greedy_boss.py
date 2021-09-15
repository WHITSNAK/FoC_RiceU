"""
Simulator for the following scenario

Let's say you have a job that pays a salary of $100 a day.
You know your boss can be bribed to increase your salary to $200 dollars a day if you pay him $1000.
How long would it take you to earn $1000 for the bribe?
How much would you paid be after the bribe?
Here is a good question to get you thinking in the right direction.
If you bribed your boss as soon as you have enough money saved up for the bribe,
  how much money would you have earned (bribes included) in 20 days?

Now, what happens if your boss is really greedy and will increase your salary by $100 dollar per day
  every time you give him $1000 dollars?
How fast would your salary increase?

Finally, let say that your boss is both greedy and smart.
He wants a bigger bribe every time he increases your salary.
What would happen?

That is basically the scenario in Cookie Clicker.
"""
"""
Simulator for greedy boss scenario
"""
# import simpleplot
import math

STANDARD = True
LOGLOG = False

# constants for simulation
INITIAL_SALARY = 100.
SALARY_INCREMENT = 100.
INITIAL_BRIBE_COST = 1000.


def greedy_boss(days_in_simulation, bribe_cost_increment, plot_type=STANDARD):
    """
    Simulation of greedy boss
    """
    salary = INITIAL_SALARY
    bribe_cost = INITIAL_BRIBE_COST
    net_earned = 0
    total_bribed = 0
    current_day = 0

    # define  list consisting of days vs. total salary earned for analysis
    days_vs_earnings = []

    # Each iteration of this while loop simulates one bribe
    while current_day <= days_in_simulation:
        if plot_type == STANDARD:
            data = current_day, net_earned + total_bribed
        elif plot_type == LOGLOG:
            try:
                data = math.log(current_day), math.log(net_earned + total_bribed)
            except ValueError:  # log does not get 0
                data = (0 ,0)

        while net_earned >= bribe_cost:  # maybe multiple bribes
            net_earned -= bribe_cost
            total_bribed += bribe_cost
            salary += SALARY_INCREMENT
            bribe_cost += bribe_cost_increment

        days_vs_earnings.append(data)

        days_to_bribe = max(math.ceil((bribe_cost - net_earned) / float(salary)), 1)
        current_day += days_to_bribe
        net_earned += salary * days_to_bribe

    return days_vs_earnings


def run_simulations():
    """
    Run simulations for several possible bribe increments
    """
    plot_type = STANDARD
    days = 70
    inc_0 = greedy_boss(days, 0, plot_type)
    inc_500 = greedy_boss(days, 500, plot_type)
    inc_1000 = greedy_boss(days, 1000, plot_type)
    inc_2000 = greedy_boss(days, 2000, plot_type)
    simpleplot.plot_lines("Greedy boss", 600, 600, "days", "total earnings", 
                          [inc_0, inc_500, inc_1000, inc_2000], False,
                         ["Bribe increment = 0", "Bribe increment = 500",
                          "Bribe increment = 1000", "Bribe increment = 2000"])

run_simulations()

print greedy_boss(35, 100)
# should print [(0, 0), (10, 1000), (16, 2200), (20, 3400), (23, 4600), (26, 6100), (29, 7900), (31, 9300), (33, 10900), (35, 12700)]

print greedy_boss(35, 0)
# should print [(0, 0), (10, 1000), (15, 2000), (19, 3200), (21, 4000), (23, 5000), (25, 6200), (27, 7600), (28, 8400), (29, 9300), (30, 10300), (31, 11400), (32, 12600), (33, 13900), (34, 15300), (34, 15300), (35, 16900)]
