"""
The template of the script for playing the game in the ml mode
"""
import random
import json
import os
import dataclasses

@dataclasses.dataclass
class GameState:
    distance: tuple
    position: tuple
    surroundings: str
    food: tuple

class MLPlay:
    def __init__(self):
        '''
        self.display_width = display_width
        self.display_height = display_height
        self.block_size = block_size
        '''
        self.game_count = 0
        # Learning parameters
        self.epsilon = 0.001
        self.lr = 0.7
        self.discount = 0.5
        #0.5->11 0.6->15 0.7->21 0.8->32 0.9->67
        # State/Action history
        self.qvalues = self.LoadQvalues()
        self.history = []

        # Action space
        self.actions = {
            0:'LEFT',
            1:'RIGHT',
            2:'UP',
            3:'DOWN'
        }
        self.previous_surroundings = "2000"
        self.preprevios_surroundings = "2000"

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] == "GAME_OVER":
            return "RESET"
        '''
        "frame": self._frame,
        "status": self._status.value,
        "snake_head": self._snake.head_pos,
        "snake_body": [body.pos for body in self._snake.body],
        "food": self._food.pos
        return "LEFT"
        return "RIGHT"
        return "UP"
        return "DOWN"
        '''
        if self.game_count<100:
            self.epsilon = 0.001
            self.lr = 0.7
        elif self.game_count<200:
            self.lr = 0.6
        elif self.game_count<400:
            self.epsilon = 0.0001
            self.lr = 0.5
        elif self.game_count<800:
            self.lr = 0.4
        elif self.game_count<1600:
            self.epsilon = 0.00001
            self.lr = 0.3
        elif self.game_count<3200:
            self.lr = 0.2
        else:
            self.epsilon = 0.000001
            self.lr = 0.1
        state = self._GetState(scene_info)
        #print(state)
        # Epsilon greedy
        rand = random.uniform(0,1)
        state_scores = self.qvalues[self._GetStateStr(state)]
        if rand < self.epsilon:
            action_key = random.choices(list(self.actions.keys()))[0]
            print("RandRandRand")
        elif rand <  self.epsilon*11 :
            Second_Max = sorted(state_scores,reverse = True)[1]
            action_key = state_scores.index(Second_Max)
            print("Second_Max")
        else:
            Max = sorted(state_scores,reverse = True)[0]
            action_key = state_scores.index(Max)
            '''
            Max_score = sorted(state_scores,reverse = True)
            #print(state_scores)
            #print(self._Surroundings(scene_info))
            #print(Max_score)
            action_key = 3
            for score in Max_score:
                if self._Surroundings(scene_info)[state_scores.index(score)]!="1":
                    action_key = state_scores.index(score)
                    break
            '''
        #print(state_scores)

        action_val = self.actions[action_key]
        
        # Remember the actions it took at each state
        self.history.append({
            'state': state,
            'action': action_key
            })
        #print(action_val)
        self.UpdateQValues()

        return action_val
        
    def reset(self):
        """
        Reset the status if needed
        """
        self.game_count += 1
        print(self.game_count)
        history = self.history[::-1]
        for i, h in enumerate(history[:-1]):
            sN = history[0]['state']
            aN = history[0]['action']
            state_str = self._GetStateStr(sN)
            reward = -200
            self.qvalues[state_str][aN] = (1-self.lr) * self.qvalues[state_str][aN] + self.lr * reward # Bellman equation - there is no future state since game is over
        if self.game_count%100==0:
            self.SaveQvalues()
        self.history = []

    def LoadQvalues(self, path="myqvaluesf.json"):
        with open(os.path.join(os.path.dirname(__file__),path), "r") as f:
            qvalues = json.load(f)
        return qvalues

    def SaveQvalues(self, path="myqvaluesf.json"):
        with open(os.path.join(os.path.dirname(__file__),path), "w") as f:
            json.dump(self.qvalues, f)
        #print("Savesavesavesavesave")

    def UpdateQValues(self):
        history = self.history[::-1]
        for i, h in enumerate(history[:-1]):
            s1 = h['state'] # current state
            s0 = history[i+1]['state'] # previous state
            a0 = history[i+1]['action'] # action taken at previous state
            
            x1 = s0.distance[0] # x distance at current state
            y1 = s0.distance[1] # y distance at current state
            #print(x1)
            x2 = s1.distance[0] # x distance at previous state
            y2 = s1.distance[1] # y distance at previous state
            ####  ##### #  #  #   #   ####  ###
            #   # #     #  #  #  # #  #   # #  #
            ####  #####  # # #  #   # ####  #   #
            #  #  #      # # #  ##### #  #  #  #
            #   # #####   # #   #   # #   # ###
            if s0.food != s1.food: # Snake ate a food, positive reward
                reward = 100
            elif abs(x1)**2 + abs(y1)**2 >= abs(x2)**2 + abs(y2)**2:
                #(abs(x1) >= abs(x2) and abs(y1) >= abs(y2)): # Snake is closer to the food, positive reward
                reward = 1
                #print("wwwwwwwwwwwwwwwwwwwwwwwww")
            else:
                reward = -1# Snake is further from the food, negative reward
            state_str = self._GetStateStr(s0)
            new_state_str = self._GetStateStr(s1)
            self.qvalues[state_str][a0] = (1-self.lr) * (self.qvalues[state_str][a0]) + self.lr * (reward + self.discount*max(self.qvalues[new_state_str])) # Bellman equation


    def _GetState(self,scene_info):
        self.block_size = 10
        self.display_width = 300
        self.display_height = 300
        dist_x = scene_info["food"][0] - scene_info["snake_head"][0]
        dist_y = scene_info["food"][1] - scene_info["snake_head"][1]

        if dist_x > 0:
            pos_x = '1' # Food is to the right of the snake
        elif dist_x < 0:
            pos_x = '0' # Food is to the left of the snake
        else:
            pos_x = 'NA' # Food and snake are on the same X file

        if dist_y > 0:
            pos_y = '3' # Food is below snake
        elif dist_y < 0:
            pos_y = '2' # Food is above snake
        else:
            pos_y = 'NA' # Food and snake are on the same Y file
        
        surroundings = self._Surroundings(scene_info)

        return GameState((dist_x, dist_y), (pos_x, pos_y), surroundings, scene_info["food"])

    def _GetStateStr(self, state):
        #print(str((state.position[0],state.position[1],state.surroundings)))
        return str((state.position[0],state.position[1],state.surroundings))

    def _Surroundings(self, scene_info):
        sqs = [
            #clockwise form inner to outer
            (scene_info["snake_head"][0],       scene_info["snake_head"][1]-10),
            (scene_info["snake_head"][0]+10,    scene_info["snake_head"][1]),
            (scene_info["snake_head"][0],       scene_info["snake_head"][1]+10),   
            (scene_info["snake_head"][0]-10,    scene_info["snake_head"][1])
            ]
        '''         
            (scene_info["snake_head"][0],       scene_info["snake_head"][1]-20),
            (scene_info["snake_head"][0]+10,    scene_info["snake_head"][1]-10),
            (scene_info["snake_head"][0]+20,    scene_info["snake_head"][1]),
            (scene_info["snake_head"][0]+10,    scene_info["snake_head"][1]+10),
            (scene_info["snake_head"][0],       scene_info["snake_head"][1]+20),
            (scene_info["snake_head"][0]-10,    scene_info["snake_head"][1]+10),
            (scene_info["snake_head"][0]-20,    scene_info["snake_head"][1]),
            (scene_info["snake_head"][0]-10,    scene_info["snake_head"][1]-10)
        '''
        '''(scene_info["snake_head"][0]+self.block_size*i,scene_info["snake_head"][1]+self.block_size*j)
            for i in range(-1,2) for j in range (-1,2)'''
        surrounding_list = []
        for sq in sqs:
            if sq in scene_info["snake_body"]: # part of tail
                if sq == scene_info["snake_body"][0]:
                    #print("OOOOO")
                    surrounding_list.append('2')
                elif sq == scene_info["snake_body"][-1]:
                    #print("yyyyyyyy")
                    surrounding_list.append('0')
                else :
                    surrounding_list.append('1')
            elif sq[0] < 0 or sq[1] < 0: # off screen left or top
                surrounding_list.append('1')
            elif sq[0] >= self.display_width or sq[1] >= self.display_height: # off screen right or bottom
                surrounding_list.append('1')
            else:
                surrounding_list.append('0')
        #surroundings = ''.join(surrounding_list)
        surroundings = self.preprevios_surroundings+self.previous_surroundings+''.join(surrounding_list)
        self.preprevios_surroundings = self.previous_surroundings
        self.previous_surroundings = ''.join(surrounding_list)
        return surroundings