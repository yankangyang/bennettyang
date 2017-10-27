import random as rand
from math import sqrt,cos,sin,atan2

########################################
#   Mandatory functions for the rrt    #
########################################

# Tests if the new_node is close enough to the goal to consider it a goal
def winCondition(new_node,goal_node,WIN_RADIUS):
    """
    new_node - newly generated node we are checking
    goal_node - goal node
    WIN_RADIUS - constant representing how close we have to be to the goal to
        consider the new_node a 'win'
    """
    return distance(new_node, goal_node) < WIN_RADIUS

# Find the nearest node in our list of nodes that is closest to the new_node
def nearestNode(nodes,new_node):
    """
    nodes - a list of nodes in the RRT
    new_node - a node generated from getNewPoint
    """
    closest = float("inf"), None
    for node in nodes:
        # no need to sqrt distances
        dist = distance_squared(node, new_node)
        if dist < closest[0]:
            closest = dist, node
    return closest[1]

# Find a new point in space to move towards uniformally randomly but with
# probability 0.05, sample the goal. This promotes movement to the goal.
def getNewPoint(XDIM,YDIM,XY_GOAL):
    """
    XDIM - constant representing the width of the game
    YDIM - constant representing the height of the game
    XY_GOAL - node (tuple of integers) representing the location of the goal
    """
    if (rand.uniform(0,1) < 0.05):
        return XY_GOAL
    else:
        xval = rand.uniform(0,XDIM)
        yval = rand.uniform(0,YDIM)
        return xval, yval

# Extend (by at most distance delta) in the direction of the new_point and place
# a new node there
def extend(current_node,new_point,delta):
    """
    current_node - node from which we extend
    new_point - point in space which we are extending toward
    delta - maximum distance we extend by
    """
    # compute using ratios of similar triangles
    xdiff = current_node[0] - new_point[0]
    ydiff = current_node[1] - new_point[1]
    ratio = delta / distance(current_node, new_point)
    # if new_point is closer than delta, just return that point
    if ratio > 1:
        return new_point
    return current_node[0] - ratio*xdiff, current_node[1] - ratio*ydiff


# iterate throught the obstacles and check that our point is not in any of them
def isCollisionFree(obstacles,point,obs_line_width):
    """
    obstacles - a dictionary with multiple entries, where each entry is a list of
        points which define line segments of with obs_line_width
    point - the location in space that we are checking is not in the obstacles
    obs_line_width - the length of the line segments that define each obstacle's
        boundary
    """
    for i in range(len(obstacles)):
        prev = obstacles.values()[i][0]
        for curr in obstacles.values()[i][1:]:
            # solve for constants in: Ax + By + C = 0, for line containing prev + curr
            # Use (y1 - y2)x + (x2 - x1)y + (x1y2 - x2y1) = 0
            A = prev[1] - curr[1]
            B = curr[0] - prev[0]
            C = prev[0]*curr[1] - curr[0]*prev[1]
            # distance formula from point to line
            dist = abs(A*point[0] + B*point[1] + C) / sqrt(A**2 + B**2)
            if dist < obs_line_width:
                # detect past bounds of line segment
                max_dist_squared = distance(prev, curr)**2 + obs_line_width**2
                if distance_squared(point, prev) > max_dist_squared or distance_squared(point, curr) > max_dist_squared:
                    continue
                return False
            prev = curr
    return True

################################################
#  Any other helper functions you need go here #
################################################

# compute distance squared between two points
def distance_squared(p1, p2):
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

# computes distance between two points
def distance(p1, p2):
    return sqrt(distance_squared(p1, p2))







