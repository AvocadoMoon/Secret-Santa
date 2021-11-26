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
    def __init__(self, fileLocal, negativeQ, positiveQ, importantQ, weight):
        self.fileLocal = fileLocal
        self.negativeQ = negativeQ
        self.positiveQ = positiveQ
        self.importantQ = importantQ
        self.weight = weight
        self.people = []
        self.names = []
    
    #when similar values, n, is odd then the code returns even number of similar values still
    def closestValues(self, list, i, n):
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
        f = open(self.fileLocal, "r")
        line = f.readline() 
        line = f.readline() #skip the first line of info

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
            person.summation(self.importantQ, self.weight)
            self.people.append(person)
            line = f.readline()
        
        f.close()
    
    def peopleSort(self):
        self.people.sort(key= lambda person: person.sum)
        for i in self.people:
            self.names.append(i.name)
    
    def findMatches(self, options):
        self.fileRead()
        self.peopleSort()

        graph = dict()
        for i in range(len(self.names)):
            edges = self.closestValues(self.names, i, options)
            graph[self.names[i]] = "sink"
            graph[self.people[i]] = edges
        graph["source"] = self.people

        return self.FordFulkerson(graph, "source", "sink")

    def FordFulkerson(self, graph, start, end):
        source = graph.get(start)
        matches = []
        
        while len(source) != 0:
            n = random.randint(0, len(source) - 1) #random node to travel to from source
            names = graph.pop(source[n]) #remove from graph of gift givers

            n2 = random.randint(0, len(names) - 1) #random name to match with that person
            while names[n2] not in graph:
                names.remove(names[n2])
                if (len(names) == 0):
                    None
                n2 = random.randint(0, len(names) - 1)

            match = (source[n].name, names[n2])

            source.remove(source[n]) #remove from gift givers set
            graph.pop(names[n2]) #remove from gift recievers set

            matches.append(match)
        
        return matches