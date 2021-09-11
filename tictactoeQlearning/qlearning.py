import statesGenerator, tictactoe
import numpy, random, time

def futureState(q_table, state, steps):
    
    for i in range(steps):
        if len(state['actions'] ) > 0:
            action = numpy.argmax(q_table[state['id']])
            state = sg.states[state['actions'][action]]
        else:
            return 0
    return numpy.argmax(q_table[state['id']])

sg = statesGenerator.TictactocStates()

q_table = numpy.zeros([len(sg.states), len(sg.actions)])

alpha = 0.1
gamma = 0.6
epsilon = 0.1

epochs, penalties = 0, 0

for i in range(1000000):
    state = random.choice(sg.not_finished_states)
    done = False

    if i % 10000 == 0:
        print(i / 10000)

    while not done:
        if not '-' in state['encoded']:
            break
        if random.uniform(0, 1) < epsilon:
            action = random.randrange(0, len(state['actions']))
        else:
            action = numpy.argmax(q_table[state['id']])
        
        next_state = sg.states[state['actions'][action]]

        value = q_table[state['id']][action]
        next_max = numpy.max(q_table[next_state['id']])
        if state['id'] == next_state['id']:
            reward = -100
        else:
            reward = -1 + next_state['possible_wins'] * -10
        new_value = (1 - alpha) * value + alpha * (reward + -gamma * (next_max + futureState(q_table, state, 3) + futureState(q_table, state, 5) + futureState(q_table, state, 7) + futureState(q_table, state, 9)) + gamma * (futureState(q_table, state, 2) + futureState(q_table, state, 4) + futureState(q_table, state, 6) + futureState(q_table, state, 8)))
        q_table[state['id']][action] = new_value

        penalties += next_state['possible_wins']

        state = next_state
        done = state['done']
        epochs += 1

print(penalties / epochs)

epochs, penalties = 0, 0
for i in range(10000):
    state = sg.states[0]
    done = False
    #is_player = bool(input("bool True False: "))
    while not done:
        if not '-' in state['encoded']:
            break
        """if is_player:
            print(tictactoe.TicTacToe.Render(state['encoded']).string())
            action = int(input("Select action ("+str(state['actions'])+"): "))
        else:
            action = numpy.argmax(q_table[state['id']])
        is_player = not is_player"""
        action = numpy.argmax(q_table[state['id']])    
        
        next_state = sg.states[state['actions'][action]]

        penalties += next_state['possible_wins']
        if state['id'] == next_state['id']:
            print("ja era")

        state = next_state
        done = state['done']
        epochs += 1
        print(tictactoe.TicTacToe.Render(state['encoded']).string())
        time.sleep(5)

print(penalties / epochs)

