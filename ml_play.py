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

        self.qvalues = self.LoadQvalues()
        self.history = []

        self.actions = {
            0:'LEFT',
            1:'RIGHT',
            2:'UP',
            3:'DOWN'
        }
        self.previous_surroundings = "2000"

    def update(self, scene_info):

        if scene_info["status"] == "GAME_OVER":
            return "RESET"

        state = self._GetState(scene_info)

        rand = random.uniform(0,1)
        state_scores = self.qvalues[self._GetStateStr(state)]
        Max = sorted(state_scores,reverse = True)[0]
        action_key = state_scores.index(Max)
        action_val = self.actions[action_key]
        
        return action_val
        
    def reset(self):
        pass

    def LoadQvalues(self, path="myqvaluesf.json"):
        with open(os.path.join(os.path.dirname(__file__),path), "r") as f:
            qvalues = json.load(f)
        return qvalues

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
        return str((state.position[0],state.position[1],state.surroundings))

    def _Surroundings(self, scene_info):
        sqs = [
            #clockwise form inner to outer
            (scene_info["snake_head"][0],       scene_info["snake_head"][1]-10),
            (scene_info["snake_head"][0]+10,    scene_info["snake_head"][1]),
            (scene_info["snake_head"][0],       scene_info["snake_head"][1]+10),   
            (scene_info["snake_head"][0]-10,    scene_info["snake_head"][1])
            ]
        surrounding_list = []
        for sq in sqs:
            if sq in scene_info["snake_body"]: # part of tail
                if sq == scene_info["snake_body"][0]:
                    surrounding_list.append('2')
                elif sq == scene_info["snake_body"][-1]:
                    surrounding_list.append('0')
                else :
                    surrounding_list.append('1')
            elif sq[0] < 0 or sq[1] < 0: # off screen left or top
                surrounding_list.append('1')
            elif sq[0] >= self.display_width or sq[1] >= self.display_height: # off screen right or bottom
                surrounding_list.append('1')
            else:
                surrounding_list.append('0')
        surroundings = self.previous_surroundings+''.join(surrounding_list)
        self.previous_surroundings = ''.join(surrounding_list)
        return surroundings
