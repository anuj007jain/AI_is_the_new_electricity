import numpy as np
import heapq
from datetime import datetime

t1 = datetime.now()

inp = open("input.txt")


class ListNode:

    def __init__(self, value, x_coordinate, y_coordinate):
        self.value = value
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate

    def __gt__(self, list_node):
        return self.value > list_node.value

    def __lt__(self, list_node):
        return self.value < list_node.value


class HeapNode:

    def __init__(self, point_set, depth, total_score, smallest_score_in_set):
        self.point_set = point_set
        self.depth = depth
        self.total_score = total_score
        self.smallest_score_in_set = smallest_score_in_set

    # inverted implementation because we only have min heap implementation
    def __gt__(self, heap_node):
        return self.total_score < heap_node.total_score

    # inverted implementation because we only have min heap implementation
    def __lt__(self, heap_node):
        return self.total_score > heap_node.total_score


class Point:

    def __init__(self, x_coordinate, y_coordinate):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate

    def __eq__(self, point):
        if self.x_coordinate == point.x_coordinate and self.y_coordinate == point.y_coordinate:
            return True
        return False

    def __hash__(self):
        return hash((self.x_coordinate, self.y_coordinate))

    def __str__(self):
        return "X: "+str(self.x_coordinate)+" Y: "+str(self.y_coordinate)


def check_if_feasible(curr_point, points):
    for point in points:
        if point.x_coordinate == curr_point.x_coordinate or point.y_coordinate == curr_point.y_coordinate or \
                abs(float(point.x_coordinate - curr_point.x_coordinate)/float(point.y_coordinate - curr_point.y_coordinate)) == 1:
            return False
    return True


gridSize = int(inp.readline().strip())
# print ("gridSize:" + str(gridSize))
policemenCount = int(inp.readline().strip())
# print ("policemenCount:" + str(policemenCount))
scooterCount = int(inp.readline().strip())
# print ("scooterCount:" + str(scooterCount))

matrix = np.zeros((gridSize, gridSize), dtype=np.int16)
# print(matrix)

for x in range(12 * scooterCount):
    scooterPosition = inp.readline().strip()
    scooterCoordinates = scooterPosition.split(",")
    matrix[int(scooterCoordinates[1])][int(scooterCoordinates[0])] += 1

inp.close()
# print (matrix)

max_heap = []
sorted_list = []
max_depth = policemenCount - 1
best_current_solution = -1

for x in range(gridSize):
    for y in range(gridSize):
        heapq.heappush(max_heap, HeapNode({Point(x, y)}, 0, matrix[x][y], matrix[x][y]))
        sorted_list.append(ListNode(matrix[x][y], x, y))

sorted_list.sort(reverse=True)

while max_heap.__len__() != 0 and (datetime.now()-t1).seconds < 175:
    max_element = heapq.heappop(max_heap)
    if max_depth == max_element.depth:
        if max_element.total_score > best_current_solution:
            best_current_solution = max_element.total_score
            # print ("new best current solution: " + str(best_current_solution))
        continue
    point_set = max_element.point_set
    for list_node in sorted_list:
        x = list_node.x_coordinate
        y = list_node.y_coordinate
        if list_node.value > max_element.smallest_score_in_set:
            continue
        if (max_element.total_score + (max_depth - max_element.depth) * list_node.value) < best_current_solution:
            break
        if check_if_feasible(Point(x, y), point_set):
            new_point_set = set(point_set)
            new_point_set.add(Point(x, y))
            heapq.heappush(max_heap, HeapNode(new_point_set, max_element.depth + 1, max_element.total_score + list_node.value, min(max_element.smallest_score_in_set, list_node.value)))

# print (best_current_solution)
out = open("output.txt", "w")
out.write(str(best_current_solution)+"\n")
out.close()
