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


def select_initial_solution(toaster):
    # create and return random 4-tuple
    return(random.randint(1, 100), random.randint(1, 100), random.random()*2, toaster)


def get_max_neighbor(current_solution):

    # get all neighbors
    x_min = (current_solution[0] - 1, current_solution[1], current_solution[2], current_solution[3])
    x_max = (current_solution[0] + 1, current_solution[1], current_solution[2], current_solution[3])
    y_min = (current_solution[0], current_solution[1] - 1, current_solution[2], current_solution[3])
    y_max = (current_solution[0], current_solution[1] + 1, current_solution[2], current_solution[3])

    neighbors = (x_min, x_max, y_min, y_max)

    # calculate utility for all neighbors
    solutions = (utility(*x_min), utility(*x_max), utility(*y_min), utility(*y_max))

    # get the index of the max utility
    index = solutions.index(max(solutions))
    # check if neighbor solution is better than current
    if solutions[index] > utility(*current_solution): 
        # check if neighbor is out of range
        if x_min[0] < 1 or x_min[1] < 1 or y_min[0] < 1 or y_min[1] < 1 or x_max[0] > 100 or x_max[1] > 100 or y_max[0] > 100 or y_max[1] > 100:
            return current_solution
        else:
            return neighbors[index]
    else:
        # return neighbor at the same index
        return current_solution


def get_gradient(toast_duration, wait_duration, power, toaster):

    # get toaster specific configuration
    hpt = [10,8,15,7,9,2,9,19,92,32][1 + toaster]
    hpw = [1,4,19,3,20,3,1,4,1,62][1 + toaster]
    toaster_utility = [1,0.9,0.7,1.3,0.3,0.8,0.5,0.8,3,0.2][1 + toaster]

    # get gradient by calculateing the partial derivative
    # setting learning rate alpha to 0.000001
    alpha = 0.000001
    gradient_power = alpha*(toaster_utility*(-0.1*toast_duration**2 + 0.2*toast_duration*hpt + 0.02*wait_duration*hpw + 2 - 0.1*hpt**2 - 0.01*wait_duration**2 - 0.01*hpw**2) * (-1*math.cos(10*power)*10 + 0.2))

    # check if current solution + gradients step over the boundaries
    if 0 <= power + gradient_power <= 2:
        # return gradient_power
        return(0, 0, gradient_power, 0)
    else:
        # return gradient_power = 0
        return(0, 0, 0, 0)


def distance(current_solution, next_state):
     # calculate and then return the distance from current solution to next solution
     d = abs(utility(*current_solution) - utility(*next_state))
     return d


def find_maximum():
    max_solution = (0,0,0,0)

    # loop through toaster specific configurations
    for toaster in range(-1, 9):
        # Initializes a starting point
        current_solution = select_initial_solution(toaster)
        
        # as long as we have new states to visit, visit them
        while True:

            # calculate the highest neighbor
            next_solution = get_max_neighbor(current_solution)
            # calculate gradient
            gradient = get_gradient(*current_solution)

            # add highest neighbor and gradient
            next_state = tuple(map(operator.add, next_solution, gradient))

            # if we haven't moved much we are finished (0.001 is an arbitrary value here)
            if (distance(current_solution, next_state) <= 0.001):
                # checks if optimum in current toaster specific configurations is bigger than the one before
                if utility(*current_solution) > utility(*max_solution):
                    max_solution = current_solution
                break
            
            # set current_solution to next_state for the next iteration
            current_solution = next_state
            
    return max_solution


# use the function and see what it thinks the optimum is
optimum = find_maximum()
print("Optimum:",optimum,)
print("value:",utility(*optimum))
