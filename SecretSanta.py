from os import error, name
import random
import smtplib, ssl

port = 465 #for ssl

class Person():
    def __init__(self, name) ->None:
        self.negMultipleChoice = []
        self.multipleChoice = []
        self.openEnded = []
        self.name = name
        self.sum = 0
        self.email = ""
        self.qOrder = []
    
    def addMultipleChoice(self, answer, neg):
        if neg:
            self.negMultipleChoice.append(answer)
            self.qOrder.append("-m")
        else:
            self.multipleChoice.append(answer)
            self.qOrder.append("m")
    
    def addOpenEnded(self, answer):
        self.openEnded.append(answer)
        self.qOrder.append("o")
    
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
    
    def setEmail(self, email):
        self.email = email

#matrix graph is best since edges may be very dense and, more vertices won't be added
class Graph():
    def __init__(self, vertices):
        self.adjMatrix = []
        self.vertices = vertices
        self.size = len(self.vertices)
        for i in range(self.size):
            self.adjMatrix.append([0 for i in range(self.size)])

    # Add edges
    def add_edge(self, v1, v2):
        if v1 == v2:
            raise ValueError #cant be matched with yourself
        self.adjMatrix[v1][v2] = 1

    # Remove edges
    def remove_edge(self, v1, v2):
        if self.adjMatrix[v1][v2] == 0:
            raise ValueError
        self.adjMatrix[v1][v2] = 0

    def __len__(self):
        return self.size
    
    def getRow(self, row):
        return self.adjMatrix[row]

    # Print the matrix
    def print_matrix(self):
        for row in self.adjMatrix:
            for val in row:
                print('{:4}'.format(val)),
            print


class SecretSanta():
    def __init__(self, fileLocal, negativeQ, positiveQ, importantQ, weight):
        self.fileLocal = fileLocal
        self.negativeQ = negativeQ
        self.positiveQ = positiveQ
        self.importantQ = importantQ
        self.allQuestions = []
        self.weight = weight
        self.graph = None
        self.people = []
        self.names = []
        self.options = None
        self.matched = None
    
    #when similar values, n, is odd then the code returns even number of similar values still
    def closestValues(self, list, i, n):
        l = i - (n//2)
        r = i + (n//2)

        #if the list is not long enough on the left side, compensate with the right and vice versa
        while l < 0:
            r += 1
            l += 1
        if l == i:
            l += 1
        while r > (len(list) - 1):
            r -= 1
            l -= 1
        if r == i:
            r -= 1
        return l, r
    
    def fileRead(self):
        f = open(self.fileLocal, "r")
        line = f.readline() 
        questions = line.split(",")
        line = f.readline() #skip the first line of info, its just questions

        #file reading
        while line:
            #format for all is #time stamp, email, name
            line = line.rstrip()
            answers = line.split(",")
            person = Person(answers[2]) #gets name
            person.setEmail(answers[1])

            #check every answer and whether its negative, positive, or open ended
            for i in range(2 ,len(answers)):
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
    
    #checks if someone already has been placed in potential matching with n amount of people, if so skip to other person
    def add_potential_matches(self, l, r, i):
        q = []
        n = l
        while i != l and l <= r:
            s = sum(self.graph.getRow(l))
            if s < self.options:
                self.graph.add_edge(l, i)
                l += 1
            elif l > 0:
                n -= 1
                while sum(self.graph.getRow(n)) == self.options:
                    n -= 1
                q.append(n)
                l += 1
            else:
                r += 1
                l += 1
        for t in q:
            self.graph.add_edge(t, i)
        
        n = r
        q = []
        while i!= r and r >= l:
            if sum(self.graph.getRow(r)) < self.options:
                self.graph.add_edge(r, i)
                r -= 1
            elif r < len(self.people) -1:
                n += 1
                while sum(self.graph.getRow(n)) == self.options:
                    n += 1
                q.append(r)
                r -=1
        for t in q:
            self.graph.add_edge(t, i)
    
    #no one node can have more than #options edges or else theres a possibility that one person or more get left out
    #rows and vertix are the sorted array of people
    #row is gift givers columns is gift recievers
    def findMatches(self, options):
        self.fileRead()
        self.peopleSort()

        def helper(self):
            self.graph = Graph(self.people)
            self.options = options
            i = random.randint(0, len(self.people) - 1) #the first person chosen has a high likely hood that all potential matches are similar to them, meanwhile the last person has very poor probability, so make the first person random for fairness
            t = i
            done = 0
            while not(done):
                l, r = self.closestValues(self.people, t, options)
                self.add_potential_matches(l, r, t)
                t = (t + 1) % len(self.people)
                if t == i:
                    done = 1
            return self.matches()
        
        while True:
            try:
                return helper(self)
            except(ValueError):
                continue

    def matches(self):
        rows = [a for a in range(len(self.people))]
        cols = [a for a in range(len(self.people))]
        matches = []

        while len(rows) != 0:
            v = random.choice(rows)
            r = self.graph.getRow(v)
            v2 = r.index(1)
            while v2 not in cols:
                self.graph.remove_edge(v, v2)
                v2 = r.index(1)
            self.graph.remove_edge(v, v2)
            rows.remove(v)
            cols.remove(v2)

            v = self.people[v]
            v2 = self.people[v2]

            matches.append((v, v2))
        
        if (len(matches) < len(self.people)):
            raise ValueError

        self.matched = matches
        
        return matches
    
    def sendEmails(self, port, sender_email, password):
        smtpServer = "smtp.gmail.com"
        context = ssl.create_default_context()
        try:
            server = smtplib.SMTP(smtpServer,port)
            server.ehlo() # Can be omitted
            server.starttls(context=context) # Secure the connection
            server.ehlo() # Can be omitted
            server.login(sender_email, password)
            for i in self.matched:
                giftGiver= i[0]
                giftReciever = i[1]
                reciever_email = giftGiver.email
                message = "Hello %s \n \t You have matched with %s and this is how they answered the following questions: \n"
                for k in giftReciever.qOrder:
                    continue
        except Exception as e:
            # Print any error messages to stdout
            print(e)
        finally:
            server.quit() 


"""
Can use a pseudo random function of the sorted list of degree of matches, then with the function allow an input of randomenss, 1 being max randomness and decimal points till 0 means least randomness
This function will map either people who match very well close together in a set space or randomly either far apart or close together
"""