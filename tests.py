import unittest
import SecretSanta

class TestSecretSanta(unittest.TestCase):
    
    def test_close_values(self):
        #setup
        similarValues = 4
        index = 0
        n = 10
        l = [a for a in range(n)]
        ss = SecretSanta.SecretSanta(None, None, None, None, None)

        #0 edge case
        t = ss.closestValues(l, index, similarValues)
        t2 = [a for a in range(index + 1, index + 1 + similarValues)]
        assert(t == t2)

        #end of list edge case
        index = n-1
        t = ss.closestValues(l, index, similarValues)
        t2 = [a for a in range(index-similarValues, n-1)]
        assert(t == t2)

        #middle of list
        index = n//2
        t = ss.closestValues(l, index, similarValues)
        t2 = [a for a in range(index - (similarValues // 2), index + (similarValues // 2) + 1) if a != index]
        assert(t == t2)
    
    def test_find_matches(self):
        posQ = ["time", "Name", '"Meaningful"', '"Surprise me"', '"Dogs"', '"Yes"', None, '"Yes"', '"Yes"', None, None, None]
        negQ = ["time", "Name", '"Expensive"', '"I know what I want"', '"Cats"', '"No"', None, '"No"', '"No"', None, None, None]
        impQ = ['"Expensive"', '"Meaningful"', '"Surprise me"', '"I know what I want"']
        weight = 5
        fl = r"C:\Users\Zeke\Document\Programming\Jokes\Secret-Santa\Secret Santa Odd.csv"
        ss = SecretSanta.SecretSanta(fl, negQ, posQ, impQ, weight)
        l = ss.findMatches(5)
        print(l)









class TestPerson(unittest.TestCase):

    #runs this everytime before a test
    def setUp(self):
        self.person = SecretSanta.Person("Kyle")
    
    def emptyChoices(self):
        self.person.multipleChoice = []
        self.person.negMultipleChoice = []

    def test_sum(self):
        weight = 5
        answer = "yo"

        #0 sum
        self.person.addMultipleChoice(answer, True) #dosent matter the answer since the boolean is the only thing that affects values
        self.person.addMultipleChoice(answer, False)
        self.person.summation([], weight)
        self.assertEqual(self.person.sum, 0)
        self.emptyChoices()

        #positive sum weight
        self.person.addMultipleChoice(answer, False)
        self.person.summation([answer], weight)
        self.assertEqual(self.person.sum, weight)
        self.emptyChoices()

        #negative sum weight
        self.person.addMultipleChoice(answer, True)
        self.person.summation([answer], weight)
        self.assertEqual(self.person.sum, (0 - weight))
    

if __name__ == "__main__":
    unittest.main()