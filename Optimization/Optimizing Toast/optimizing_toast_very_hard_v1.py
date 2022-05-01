################################################################################
# Problem Setup: You want the perfect bread
# What influences this?
#  - how long do you toast it?
#  - how long after toasting do you eat the bread?
#  - Do you have power? And how much? 
#  - Which toaster do you use?
################################################################################

import math
import operator
import random
import numpy as np

################################################################################
# the function you are supposed to optimize.
# It has the following input:
#  toast_duration: duration of toasting in seconds. It is supposed to be an integer between 1 and 100
#  wait_duration: duration of waiting after toasting in seconds. It's supposed to be an integer between 1 and 100
#  toaster: the number of the toaster you want to use. It's supposed to be an integer, between 1 and 10.
#  power: how much power the toaster has (it's supposed to be a floating point number between 0 and 2)
################################################################################
def utility(toast_duration, wait_duration, power = 1.0,toaster = 1):
    # handle input errors
    if (not type(toast_duration) is int) and not (1 <= toast_duration <= 100):
        raise ValueError("toast_duration is not an integer")
    if (not type(wait_duration) is int) and not (1 <= wait_duration <= 100):
        raise ValueError("wait_duration is not an integer")
    if (not type(toaster) is int) and not (1 <= toaster <= 10):
        raise ValueError("toaster is not an integer or is not in a valid range")
    if (not type(power) is float) and not (0.0 <= power <= 2.0):
        raise ValueError("power is not a float or not in the valid range")

    # get toaster specific configuration
    hpt = [10,8,15,7,9,2,9,19,92,32][1 + toaster]
    hpw = [1,4,19,3,20,3,1,4,1,62][1 + toaster]
    toaster_utility = [1,0.9,0.7,1.3,0.3,0.8,0.5,0.8,3,0.2][1 + toaster]

    # calculate values
    toast_utility = -0.1*(toast_duration-hpt)**2+1
    wait_utility = -0.01*(wait_duration-hpw)**2+1
    overall_utility = (toast_utility + wait_utility) * toaster_utility

    # apply modifier based on electricity
    power_factor = math.sin(10*power+math.pi/2 -10) + power*0.2
    overall_utility *= power_factor

    return overall_utility


################################################################################
# Writing this function is your homework. 
# The function should return the tuple of parameters that optimizes the function.
# 
# You can implement it in multiple difficulty levels:
# easy: 
#     - implement it with only two parameters: toast_duration and wait_duration
#     - e.g., utility(2,3)
#     - Implement the function by testing all possible values for these variables.
#     - (This state space has only 10000 values, so it shouldn't take too long)
#
# medium: 
#    - same as easy, but implement hill climbing
#    - see pseudo code
#
# hard: 
#    - also use the parameter power
#    - e.g., utility(2,3,1.2)
#    - this introduces the following complications:
#        - multiple maxima
#        - a continuous parameter
#    - implement gradient ascent
#
# very hard:
#    - Same as hard, but use repeated search to find all maxima. 
#    - repeated search: 
#        - apply gradient descent from different starting points.
#    - I think there are 5 maxima. But I'm not sure :-P
#
# prepare to cry:
#    - find the optimum for all four parameters
#    - define your own algorithm!


def select_initial_solution():
    # create and return random 3-tuple
    return(random.randint(1, 100), random.randint(1, 100), random.random()*2)


def get_gradient(toast_duration, wait_duration, power):

    # get gradient by calculateing the partial derivative
    gradient_toast_duration = int(round(0.7*(math.sin(10*power + math.pi/2 - 10) + 0.2*power) * (-0.2*toast_duration + 3)))
    gradient_wait_duration = int(round(10*(0.7*(math.sin(10*power + math.pi/2 - 10) + 0.2*power) * (-0.02*wait_duration + 0.38))))
    # setting alpha to 0.00001
    alpha = 0.000001
    gradient_power = alpha*(0.7*(-0.1*toast_duration**2 + 3*toast_duration + 0.38*wait_duration - 0.01*wait_duration**2 - 24.11) * (math.cos(10*power + math.pi/2 - 10) * 10 + 0.2))

    # check if current solution + gradients step over the boundaries
    if 1 <= toast_duration + gradient_toast_duration <= 100:
        y_1 = gradient_toast_duration
    else:
        y_1 = 0

    if 1 <= wait_duration + gradient_wait_duration <= 100:
        y_2 = gradient_wait_duration
    else:
        y_2 = 0

    if 0 <= power + gradient_power <= 2:
        y_3 = gradient_power
    else:
        y_3 = 0

    # return gradients
    return(y_1, y_2, y_3)


def distance(current_solution, next_state):
     # calculate and then return the distance from current solution to next solution
     d = abs(utility(*current_solution) - utility(*next_state))
     return d


def find_maximum():
    # Initializes a starting point
    current_solution = select_initial_solution()

    # as long as we have new states to visit, visit them
    while True:

        # calculate and add gradient
        gradient = get_gradient(*current_solution)

        #next_state = current_solution + gradient
        next_state = tuple(map(operator.add, current_solution, gradient))

        # if we haven't moved much we are finished (0.001 is an arbitrary value here)
        if (distance(current_solution, next_state) <= 0.000001):
             break
        
        # set current_solution to next_state for the next iteration
        current_solution = next_state
        
    return current_solution


# set initial values for optima
value_one = -100
optimum_one = (-1, -1, -1)
value_two = -100
optimum_two = (-1, -1, -1)
value_three = -100
optimum_three = (-1, -1, -1)
value_four = -100
optimum_four = (-1, -1, -1)
value_five = -100
optimum_five = (-1, -1, -1)

# find all 5 optima by initializing a number of randomly selected points (10)
for i in range(10):
    optimum = find_maximum()
    value = utility(*optimum)

    # check if value falls in on of the following optima categories
    if value <= 6:
        # select the bigest value in the given category 
        if value >= value_one:
            optimum_one = optimum
            value_one = value

    elif 8 <= value <= 58:
        # select the bigest value in the given category 
        if value >= value_two:
            optimum_two = optimum
            value_two = value
    
    elif 308 <= value <= 337:
        # select the bigest value in the given category 
        if value >= value_three:
            optimum_three = optimum
            value_three = value
        
    elif 371 <= value <= 406:
        # select the bigest value in the given category 
        if value >= value_four:
            optimum_four = optimum
            value_four = value
    
    elif 434 <= value:
        # select the bigest value in the given category 
        if value >= value_five:
            optimum_five = optimum
            value_five = value
    

# look for all 5 optima
# if value is not initial value (-100) you found a optimum
if not value_one == -100:
    print("\nFound a local optimum at: " f"{optimum_one}")
    print("With a value of: " f"{value_one}")
    
if not value_two == -100:
    print("\nFound a local optimum at: " f"{optimum_two}")
    print("With a value of: " f"{value_two}")
    
if not value_three == -100:
    print("\nFound a local optimum at: " f"{optimum_three}")
    print("With a value of: " + f"{value_three}")
    
if not value_four == -100:
    print("\nFound a local optimum at: " f"{optimum_four}")
    print("With a value of: " f"{value_four}")
    
if not value_five == -100:
    print("\n\nFound a global optimum at: " f"{optimum_five}")
    print("With a value of: " f"{value_five}")


