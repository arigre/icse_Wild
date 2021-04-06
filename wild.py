from typing import Generator
import pydata

from math import sqrt
from random import randint
from typing import Protocol, Dict, List, Iterator, Tuple, TypeVar, Optional
import heapq
import collections

T = TypeVar('T')

Location = TypeVar('Location')
groundType : Dict[int, str] = {1:'Terroso', 2:'Sabbioso', 3:'Breccioso', 4:'Erboso', 5:'Alberato', 6:'Roccioso',-1:'None'}
weightsforsun =[{'Terroso':3, 'Sabbioso':6, 'Breccioso':6, 'Erboso':3, 'Alberato':3, 'Roccioso':9},
                {'Terroso':3, 'Sabbioso':3, 'Breccioso':6, 'Erboso':9, 'Alberato':9, 'Roccioso':3},
                {'Terroso':3, 'Sabbioso':6, 'Breccioso':3, 'Erboso':6, 'Alberato':3, 'Roccioso':6}]

weightsforrain =[{'Terroso':9, 'Sabbioso':6, 'Breccioso':6, 'Erboso':6, 'Alberato':3, 'Roccioso':9},
                {'Terroso':6, 'Sabbioso':6, 'Breccioso':6, 'Erboso':9, 'Alberato':9, 'Roccioso':3},
                {'Terroso':3, 'Sabbioso':3, 'Breccioso':3, 'Erboso':6, 'Alberato':6, 'Roccioso':6}]






class Graph(Protocol):
    def neighbors(self, id: Location) -> List[Location]: pass


class SimpleGraph:
    def __init__(self):
        self.edges: Dict[Location, List[Location]] = {}

    def neighbors(self, id: Location) -> List[Location]:
        return self.edges[id]



class Queue:
    def __init__(self):
        self.elements = collections.deque()

    def empty(self) -> bool:
        return not self.elements

    def put(self, x: T):
        self.elements.append(x)

    def get(self) -> T:
        return self.elements.popleft()


# utility functions for dealing with square grids
def from_id_width(id, width):
    return (id % width, id // width)


def draw_tile(graph, id, style):
    r = " . "
    if 'number' in style and id in style['number']: r = " %-2d" % style['number'][id]
    if 'point_to' in style and style['point_to'].get(id, None) is not None:
        (x1, y1) = id
        (x2, y2) = style['point_to'][id]
        if x2 == x1 + 1: r = " > "
        if x2 == x1 - 1: r = " < "
        if y2 == y1 + 1: r = " v "
        if y2 == y1 - 1: r = " ^ "
    if 'path' in style and id in style['path']:   r = " ♥ "
    if 'start' in style and id == style['start']: r = " S "
    if 'goal' in style and id == style['goal']:   r = " X "
    if id in graph.walls: r = "###"
    return r


def draw_grid(graph, **style):
    print("~~~" * graph.width)
    for y in range(graph.height):
        for x in range(graph.width):
            print("%s" % draw_tile(graph, (x, y), style), end="")
        print()
    print("~~~" * graph.width)

GridLocation = Tuple[int, int]


class Node:
    def __init__(self, ground, walkable):
        self.ground = ground
        self.walkable = walkable




class SquareGrid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.walls: List[GridLocation] = []

    def in_bounds(self, id: GridLocation) -> bool:
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id: GridLocation) -> bool:
        return id not in self.walls

    def neighbors(self, id: GridLocation) -> Iterator[GridLocation]:
        (x, y) = id
        neighbors = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]  # E W N S
        # see "Ugly paths" section for an explanation:
        if (x + y) % 2 == 0: neighbors.reverse()  # S N W E
        results = filter(self.in_bounds, neighbors)
        results = filter(self.passable, results)
        return results


class WeightedGraph(Graph):
    def cost(self, from_id: Location, to_id: Location) -> float: pass


class GridWithWeights(SquareGrid):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.weights: Dict[GridLocation, float] = {}

    def cost(self, from_node: GridLocation, to_node: GridLocation) -> float:
        return self.weights.get(to_node, 1)


diagram4 = GridWithWeights(10, 10)
diagramnode: Dict[GridLocation, Node] = {}



def randgraph(start, goal):
    for i in range(diagram4.height):
        for y in range(diagram4.width):
            if (not i == 0) & (not i == diagram4.height-1) & (not y == 0) & (not y == diagram4.width-1):
                if randint(1, 15) < 3:
                    if (not start.__eq__((i, y))) & (not goal.__eq__((i, y))):
                        diagram4.walls.append((i, y))
                        diagramnode[(i, y)] = Node(-1, False)
                else:
                    typenode((i, y))
            else:
                typenode((i, y))


def setweights(results,me,type):
    for i in range(diagram4.height):
        for y in range(diagram4.width):
            diagram4.weights[(i, y)] = 9
    for i in range(diagram4.height):
        for y in range(diagram4.width):
            x = groundType[diagramnode[(i, y)].ground]
            for st in results.data:
                    if x == st[0]:
                        if me == 'Sole':
                            u=weightsforsun[type][x]
                            diagram4.weights[(i, y)] = weightsforsun[type][x]
                        else:
                            diagram4.weights[(i, y)] = weightsforrain[type][x]



def typenode(id : GridLocation):
    diagramnode[id] = Node(randint(1,6), True)

class PriorityQueue:
    def __init__(self):
        self.elements: List[Tuple[float, T]] = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item: T, priority: float):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> T:
        return heapq.heappop(self.elements)[1]


# reconstruct_path that doesn't have duplicate entries
def reconstruct_path(came_from: Dict[Location, Location],
                     start: Location, goal: Location) -> List[Location]:
    current: Location = goal
    path: List[Location] = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)  # optional
    path.reverse()  # optional
    return path


def heuristic(a: GridLocation, b: GridLocation, type) -> float:
    (x1, y1) = a
    (x2, y2) = b
    return sqrt(abs(x1 - x2) ** 2 + abs(y1 - y2) ** 2)


def a_star_search(graph: WeightedGraph, start: Location, goal: Location, type):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from: Dict[Location, Optional[Location]] = {}
    cost_so_far: Dict[Location, float] = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current: Location = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next, goal, type)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far


def main():
    start, goal = (0, 0), (9,9)
    print("\n  ♣  W I L D  ♣\n\nTi aiuteremo a scegliere il percorso adeguato per la tua giornata in un parco naturale in base alle tue preferenze e al meteo\n")
    while True:
        print("Scegli se vuoi fare una: \n - Passeggiata\n - Panoramico\n - Avventura \n Ricorda di inserire la tua scelta con la prima lettera maiuscola")
        tipo=(input())

        result = pydata.querytype(tipo)
        print()
        mode = result.data[0][0]

        print ("\nIl meteo di oggi è\n(Scegli inserendo 1 oppure 2):\n1.Soleggiato o Abbastanza soleggiato\n2.Piovoso o ha appena smesso di piovere")
        meteo = (input())
        if meteo == '1':
            me="Sole"
        else:
            me= "Pioggia"

        result = pydata.query([me, mode])
        randgraph(start, goal)
        setweights(result,me,1)
        came_from, cost_so_far = a_star_search(diagram4, start, goal, 0)
        print("\n\nIl percorso che ti congigliamo è: \n")
        draw_grid(diagram4, path=reconstruct_path(came_from, start=start, goal=goal))
        print()
        print("Ti interessa visualizzare il grafo con i costi del percorso e la ricostruzione del percorso per vedere perchè ti abbiamo consigliato proprio questo?si/no")
        if (input())=='si':
            print("\n\nGrafo con i costi:\n")
            draw_grid(diagram4, number=cost_so_far, start=start, goal=goal)
            print()
            print("\n\nGrafo ricostruito partendo dal nodo Goal:\n\n")
            draw_grid(diagram4, point_to=came_from, start=start, goal=goal)
        print()
        print("ripetere esecuzione?si/no")
        if (input()) == 'no':
            print("Arrivederci!")
            break


if __name__ == '__main__':
    main()