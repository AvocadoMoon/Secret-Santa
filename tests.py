import unittest
import SecretSanta

class TestSecretSanta(unittest.TestCase):

    def setUp(self):
        posQ = ["time", "Name", '"Meaningful"', '"Surprise me"', '"Dogs"', '"Yes"', None, '"Yes"', '"Yes"', None, None, None]
        negQ = ["time", "Name", '"Expensive"', '"I know what I want"', '"Cats"', '"No"', None, '"No"', '"No"', None, None, None]
        impQ = ['"Expensive"', '"Meaningful"', '"Surprise me"', '"I know what I want"']
        weight = 5
        fl = r"C:\Users\Zeke\Document\Programming\Jokes\Secret-Santa\Secret Santa Even.csv"
        laptop = r"E:\Downloads\Programing\Jokes\Secret-Santa\Secret Santa Even.csv"
        self.ss = SecretSanta.SecretSanta(laptop, negQ, posQ, impQ, weight)
    
    def test_close_values(self):
        #setup
        similarValues = 4
        index = 0
        n = 10
        lis = [a for a in range(n)]
        ss = self.ss

        #0 edge case
        l, r = ss.closestValues(lis, index, similarValues)
        lt = index + 1
        rt = index + similarValues
        assert(l == lt)
        assert(r == rt)

        #end of list edge case
        index = n-1
        l , r = ss.closestValues(lis, index, similarValues)
        lt = index-similarValues
        rt = index - 1
        assert(lt == l)
        assert(rt == r)

        #middle of list
        index = n//2
        l, r = ss.closestValues(lis, index, similarValues)
        lt = index - (similarValues // 2)
        rt = index + (similarValues // 2)
        assert(lt == l)
        assert(rt == r)
    
    def test_find_matches(self):
        ss = self.ss
        l = ss.findMatches(5)
        for i in l:
            print(i[0].name, i[1].name)
    
    def test_file_read(self):
        ss = self.ss
        










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