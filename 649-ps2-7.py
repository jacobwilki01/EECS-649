import math

class Environment:
    def __init__(self, location: int, is_a_clean: bool, is_b_clean: bool):
        self.location : int = location # 0 if in A, 1 if in B
        self.aClean : bool = is_a_clean
        self.bClean : bool = is_b_clean
        self.score = 0
    
    def iterate(self) -> None:
        self.score += 0 if self.aClean else 1
        self.score += 0 if self.bClean else 1

        print(f"Location of the vacuum: {'Room A' if self.location == 0 else 'Room B'}")
        print(f"State of Room A: {'Clean' if self.aClean else 'Dirty'}")
        print(f"State of Room B: {'Clean' if self.bClean else 'Dirty'}")
        print(f"Current Score: {self.score}")

        # A, Clean = Right
        # A, Dirty = Clean
        if self.location == 0:
            if self.aClean:
                self.location = 1
            else:
                self.aClean = True
        
        # B, Clean = Left
        # B, Dirty = Clean
        else:
            if self.bClean:
                self.location = 0
            else:
                self.bClean = True

def main():
    locations = [0,1]
    statesOfA = [True, False]
    statesOfB = [True, False]

    env_num = 1
    scores = []

    for location in locations:
        for stateOfA in statesOfA:
            for stateOfB in statesOfB:
                env = Environment(location, stateOfA, stateOfB)

                print(f"========Environment #{env_num}========")
                for i in range(9):
                    env.iterate()
                
                print(f"Final Score: {env.score}")
                scores.append(env.score)
                env_num += 1
    
    print(f"Average Score: {sum(scores)/len(scores)}")

if __name__ == "__main__":
    main()