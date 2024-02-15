# Python conversion
# MS Branicky, 2020-02-11

from random import random # random() generates a uniform random number in [0.0, 1.0]
from math import ceil, exp

N = 1000
k = 1001
pmut = 0.1

EVALS = 0
ELITISM = 1

"""
// Use: Metropolis Algorithm for Maximization
//
// Source: Based on the code and explanation
// of a routine for minimization found in
// Press et al., _Numerical_Recipes_in_C_,
// Cambridge Univ. Press, 1988.  Page 351.
//
// Returns a boolean value on whether or not to
// accept a reconfiguration which leads to a 
// change dE in the objective function E.
// If dE>0, returns 1 (TRUE); if dE<=0, returns
// 1 with probablity exp(dE/T), where T is a
// temperature determined by the annealing schedule.
//
"""
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
  for i in range(1,9):
    r = random()
    if r<p:
      enc[i-1] = int(ceil(random()*8))

# copy each digit of an encoding with a prob. of error p
def mutate2(src, dest, p):
  for i in range(1,9):
    r = random()
    if (r<p):
      dest[i-1] = int(ceil(random()*8))
    else:
      dest[i-1] = src[i-1]

# produces TWO offspring via crossover at a random location on two encodings (in place)
def xover(e1, e2):
  # choose a random integer c between 1 and 7, inclusive
  c = int(ceil(random()*7))
  for i in range(c+1,9):
    e1[i-1], e2[i-1] = e2[i-1], e1[i-1]

def printenc(s, encoding):
  s = str(encoding)

# test the routines
def test():
  """
  for (double T=10000000.; T>0.000001; T/=10.) {
    int i=metrop(-1.,T);
    // int j=metrop(1.,T);
    // cout << i << ", " << j << endl;
    cout << i << endl;
  }
  """
    
  # configs from R&N, p 123, 4th ed
  enc1 = [5, 6, 7, 4, 5, 6, 7, 6]
  enc2 = [8, 3, 7, 4, 2, 5, 1, 6]

  # configs from R&N, p 127, 4th ed
  enc3 = [2, 4, 7, 4, 8, 5, 5, 2]
  enc4 = [3, 2, 7, 5, 2, 4, 1, 1]
  enc5 = [2, 4, 4, 1, 5, 1, 2, 4]
  enc6 = [3, 2, 5, 4, 3, 2, 1, 3]

  # test fitness
  for enc in [enc1, enc2, enc3, enc4, enc5, enc6]:
    print("Fitness (", str(enc), ") = ", fitness(enc))
  print()

  # test mutate
  mutate2(enc1,enc2,1.0)
  print("Random Encoding: ", str(enc2))
  mutate2(enc1,enc2,0.5)
  print("Random Encoding: ", str(enc2))
  mutate2(enc1,enc2,0.0)
  print("Random Encoding: ", str(enc2))
  mutate(enc1,1.0)
  print("Random Encoding: ", str(enc1))
  mutate(enc1,0.5)
  print("Random Encoding: ", str(enc1))
  mutate(enc1,0.0)
  print("Random Encoding: ", str(enc1))
  print()

  # test xover
  print("  Parents:", str(enc3), str(enc4))
  xover(enc3,enc4)
  print("Offspring:", str(enc3), str(enc4))
  print("  Parents:", str(enc5), str(enc6))
  xover(enc5,enc6)
  print("Offspring:", str(enc5), str(enc6))
  print()

  # test successor function
  enc7 = [1, 2, 3, 4, 5, 6, 7, 8]
  enc8 = enc7[:]
  bestE = 0
  bestSuccIndex = 0
  for i in range(1,57):
    getsuccessor(enc7, i, enc8)
    f = fitness(enc8)
    # accept better always, bu accept one that is not better with some small probability
    if f>bestE or (f==bestE and random()<0.001):  
      bestE = f
      bestSuccIndex = i
    print("Successor ( ", i, " ) = ", str(enc8), ", fitness =", fitness(enc8));
  
  getsuccessor(enc7, bestSuccIndex, enc8)
  print("  Best Successor with index ", bestSuccIndex, "=", str(enc8), "has E =", bestE)

  # generate a random successor
  RandomSuccIndex = int(ceil(random()*56)) # random int in {1, 2, ..., 56}
  getsuccessor(enc7, RandomSuccIndex, enc8)
  print("Random Successor with index ", RandomSuccIndex, "=", str(enc8), "has E =", fitness(enc8))  

# the main search method. Adapted from the C example's 'main' routine.
def search():
  # create the relevant variables.
  pop = [[0 for _ in range(8)] for _ in range(k)] # the population, represented as a list of lists containing 0s.
  newpop = [[0 for _ in range(8)] for _ in range(k)] # the next population, identical to the current one.
  popE = [0 for _ in range(k)] # the population of Es. Represented by list of 0s.
  bestE = 0 # the best E, initialized as zero.
  s = ['' for _ in range(9)] # the 's' array.
  cumprobs = [0.0 for _ in range(k)] # the cumulative probabilties, represented by a list of floats initialized to 0.0.

  s[8] = 0

  # do base mutation of all of the populations.
  for i in range(k):
    mutate(pop[i], 1.0)
  
  # loop over each generation
  for t in range(1,N+1):
    # print(f"Generation {t} ... ")

    # evaluate a population's fitness
    sumE = 0 # the sum of Es
    bestind = 0 # the best index, referring to the best overall E.
    for i in range(k):
      E = fitness(pop[i]) # let E be the fitness of the population.

      sumE += E # update sumE
      popE[i] = E # set popE

      # if E is better than the previous best, update it.
      if E > bestE:
        bestE = E
        bestind = i

        # if bestE is the solution, end the program. Report the results.
        if bestE == 28:
          solution = ""
          for n in pop[i]:
            solution += str(n)
          print(f"Solution found during Generation {t}. Total Evaluations: {EVALS}. Solution: {solution}.")
          return EVALS
    
    # compute selection probabilities
    cumprobs[0] = popE[0]/sumE
    for i in range(1,k):
      cumprobs[i] = cumprobs[i-1] + (popE[i] / sumE)
    
    # selection, WITH elitism!!!
    if ELITISM:
      for j in range(8):
        newpop[0][j] = pop[bestind][j]
    
    for i in range (ELITISM, k):
      index = 0
      r = random()

      for j in range(k):
        if cumprobs[j] >= r:
          index = j
          break
      for j in range(8):
        newpop[i][j] = pop[index][j]
    
    # crossover
    for i in range(ELITISM,k,2):
      if i + 1 >= len(newpop): continue
      xover(newpop[i], newpop[i+1])
    
    # mutation
    for i in range(ELITISM,k):
      mutate2(newpop[i], pop[1], pmut)
    
    # mutation in place!
    for i in range(ELITISM,k):
      mutate(newpop[i], pmut)
    for i in range(k):
      for j in range(8):
        pop[i][j] = newpop[i][j]

if __name__ == "__main__":
  evals = []

  for i in range(100):
    print(f"Algorithm Run #{i}")
    evals.append(search())
    EVALS = 0
  
  print(f"Average # of Evaluations: {sum(evals)/len(evals)}.")