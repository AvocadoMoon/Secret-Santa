

class Graph():
    def __init__(self, graph):
        self.graph = graph  # residual graph
        self. ROW = len(graph)
        # self.COL = len(gr[0])
 
    '''Returns true if there is a path from source 's' to sink 't' in
    residual graph. Also fills parent[] to store the path '''
 
    def BFS(self, s, t, parent):
 
        # Mark all the vertices as not visited
        visited = [False]*(self.ROW)
 
        # Create a queue for BFS
        queue = []
 
        # Mark the source node as visited and enqueue it
        queue.append(s)
        visited[s] = True
 
         # Standard BFS Loop
        while queue:
 
            # Dequeue a vertex from queue and print it
            u = queue.pop(0)
 
            # Get all adjacent vertices of the dequeued vertex u
            # If a adjacent has not been visited, then mark it
            # visited and enqueue it
            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and val > 0:
                      # If we find a connection to the sink node,
                    # then there is no point in BFS anymore
                    # We just have to set its parent and can return true
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u
                    if ind == t:
                        return True
 
        # We didn't reach sink in BFS starting
        # from source, so return false
        return False

class Person():
    def __init__(self, name) ->None:
        self.negMultipleChoice = []
        self.multipleChoice = []
        self.openEnded = []
        self.name = name
        self.sum = 0
    
    def addMultipleChoice(self, answer, neg):
        if neg:
            self.negMultipleChoice.append(answer)
        else:
            self.multipleChoice.append(answer)
    
    def addOpenEnded(self, answer):
        self.openEnded.append(answer)
    
    def summation(self, importantQ, weight):
        sum = 0
        for i in range(len(self.multipleChoice)):
            if i in importantQ:
                sum += weight
            else:
                sum += 1
        for i in range(len(self.negMultipleChoice)):
            if i in importantQ:
                sum -= weight
            else:
                sum -= 1
        self.sum = sum

#when similar values, n, is odd then the code returns even number of similar values still
def closestValues(list, i, n):
    l = i - (n//2)
    r = i + (n//2)

    #if the list is not long enough on the left side, compensate with the right and vice versa
    while l < 0:
        r += 1
        l += 1
    while r > (len(list) - 1):
        r -= 1
        l -= 1
    close = list[l: i]
    close.extend(list[i+1: r+1])
    return close


def SecretSanta(fileLocal, negative, positive, importantQ):
    #setup
    weight = 10
    f = open(fileLocal, "r")
    line = f.readline() 
    line = f.readline() #skip the first line of info
    people = []
    names = []

    #file reading
    while line:
        line = line.rstrip()
        answers = line.split(",")
        person = Person(answers[1])

        #check every answer and whether its negative, positive, or open ended
        for i in range(len(answers)):
            if answers[i] == negative[i]:
                person.addMultipleChoice(answers[i], True)
            elif answers[i] == positive[i]:
                person.addMultipleChoice(answers[i], False)
            else:
                person.addOpenEnded(answers[i])
        
        #every line is one person, and every persons sum must be calculated
        person.summation(importantQ, weight)
        people.append(person)
    
    
    people.sort(key= lambda person: person.sum)
    for i in people:
        names.append(i.name)

    #create graph
    graph = dict()
    for i in range(len(names)):
        edges = closestValues(names, i, 4)
        graph[names[i]] = "sink"
        graph[people[i]] = edges
    
    graph["source"] = people


if __name__ == "__main__":

    #setup
    similarValues = 4
    index = 0
    n = 10
    neg = -5
    weight = 5
    l = [a for a in range(n)]
    person = Person("Kyle")

    #0 edge case
    t = closestValues(l, index, similarValues)
    t2 = [a for a in range(index + 1, index + 1 + similarValues)]
    assert(t == t2)

    #end of list edge case
    index = n-1
    t = closestValues(l, index, similarValues)
    t2 = [a for a in range(index-similarValues, n-1)]
    assert(t == t2)

    #middle of list
    index = n//2
    t = closestValues(l, index, similarValues)
    t2 = [a for a in range(index - (similarValues // 2), index + (similarValues // 2) + 1) if a != index]
    assert(t == t2)

    #0 sum
    person.addMultipleChoice(-5, True) #dosent matter the answer since the boolean is the only thing that affects values
    person.addMultipleChoice(5, False)
    person.summation([], weight)
    assert(person.sum == 0)