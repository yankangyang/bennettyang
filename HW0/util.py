##### Filename: util.py
##### Author: Yankang Yang
##### Date: 9/6/2017
##### Email: yankangyang@college.harvard.edu

import copy
from collections import deque

## Problem 1

def matrix_multiply(x, y):
    ## initialize list of lists
    calculated = [[ 0 for b in range(len(y[0]))] for a in range(len(x)) ]
    ## loop through rows and columns of matricies corresponding to matrix multiplication
    for i in range(len(x)):
        for j in range(len(y[0])):
            for k in range(len(y)):
                calculated[i][j] += x[i][k] * y[k][j]                  
    return calculated
    

## Problem 2, 3

class MyQueue:
    def __init__(self):
        ## initialize deque data structure 
        self.items = deque()
    def push(self, val):
        ## append value to items
        self.items.append(val)
    def pop(self):
        try:
            ## try to pop value from the top of the queue
            val = self.items.popleft()
            return val
        except IndexError:
            ## otherwise return none
            return None
    def __eq__(self, other):
        for i in self.items:
            ## check all for inequality 
            if self.items[i] != other.items[i]:
                return False
            ## return true if you make it through the whole list
            return True
    def __ne__(self, other):
        for i in self.items:
            ## check all for equality
            if self.items[i] == other.items[i]:
                return False
            ## return true if the whole list is not eq
            return True
    def __str__(self):
        s = ''
        ## append each to string
        for i in self.items:
            s += (str(i) + ' ')
        return s 

class MyStack:
    def __init__(self):
        ## init stack as deque
        self.items = deque()
    def push(self, val):
        ## append values to items
        self.items.append(val)
    def pop(self):
        ## same try/except as queue except pop from right
        try:
            val = self.items.pop()
            return val
        except IndexError:
            return None
    ## same as queue
    def __eq__(self, other):
        for i in self.items:
            if self.items[i] != other.items[i]:
                return False
            return True
    def __ne__(self, other):
        for i in self.items:
            if self.items[i] == other.items[i]:
                return False
            return True
    def __str__(self):
        s = ''
        for i in self.items:
            s += (str(i) + ' ')
        return s 

## Problem 4

def add_position_iter(lst, number_from= 4):
    ## copy a new list
    lst_cpy = list(lst)
    ## add both the offset (number_from) and the appropriate index value
    for i in range(0, len(lst)):
        lst_cpy[i] += i + number_from
    return lst_cpy

def add_position_recur(lst, number_from=0):
    ## we need two functions or else the list recopies on each recursion
    lst_cpy = list(lst) 
    return recursion(lst, number_from, 0)

def recursion(lst, number_from, index):
    ## this function is called recursively with a new index 
    if (index + 1) <= len(lst): 
        lst[index] += index + number_from
        recursion(lst, number_from, index + 1)
    ## when the list is exhausted, return the copied list
    return lst

def add_position_map(lst, number_from=0):
    list_cpy = list(lst)
    ## copy number_from offset into a list so all values can be mapped
    nf_list = len(lst) * [number_from]
    ## use lambda function to sum components and map to new list
    list_cpy = map(lambda l,r,nf: l+r+nf, list_cpy, range(0, len(lst)), nf_list)
    return list_cpy

## Problem 5

def remove_course(roster, student, course):
    ## use set and dictionary components to remove roster
    roster[student].remove(course)
    return roster

## Problem 6
def copy_remove_course(roster, student, course):
    ## use deepcopy function to copy the roster over
    new_roster = copy.deepcopy(roster)
    return remove_course(new_roster,student,course)

## Main Function

def main():
    ## Problem 1
    x = [[9,6,3],[4,4,5]]
    y = [[1,6,9],[7,8,1]]
    mm = matrix_multiply(x,y)
    print mm
   

    ## Problem 2
    q = MyQueue()
    popped_val = q.pop()
    print(popped_val) ##none
    
    s = MyStack()
    s.push(1); s.push(2); s.push(3)
    print(s.pop())

    
    ## Problem 3
    ## __eq__
    s1 = MyStack()
    s1.push(1); s1.push(2); s1.push(3)
    
    s2 = MyStack()
    s2.push(1); s2.push(2); s2.push(3); s2.pop(); s2.push(3)
    print(s1.__eq__(s2)) ## true
    
    ## __ne__
    q1 = MyQueue()
    q1.push(1); q1.push(2); q1.push(3)
    
    q2 = MyQueue()
    q2.push(1); q2.push(2); q2.push(3)
    print(q1.__ne__(q2)) ## false
    
    ## __str__
    print(q1.__str__()) ## prints '1 2 3'
    
    
    ## Problem 4
    ## iterative
    lst = [8, 2, 5, 7, 9]
    print(add_position_iter(lst))
    
    ## recursive
    recur_list = [9, 12, 46, 2, 33]
    print(add_position_recur(recur_list))
    
    ## mapping
    map_list = [42, 76, 1, 290, 2]
    print(add_position_map(map_list))
    
    
    ##Problem 5 
    roster = {'kyu': set(['cs182', 'gov20']), 'david': set(['cs182', 'es128'])}
    print roster
    remove_course(roster, 'kyu','cs182')
    print roster
    
    ##Problem 6
    nd_roster = {'jason': set(['cs182', 'gov20']), 'david': set(['cs136', 'es128'])}
    dest_roster = copy_remove_course(nd_roster, 'jason','cs182')
    print dest_roster
    print nd_roster
    
main()



