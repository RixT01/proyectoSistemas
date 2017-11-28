import random

class Individual:
    def __init__(self):
        self.configuration = {
            "head":[],
            "chest":[],
            "pants":[],
            "socks":[],
            "shoes":[],
            "accessory":[]
        }

        self.fitness = 0

    def add(self, k, val):
        self.configuration[k].append(val)

    def remove(self, k):
        ind_to_delete = random.randint(0, len(self.configuration[k])-1)
        del self.configuration[k][ind_to_delete]

    @staticmethod
    def get_fitness(self):
        return self.fitness

    def __str__(self):
        my_str = "------\n"

        for k, v in self.configuration.items():
            my_str+="{} has: {}\n".format(k, v)



        my_str+="------\n"

        return my_str


    def randomize(self, possible_items):
        
        for k, v in self.configuration.items():
            self.configuration[k].append(possible_items[random.randint(0, len(possible_items) -1)])
