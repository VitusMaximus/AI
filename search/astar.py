#!/usr/bin/env python3
from search_templates import Solution, HeuristicProblem
from typing import Optional
from dataclasses import dataclass, field
import heapq


@dataclass(order=True)
class Node:
    f: float       # f = g + h
    g: float = field(compare=False)
    state: object = field(compare=False)
    parent: 'Node' = field(compare=False)
    action: any = field(compare=False)


class Frontier:
    def __init__(self):
        self.frontier = []
        self.state_costs = {}   # Contains lowest cost for each distinct state in frontier

    def push(self, node: Node) -> None:
        if node.state in self.state_costs and self.state_costs[node.state] <= node.g: #Same state with lower or same cost is already in frontier
            return
        heapq.heappush(self.frontier, node)
        self.state_costs[node.state] = node.g

    def pop(self) -> Node:
        return heapq.heappop(self.frontier)
    
    def empty(self) -> bool:
        return len(self.frontier) == 0


class AStarSearch:
    def __init__(self, prob: HeuristicProblem):
        self.prob = prob
        self.explored = set()
        self.visited = Frontier()

    def explore_state(self, node: Node):
        actions = self.prob.actions(node.state)

        for action in actions:
            new_state = self.prob.result(node.state, action)
            if new_state in self.explored:
                continue

            a_cost = self.prob.cost(node.state, action)
            new_cost = node.g + a_cost
            f = new_cost + self.prob.estimate(new_state)
            new_node = Node(f, new_cost, new_state, node, action)
            self.visited.push(new_node)

    def next_to_explore(self) -> Node:
        while not self.visited.empty():
            node = self.visited.pop()
            if node.state not in self.explored:
                return node
            
        return None
    
    def reconstruct_path(self, node: Node):
        path_rev = []
        while node.parent is not None:
            path_rev.append(node.action)
            node = node.parent

        return list(reversed(path_rev))

    def search(self):
        init_state = self.prob.initial_state()
        node = Node(self.prob.estimate(init_state), 0, init_state, None, None)
        while not self.prob.is_goal(node.state):
            self.explored.add(node.state)
            self.explore_state(node)

            node = self.next_to_explore()
            if node is None: return None

        path_to_goal = self.reconstruct_path(node)
        return Solution(path_to_goal, node.state, node.g)



def AStar(prob: HeuristicProblem) -> Solution:
    """Return Solution of the problem solved by AStar search."""
    # Your implementation goes here.
    astar_search = AStarSearch(prob)
    return astar_search.search()

    # return Solution([actions leading to goal], goal_state, path_cost)
