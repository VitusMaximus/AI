#!/usr/bin/env python3
from game.board import Board, ETile, EDirection
from typing import List



def detect(board: Board) -> List[List[bool]]:
    """
    Returns 2D matrix containing true for dead squares.

    Dead squares are squares, from which a box cannot possibly
     be pushed to any goal (even if Sokoban could teleport
     to any location and there was only one box).

    You should prune the search at any point
     where a box is pushed to a dead square.

    Returned data structure is
        [board_width] lists
            of [board_height] lists
                of bool values.
    (This structure can be indexed "struct[x][y]"
     to get value on position (x, y).)
    """
    map = [[True for _ in range(board.height)] for _ in range(board.width)]

    changed = True
    while changed:
        changed = False
        for x in range(board.width):
            for y in range(board.height):

                if not map[x][y]:
                    continue

                tile = board.tile(x, y)

                if ETile.is_target(tile):   # A target is never a dead square
                    map[x][y] = False
                    changed = True
                    continue

                if ETile.is_wall(tile):     # A wall is dead square
                    continue

                can_get_to_non_dead = False
                for dir in EDirection:
                    dx, dy = dir.value[1], dir.value[2]
                    nx, ny = x + dx, y + dy # Position to which box would be pushed
                    sx, sy = x - dx, y - dy # Position where Sokoban would stand to push
                    stile = board.tile(sx, sy)
                    if not map[nx][ny] and not ETile.is_wall(stile): # Not dead if box can be moved to non-dead square and Sokoban can push it there
                        can_get_to_non_dead = True
                        break

                if can_get_to_non_dead:
                    map[x][y] = False
                    changed = True

    return map



def detect_wrong(board: Board) -> List[List[bool]]:
    """
    Returns 2D matrix containing true for dead squares.

    Dead squares are squares, from which a box cannot possibly
     be pushed to any goal (even if Sokoban could teleport
     to any location and there was only one box).

    You should prune the search at any point
     where a box is pushed to a dead square.

    Returned data structure is
        [board_width] lists
            of [board_height] lists
                of bool values.
    (This structure can be indexed "struct[x][y]"
     to get value on position (x, y).)
    """
    map = [[False for _ in range(board.height)] for _ in range(board.width)]

    changed = True
    while changed:
        changed = False
        for x in range(board.width):
            for y in range(board.height):
                if map[x][y]:
                    continue

                tile = board.tile(x, y)

                if ETile.is_target(tile):   # A target is never a dead square
                    continue

                if ETile.is_wall(tile):     # A wall is dead square
                    map[x][y] = True
                    changed = True
                    continue
                
                dead = True
                for dir in EDirection:
                    dx, dy = dir.value[1], dir.value[2]
                    nx, ny = x + dx, y + dy # Position to which box would be pushed
                    sx, sy = x - dx, y - dy # Position where Sokoban would stand to push
                    stile = board.tile(sx, sy)
                    if not map[nx][ny] and not ETile.is_wall(stile): # Not dead if box can be moved to non-dead square and Sokoban can push it there
                        dead = False
                        break
                if dead:
                    map[x][y] = True
                    changed = True

    return map


def is_dead_square(dead_squares: List[List[bool]], x: int, y: int) -> bool:
    """Returns whether the square (x, y) is a dead square."""
    return dead_squares[x][y]