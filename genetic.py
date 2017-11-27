#static class, will breed, mix and evaluate fitness, it's only function is to receive a generation and output the next one

import random
from individual import Individual

class Genetic:

    @staticmethod
    def fitness(individual):
        fitness = 100

        chest_items = len(individual.configuration["chest"])
        fitness -= (abs(1-chest_items)) * 4

        head_items = len(individual.configuration["head"])
        fitness -= (abs(1-head_items)) * 5

        pants_items = len(individual.configuration["pants"])
        fitness -= (abs(1-pants_items)) * 6

        socks_items = len(individual.configuration["socks"])
        fitness -= (abs(2-socks_items)) * 10

        shoes_items = len(individual.configuration["shoes"])
        fitness -= (abs(2-shoes_items)) * 10

        #high fitness if its the same sock/shoe
        if (socks_items) > 1:
            prev_sock = None
            for sock in individual.configuration["socks"]:
                if sock == prev_sock:
                    fitness += 15
                    break
                elif prev_sock is None:
                    pass
                else:
                    fitness -= 5
        if (shoes_items) > 1:
            prev_shoe = None
            for shoe in individual.configuration["shoes"]:
                if shoe == prev_shoe:
                    fitness += 15
                    break
                elif prev_shoe is None:
                    pass
                else:
                    fitness -= 5

        #calculating fitness for weird accesories
        wrist_used = 0
        ear_used = 0
        neck_used = 0
        for item in individual.configuration["accessory"]:
            if item == "watch":
                wrist_used += 1
            elif item == "necklace":
                neck_used += 1
            elif item == "earring":
                ear_used += 1
            elif item == "wristband":
                wrist_used += 1
        if wrist_used > 2:
            fitness -= abs(2 - wrist_used) * 5
        if ear_used > 5:
            fitness -= abs(5 - ear_used) * 5
        if neck_used > 1:
            fitness -= abs(1 - neck_used) * 5

        #calculating fitness for appropiate slot
        chest_possib = ["shirt","sweater","blouse"]
        head_possib = ["beanie","hat","bow"]
        pants_possib = ["denim pants","sweatpants","shorts", "leggings"]
        socks_possib = ["sock"]
        shoes_possib = ["tennis","sandals","shoes"]
        accessory_possib = ["watch","necklace","wristband","earring"]

        for v in individual.configuration["head"]:
            if not v in head_possib :
                #print("offender:{}".format(v))
                fitness-= 10

        #print("fitness: {}".format(fitness))

        for v in individual.configuration["chest"]:
            if not v in chest_possib :
                #print("offender:{}".format(v))
                fitness-= 10

        #print("fitness: {}".format(fitness))

        for v in individual.configuration["pants"]:
            if not v in pants_possib :
                #print("offender:{}".format(v))
                fitness-= 10

        #print("fitness: {}".format(fitness))
        
        for v in individual.configuration["socks"]:
            if not v in socks_possib :
                #print("offender:{}".format(v))
                fitness-= 10

        #print("fitness: {}".format(fitness))

        for v in individual.configuration["shoes"]:
            if not v in shoes_possib :
                #print("offender:{}".format(v))
                fitness-= 10
        #print("fitness: {}".format(fitness))

        for v in individual.configuration["accessory"]:
            if not v in accessory_possib :
                #print("offender:{}".format(v))
                fitness-= 10
        #print("fitness: {}".format(fitness))

        


        individual.fitness = fitness
        return

    #receives a generation and returns the next generation
    @staticmethod
    def breed(generation, my_registers):
        gen_size = len(generation)
        my_new_gen = []

        gen_parents = []

        selection_pool = []


        #weighted random
        for individual in generation:      
            selection_pool += individual.fitness * [individual]
            selection_pool += [individual]

        #parent generation
        for i in range(0, gen_size):
            gen_parents.append(random.choice(selection_pool))


        #creating offspring
        for i in range(0, gen_size):
            if i % 2 == 1:
                offspring1 = Individual()
                offspring2 = Individual()
                parent1 = gen_parents[i-1]
                parent2 = gen_parents[i]
                mirror = random.randint(1,4)

                counter = 0
                for k, v in offspring1.configuration.items():
                    if counter <= mirror:
                        offspring1.configuration[k] = parent1.configuration[k]
                        offspring2.configuration[k] = parent2.configuration[k]
                    else:
                        offspring1.configuration[k] = parent2.configuration[k]
                        offspring2.configuration[k] = parent1.configuration[k]
                    counter+=1
                my_new_gen.append(offspring1)
                my_new_gen.append(offspring2)

            else:
                pass


        #mutate
        my_new_gen = Genetic.mutate(my_new_gen, my_registers)
        


        #evaluating fitness for new generation
        for item in my_new_gen:
            Genetic.fitness(item)

        return my_new_gen

    @staticmethod
    def mutate(generation, my_registers):

        #modifying the quantity of items per slot
        meta_chance = 1
        for individual in generation:
            for k, v in individual.configuration.items():
                roulette = random.randint(0, 500)
                if roulette < meta_chance:
                    #print("inserting")
                    #gonna decide if we add or take
                    if len(individual.configuration[k]) > 0:
                        adding = (1 == random.randint(0,1))
                    else:
                        adding = True

                    if adding:
                        to_insert = (random.choice(my_registers))
                        individual.add(k, to_insert)
                    else:
                        individual.remove(k)

        modi_chance = 5
        for individual in generation:
            for k, v in individual.configuration.items():
                for item in v:
                    roulette = random.randint(0, 500)
                    if roulette < modi_chance:
                        #print("modifying")
                        item = random.choice(my_registers)
                   

        

        return generation

