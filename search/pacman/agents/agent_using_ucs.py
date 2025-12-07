#!/usr/bin/env python3
from game.controllers import PacManControllerBase
from game.pacman import Game, DM, Direction
from typing import List
import sys
from os.path import dirname

# hack for importing from parent package
sys.path.append(dirname(dirname(dirname(__file__))))
from search_templates import *
from ucs import ucs


class PacProblem(Problem):
    def __init__(self, game: Game) -> None:
        self.game: Game = game

    def initial_state(self) -> int:
        return self.game.pac_loc

    def actions(self, state: int) -> List[int]:
        return self.game.get_possible_dirs(state)

    def result(self, state: int, action: int) -> int:
        return self.game.get_neighbor(state, action)

    def is_goal(self, state: int) -> bool:
        
        pp = self.game.get_power_pill_index(state)
        if pp != -1 and self.game.check_power_pill(pp) == True and self.num_ghosts_edible() < 2:
            return True
        ghost_idx = self.get_ghost_index(state)
        if ghost_idx != -1 and self.game.is_edible(ghost_idx) == True:
            return True
        if self.game.get_active_power_pills_count() == 0:
            pill = self.game.get_pill_index(state)
            if pill != -1 and self.game.check_pill(pill) == True:
                return True
        return False

    def cost(self, state: int, action: int) -> float:
        result_state = self.result(state, action)
        """
        ghost_idx, ghost_dist = self.get_closest_ghost_index_distance(result_state)        
        if ghost_idx != -1 and ghost_dist < 1000:       
            best_action = self.game.get_best_dir_from(self.game._graph[state].neighbors, ghost_idx, False)
            worst_action = self.game.get_best_dir_from(self.game._graph[state].neighbors, ghost_idx, True)
            if self.game.is_edible(ghost_idx) == True:
                best_action, worst_action = worst_action, best_action
            if action == best_action:
                return 0
            if action == worst_action:
                return 10000
        """
        pp = self.game.get_power_pill_index(result_state)
        if pp != -1 and self.game.check_power_pill(pp) == True:
            return 10
        
        pil = self.game.get_pill_index(result_state)
        if pil != -1 and self.game.check_pill(pil) == True:
            return 30
        
        return 100
    
    def get_ghost_index(self, state: int) -> int:
        for i, loc in enumerate(self.game.ghost_locs):
            if loc == state:
                return i
        return -1
    
    def get_closest_ghost_index_distance(self, state: int) -> int:
        min_dist = float('inf')
        closest_ghost_idx = -1
        for i, loc in enumerate(self.game.ghost_locs):
            dist = self.game.get_path_distance(state, loc)
            if dist < min_dist:
                min_dist = dist
                closest_ghost_idx = i
        return closest_ghost_idx, min_dist
    
    def num_ghosts_edible(self) ->int:
        cnt = 0
        for i in range(len(self.game.ghost_locs)):
            if self.game.is_edible(i):
                cnt += 1
        return cnt



class Agent_Using_UCS(PacManControllerBase):
    def tick(self, game: Game) -> None:
        prob = PacProblem(game)
        sol = ucs(prob)
        if sol is None or not sol.actions:
            print("No path found.", file=sys.stderr)
        else:
            self.pacman.set(sol.actions[0])
