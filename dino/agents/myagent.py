#!/usr/bin/env python3
from game.dino import *
from game.agent import Agent
import numpy as np

class MyAgent(Agent):
    """Reflex agent static class for Dino game."""

    @staticmethod
    def get_move(game: Game) -> DinoMove:
        """
        Note: Remember you are creating simple-reflex agent, that should not
        store or access any information except provided.
        """
        # # for visual debugging intellisense you can use
        # if MyAgent.debug:
        #     from game.debug_game import DebugGame
        #     game: DebugGame = game
        #     if not hasattr(MyAgent, "debug_txt"):
        #         _ = game.add_text(Coords(10, 10), "red", "Hello World.")
        #         MyAgent.debug_txt = game.add_text(Coords(10, 30), "red", "0")
        #     else:
        #         MyAgent.debug_txt.text = str(game.score)
        #     game.add_dino_rect(Coords(-10, -10), 150, 150, "yellow")
        #     l = game.add_dino_line(Coords(0, 0), Coords(100, 0), "black")
        #     l.dxdy.update(50, 30)
        #     l.dxdy.x += 50
        #     game.add_moving_line(Coords(1000, 100), Coords(1000, 500), "purple")

        # YOUR CODE GOES HERE
        duck_top = Dino.Y_DUCK

        x = game.dino.x
        next_obstacle = None
        for i, o in enumerate(game.obstacles):
            if o.rect.x > x and o.rect.coords.x < x + 120 + 20 * (game.speed - 5):   # Obstacle in front
                if o.rect.bottom <= duck_top:
                    if MyAgent.verbose:
                        print("ducking right")
                    return DinoMove.DOWN_RIGHT
                else:
                    if MyAgent.verbose:
                        print("jumping right")
                    return DinoMove.UP_RIGHT

            if o.rect.left < x and o.rect.right > x:    # Above or bellow obstacle
                if game.dino.state is DinoState.DUCKING:
                    if game.dino.head.x < o.rect.right:
                        if MyAgent.verbose:
                            print("ducking right")
                        return DinoMove.DOWN_RIGHT
                else:
                    if MyAgent.verbose:
                        print("running right")
                    return DinoMove.RIGHT
                
            #if o.rect.x > x and game.dino.state is DinoState.JUMPING and MyAgent.will_clear_while_jumping(game, o):
            #        print("running right")
            #    return DinoMove.RIGHT
        
        if game.dino.state is DinoState.JUMPING: 
            if MyAgent.verbose:
                print("Ending jump")
            return DinoMove.DOWN

        if game.dino.x < 300:
            if MyAgent.verbose:
                print("Speeding up")
            return DinoMove.RIGHT
        return DinoMove.NO_MOVE
    
    @staticmethod
    def will_clear_while_jumping(game: Game, obstacle: Obstacle) -> bool:
        """
        Makes an estimate if the dino will clear the obstacle while jumping.
        """
        distance_to_clear = obstacle.rect.right - game.dino.x
        current_clearance = obstacle.rect.top - game.dino.y

        return current_clearance * np.power(game.speed / 5, 1/2.5) > distance_to_clear * 0.8