from random import random, randint # Import randint for generating random integers
from math import ceil, exp

N = 1000
k = 1001
pmut = 0.1

EVALS = 0
ELITISM = 1

def metrop(dE, T):
  r=random()
  return (dE>0) or (r<exp(dE/T))

# returns 1 if queens q1 and q2 are attacking each other, 0 o.w.
def attacking(q1col, q1row, q2col, q2row):
  if q1col==q2col:
    return 1  # same column
  if q1row==q2row:
    return 1  # same row
  coldiff=q1col-q2col
  rowdiff=q1row-q2row
  if abs(coldiff)==abs(rowdiff):
    return 1  # same diagonal
  return 0 

# evaluates the fitness of an encoding, defined as the number of
# non-attacking pairs of queens (28 - number of attacking pairs)
#
# the global variable EVALS keeps track of the number of times called
def fitness(encoding):
  global EVALS
  EVALS += 1
  E = 28
  for i in range(1,8):
    for j in range(i+1,9):
      E -= attacking(i, encoding[i-1], j, encoding[j-1])
  return E

# the following is useful in a variety of algorithms
# returns the nth successor of an encoding
def getsuccessor(init, n, succ):
  n -= 1
  quotient, remainder = divmod(n,7) 
  newrow=init[quotient]+remainder+1
  if newrow>8:
    newrow -= 8
  for j in range(8):
    if j==quotient:
      succ[j]=newrow
    else:
      succ[j]=init[j]

# copy each digit of an encoding with a prob. of error p (in place)
def mutate(enc, p):
    for i in range(1, 9):
        r = random()
        if r < p:
            enc[i-1] = randint(1, 8)

# generated with help from chat gpt. Asked for explanation and example of cyclic selection.
def mutate2(src, dest, p):
    for i in range(1, 9):
        r = random()
        if (r < p):
            dest[i - 1] = int(ceil(random() * 8))
        else:
            dest[i - 1] = src[i - 1]

# produces TWO offspring via crossover at a random location on two encodings (in place)
def xover(e1, e2):
  # choose a random integer c between 1 and 7, inclusive
  c = int(ceil(random()*7))
  for i in range(c+1,9):
    e1[i-1], e2[i-1] = e2[i-1], e1[i-1]

# main search method. Adapted and modified from the C example's main routine.
def search(mode : str) -> int:
    pop = [[randint(1, 8) for _ in range(8)] for _ in range(k)] # the population
    newpop = [[0 for _ in range(8)] for _ in range(k)] # the next population
    popE = [0 for _ in range(k)] # the population of Es, represented by 0s
    bestE = 0 # the best E, initialized to zero
    cumprobs = [0.0 for _ in range(k)] # the cumulative probabilities of the generation

    # loop over each generation
    for t in range(1, N+1):
        
        # evaluation a population's fitness
        sumE = 0 # sum of Es
        bestind = 0 # the best index, referring to the best overall E.
        for i in range(k):
            E = fitness(pop[i]) # let E be the fitness of the population.

            sumE += E # update sumE
            popE[i] = E # set popE

            if E > bestE: # if E is better, update
                bestE = E
                bestind = i

                # if E is the solution, return
                if bestE == 28:
                    solution = "".join(map(str, pop[i]))
                    print(f"Solution found during Generation {t}. Total Evaluations: {EVALS}. Solution: {solution}.")
                    return EVALS

        # cumulative selection probabilities
        cumprobs[0] = popE[0] / sumE
        for i in range(1, k):
            cumprobs[i] = cumprobs[i-1] + (popE[i] / sumE)

        # selection with elitism
        if ELITISM:
            for j in range(8):
                newpop[0][j] = pop[bestind][j]

        for i in range(ELITISM, k):
            index = 0
            r = random()

            for j in range(k):
                if cumprobs[j] >= r:
                    index = j
                    break
            for j in range(8):
                newpop[i][j] = pop[index][j]

        # crossover
        for i in range(ELITISM, k, 2):
            if i + 1 >= len(newpop):
                continue
            xover(newpop[i], newpop[i+1])

        # mutation, min-conflicts based on the two types of selection
        if mode == "random":
          for i in range(ELITISM, k):
            mutate(newpop[i], pmut)
        else:
          for i in range(ELITISM, k):
            mutate2(newpop[i], pop[1], pmut)

        # mutation in place
        for i in range(k):
            for j in range(8):
                pop[i][j] = newpop[i][j]
  
    print("Solution not found... :(")
    return -1 # if failure, return -1 so it is not included in the sucessful solutions

if __name__ == "__main__":
    print("Select Mode:\n1) Random Selection\n2) Cyclic Selection")
    selection = input("Select Mode (1 or 2): ")

    if selection == 1:
       mode = "random"
       print("==========RANDOM SELECTION==========")
    else:
       mode = "cyclic"
       print("==========CYCLIC SELECTION==========")

    evals = []

    for i in range(10):
        print(f"Algorithm Run #{i+1}")
        solution = search(mode)

        if solution > 0:
          evals.append(solution)
        EVALS = 0
      
    # normalize data by removing high and low.
    evals.remove(max(evals))
    evals.remove(min(evals))

    print(f"Average # of Evaluations: {round(sum(evals)/len(evals), 0)}.")