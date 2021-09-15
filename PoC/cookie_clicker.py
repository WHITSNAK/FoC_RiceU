"""
Cookie Clicker Simulator
"""
import math
import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0


# Game state class
class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = 0.0
        self._cookies = 0.0
        self._time = 0.0
        self._cps = 1.0

        # (time, item purchased, purchased tiem cost, total cookies up to date)
        self._history = [(0.0, None, 0.0, 0.0)]
        self._builds_counter = {}
        
    def __str__(self):
        """
        Return human readable state
        """
        return '<Time={:.3}, Total Cookies={:.3}, Current Cookies={:.3}, CPS={:.3}>'.format(
            self._time, self._total_cookies, self._cookies, self._cps
        )
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        """
        return self._cookies
    
    def get_cps(self):
        """
        Get current CPS
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time
        """
        return self._time
    
    def get_history(self):
        """
        Get history list

        return
        ------
        History list is a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]
        """
        return list(self._history)  # a copy, no direct reference

    def time_until(self, cookies):
        """
        Time in seconds until you have the given number of cookies
          in whole seconds
        """
        return time_needed(cookies, self._cookies, self._cps)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state
        do nothing if time <= 0.0
        """
        if time <= 0.0:
            return

        self._time += time
        cookies_inc = time * self._cps
        self._total_cookies += cookies_inc
        self._cookies += cookies_inc
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state
        Should do nothing if you cannot afford the item
        """
        if cost > self._cookies:
            return

        record = (self._time, item_name, cost, self._total_cookies)
        self._cookies -= cost
        self._cps += additional_cps
        self._history.append(record)
        self._builds_counter[item_name] = self._builds_counter.get(item_name, 0) + 1

   
# Simulation
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    builds = build_info.clone()  # a copy, no modify on the original
    state = ClickerState()
    
    while state.get_time() <= duration:
        # print 'Before', state
        t_left = duration - state.get_time()

        item = strategy(
            state.get_cookies(), state.get_cps(),
            state.get_history(), t_left, builds
        )

        # break if there no need to buy anymore
        if item is None:
            break 
    
        item_cost = builds.get_cost(item)
        item_cps = builds.get_cps(item)

        # moved to the timestamp that is able to buy build
        t_needed = state.time_until(item_cost)
        if t_needed > t_left:
            break

        # print 'Time to wait', t_needed
        state.wait(t_needed)
        
        # print 'To buy', item, item_cost, state.get_cookies()
        state.buy_item(item, item_cost, item_cps)
        builds.update_item(item)
        
        # print 'After', state

    t_left = duration - state.get_time()
    state.wait(t_left)
    return state


# helper functions
def time_needed(cost, cookies, cps):
    """
    returns number of time needed to reach certain goal

    parameter
    ---------
    goal: cost
    cookies: money
    cps: rate of money producing
    """
    return math.ceil(amount_short(cost, cookies) / cps)

def amount_short(cost, cookies):
    """
    returns how much short from a goal
    """
    return max(cost - cookies, 0.0)

def is_afforable(cost, cookies, cps, time_left):
    """
    returns whether you can afford a product within a time limit
    """
    # last time step does not produce any cookies, but not ignore
    return amount_short(cost, cookies) <= time_left * cps

def present_value(pmt, rate, npmt, n2pmt):
    """
    Calculates present value of an annuity immediate
      with no payment discounts
    """
    annu = (1.0 + (1.0 + rate) ** (-npmt)) / rate
    pval = annu * ((1.0 + rate) ** (-n2pmt)) * pmt
    return pval


# Sample Strategies
def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!
    """
    item = 'Cursor'
    item_cost = build_info.get_cost(item)
    if not is_afforable(item_cost, cookies, cps, time_left):
        return None
    return item

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None
    """
    return None

def strategy_polar(cookies, cps, history, time_left, build_info, style='low'):
    """
    General strategy for choosing either the cheapest or the most expensive item
      you can afford in the time left

    paramter
    --------
    style: 'low' for the cheapest, 'high' for the most expensive

    return
    ------
    selected item, str or None if not selected any
    """
    items = build_info.build_items()
    sel_item = None

    # oo or -oo for choosing highest or lowest
    if style == 'low':
        sel_cost = float('inf')
    elif style == 'high':
        sel_cost = float('-inf')

    for item in items:
        item_cost = build_info.get_cost(item)
        
        # check whether i can afford to buy it
        if not is_afforable(item_cost, cookies, cps, time_left):
            continue

        # choosing cheapest or most epensive
        if style == 'low':
            cond1 = item_cost < sel_cost
        elif style == 'high':
            cond1 = item_cost > sel_cost

        if cond1:
            sel_item = item
            sel_cost = item_cost
    return sel_item

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    return strategy_polar(cookies, cps, history, time_left, build_info, style='low')

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    return strategy_polar(cookies, cps, history, time_left, build_info, style='high')

def strategy_pv(cookies, cps, history, time_left, build_info):
    """
    Choose based on present value of the total cookies
    """
    items = build_info.build_items()
    max_k = None
    max_pv = float('-inf')

    discount_r = 1.2E-8
    for item in items:
        item_cost = build_info.get_cost(item)

        # skip those not afforable within the time limit
        if not is_afforable(item_cost, cookies, cps, time_left):
            continue

        item_cps = build_info.get_cps(item)
        t_needed = time_needed(item_cost, cookies, cps)
        present_val = present_value(item_cps, discount_r, time_left - t_needed, t_needed)
        
        if max_k is None or present_val > max_pv:
            max_k, max_pv = item, present_val
    
    return max_k

def strategy_cphd(cookies, cps, history, time_left, build_info):
    """
    Cookir Clicker strategy
    Choose the build based on the highest Cookies per Hour per Dollar metric
    """
    items = build_info.build_items()
    max_k = None
    metric = float('-inf')

    for item in items:
        item_cost = build_info.get_cost(item)

        # skip those not afforable within the time limit
        if not is_afforable(item_cost, cookies, cps, time_left):
            continue

        item_cps = build_info.get_cps(item)
        item_cphd = item_cps*60*60 / item_cost
        
        if max_k is None or item_cphd > metric:
            max_k, metric = item, item_cphd
    
    return max_k

# best of all
def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy
    """
    return strategy_cphd(cookies, cps, history, time_left, build_info)



# Run it babe
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state
    
    # more information
    if strategy_name == 'CPHD':
        info = provided.BuildInfo()
        print 'Total Cookies', state._total_cookies
        for k,v in state._builds_counter.items():
            print k, v, '{:.3}'.format(info.get_cost(k) * 1.15**v)
        print

    import matplotlib.pyplot as plt
    history = state.get_history()
    xhis = [item[0] for item in history]
    yhis = [item[3] for item in history]
    plt.plot(xhis, yhis, label=strategy_name)
    plt.legend()

def run():
    """
    Run the simulator.
    """    
    # run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)
    # run_strategy("Nonthing", SIM_TIME, strategy_none)
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("PV", SIM_TIME, strategy_pv)
    run_strategy("CPHD", SIM_TIME, strategy_cphd)


run()
