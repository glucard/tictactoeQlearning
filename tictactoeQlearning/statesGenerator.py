import tictactoe
import random, copy
from collections import Counter

def listOfActions():
    actions = []
    for i in range(3):
        for j in range(3):
            actions.append((j, i))
    return actions

class TictactocStates():
    def __init__(self):
        self.reset()

    def reset(self):
        self.actions = listOfActions()
        epoch = [0]
        self.states = []
        game_start_state = tictactoe.TicTacToe()
        self.stateGenerator(game_start_state)
        for state in self.states:
            self.canWin(state)
        self.not_finished_states = [state for state in self.states
                                    if state['done'] == False]

    def find(self, game_state):
        rotations_encoded = []
        for i in range(4):
            rotations_encoded.append(game_state.encode())
            game_state.rotate()

        id = 0
        for state in self.states: 
            id += 1
            for encoded in rotations_encoded:
                if state['encoded'] == encoded:
                    return True, state['id']
        return False, id

    def canWin(self, state):
        wins = 0
        for next_state in [self.states[id] for id in state['actions']]:
            if next_state['done'] == True:
                wins += 1
        state['possible_wins'] = wins

    def stateGenerator(self, game_state):
        encoded = game_state.encode()
        exist, id = self.find(game_state)
        if id % 1000 == 0:
            print(id)
        if not exist:
            done = not game_state.notFinished()
            state_element = {
                'id': id,
                'encoded': encoded,
                'actions': [],
                'done': done
            }
            self.states.append(state_element)
            if not done:
                for i in range(9):
                    next_state_game = copy.deepcopy(game_state)
                    action = id
                    if next_state_game.mark(self.actions[i][0], self.actions[i][1]):
                        action = self.stateGenerator(next_state_game)
                    state_element['actions'].append(action)
        return id


tstates = TictactocStates()
textfile = open("states.txt", "w")
for element in tstates.states:
    textfile.write("id: " + str(element['id']) + "\n")
    textfile.write("encoded: " + element['encoded'] + "\n")
    textfile.write("actions: " + str(element['actions']) + "\n")
    textfile.write("possible_wins: " + str(element['possible_wins']) + "\n")
    textfile.write("done: " + str(element['done']) + "\n" + "\n")
textfile.close()