from os import name
import random

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
        for i in self.multipleChoice:
            if i in importantQ:
                sum += weight
            else:
                sum += 1
        for i in self.negMultipleChoice:
            if i in importantQ:
                sum -= weight
            else:
                sum -= 1
        self.sum = sum

class SecretSanta():
    def __init__(self, fileLocal, negativeQ, positiveQ, importantQ):
        self.fileLocal = fileLocal
        self.negativeQ = negativeQ
        self.positiveQ = positiveQ
        self.importantQ = importantQ
        self.people = []
        self.names = []
    
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
    
    def fileRead(self):
        #file reading
        while line:
            line = line.rstrip()
            answers = line.split(",")
            person = Person(answers[1])

            #check every answer and whether its negative, positive, or open ended
            for i in range(len(answers)):
                if answers[i] == self.negativeQ[i]:
                    person.addMultipleChoice(answers[i], True)
                elif answers[i] == self.positiveQ[i]:
                    person.addMultipleChoice(answers[i], False)
                else:
                    person.addOpenEnded(answers[i])
            
            #every line is one person, and every persons sum must be calculated
            person.summation(self.importantQ, weight)
            self.people.append(person)
    
    def peopleSort(self):
        self.people.sort(key= lambda person: person.sum)
        for i in self.people:
            self.names.append(i.name)
    
    def findMatches(self):
        graph = dict()
        for i in range(len(self.names)):
            edges = self.closestValues(self.names, i, 4)
            graph[self.names[i]] = "sink"
            graph[self.people[i]] = edges
        graph["source"] = self.people


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

def FordFulkerson(graph, start, end):
    source = graph.get(start)
    matches = []
    
    while len(source) != 0:
        n = random.randint(0, len(source) - 1) #random node to travel to from source
        names = graph.pop(source[n]) #remove from graph of gift givers

        n2 = random.randint(0, len(names) - 1) #random name to match with that person
        while names[n2] not in graph:
            names.remove(source[n2])
            n2 = random.randint(0, len(names))

        match = (source[n], names[n2])

        source.remove(source[n]) #remove from gift givers set
        graph.pop(names[n2]) #remove from gift recievers set

        matches.append(match)
    
    return matches



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
    answer = "yo"
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
    person.addMultipleChoice(answer, True) #dosent matter the answer since the boolean is the only thing that affects values
    person.addMultipleChoice(answer, False)
    person.summation([], weight)
    assert(person.sum == 0)

    #positive sum weighted
    person.multipleChoice = []
    person.negMultipleChoice = []
    person.addMultipleChoice(answer, False)
    person.summation([answer], weight)
    assert(person.sum == weight)

    #negative sum weighted
    person.multipleChoice = []
    person.negMultipleChoice = []
    person.addMultipleChoice(answer, True)
    person.summation([answer], weight)
    assert(person.sum == (0 - weight))