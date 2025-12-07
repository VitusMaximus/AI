#!/usr/bin/env python3
from game.action import *
from game.board import *
from game.artificial_agent import ArtificialAgent
from dead_square_detector import detect
from typing import List, Union
import sys
from time import perf_counter
from os.path import dirname

# hack for importing from parent package
sys.path.append(dirname(dirname(dirname(__file__))))
from astar import AStar
from search_templates import HeuristicProblem

from collections import deque


class MyAgent(ArtificialAgent):
    """
    Logic implementation for Sokoban ArtificialAgent.

    See ArtificialAgent for details.
    """
    def __init__(self, optimal, verbose) -> None:
        super().__init__(optimal, verbose)  # recommended

    def new_game(self) -> None:
        """Agent got into a new level."""
        super().new_game()  # recommended

    @staticmethod
    def think(
        board: Board, optimal: bool, verbose: bool
    ) -> List[Union[EDirection, Action]]:
        
        """
        Code your custom agent here.
        You should use your A* implementation.

        You can find example implementation (without use of A*)
        in simple_agent.py.
        """
        
        prob = SokobanProblem(board)
        solution = AStar(prob)
        if not solution:
            return None

        return [a.dir for a in solution.actions]


class SokobanProblem(HeuristicProblem):
    """HeuristicProblem wrapper of Sokoban game."""

    def __init__(self, initial_board) -> None:
        # Your implementation goes here.
        # Hint: __init__(self, initial_board) -> None:
        self.dead_squares = detect(initial_board)
        self.initial_board = initial_board
        self.distance_map = self.compute_distance_map(initial_board)
        #print(tabulate(np.array(self.distance_map).T))

    def initial_state(self) -> Union[Board, StateMinimal]:
        # Your implementation goes here.
        # Hint: return self.initial_board
        return self.initial_board

    def actions(self, state: Union[Board, StateMinimal]) -> List[Action]:
        # Your implementation goes here.
        actions = []
        for dir in EDirection:
            action = Move.or_push(state, dir)
            if action.is_possible(state) and not self.is_pushing_to_dead_square(state, action):
                actions.append(action)
        return actions


    def result(
        self, state: Union[Board, StateMinimal], action: Action
    ) -> Union[Board, StateMinimal]:
        # Your implementation goes here.
        state = state.clone()
        action.perform(state)
        return state

    def is_goal(self, state: Union[Board, StateMinimal]) -> bool:
        # Your implementation goes here.
        return state.is_victory()

    def cost(self, state: Union[Board, StateMinimal], action: Action) -> float:
        # Your implementation goes here.
        return 1.0

    def estimate(self, state: Union[Board, StateMinimal]) -> float:
        # Your implementation goes here.
        dist_sum = 0
        for x in range(state.width):
            for y in range(state.height):
                tile = state.tile(x, y)
                if ETile.is_box(tile):
                    dist = self.distance_map[x][y]
                    assert dist != -1, "Box in wall"
                    dist_sum += dist

        return dist_sum

    
    def is_pushing_to_dead_square(self, state: Union[Board, StateMinimal], action: Action) -> bool:
        if not isinstance(action, Push):
            return False

        dx, dy = action.dir.value[1], action.dir.value[2]
        nx, ny = state.sokoban.x + 2*dx, state.sokoban.y + 2*dy

        return self.dead_squares[nx][ny]
    


    def compute_distance_map(self, state: Union[Board, StateMinimal]) -> List[List[int]]:
        map = [[-1 for _ in range(state.height)] for _ in range(state.width)]
        q = deque()
        for x in range(state.width):
            for y in range(state.height):
                tile = state.tile(x, y)
                if ETile.is_target(tile):
                    map[x][y] = 0
                    q.append((x, y))
        
        while q:
            x, y = q.popleft()
            for dir in EDirection:
                dx, dy = dir.value[1], dir.value[2]
                nx, ny = x + dx, y + dy
                if map[nx][ny] == -1:
                    tile = state.tile(nx, ny)
                    if not ETile.is_wall(tile):
                        map[nx][ny] = map[x][y] + 1
                        q.append((nx, ny))
        return map

                    
