#static class, will breed, mix and evaluate fitness, it's only function is to receive a generation and output the next one

import random
from individual import Individual
import math

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
                    pass
                elif prev_sock is None:
                    pass
                else:
                    fitness -= 5
        if (shoes_items) > 1:
            prev_shoe = None
            for shoe in individual.configuration["shoes"]:

                if shoe == prev_shoe:
                    pass
                elif prev_shoe is None:
                    pass
                else:
                    fitness -= 5
                prev_shoe = shoe

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
        return fitness

    #receives a generation and returns the next generation
    @staticmethod
    def breed(generation, my_registers):
        #notes:
            #dna diversity is dying 2 quickly, lets pump it up
            #first of all, we're gonna create twice as many offspring
            #and we're only gonna keep the half with the best fitness
        gen_size = len(generation)
        my_new_gen = []

        gen_parents = []

        selection_pool = []

        


        #selecting top performer of this generation
        top_performer = Individual()
        second_top = Individual()

        sorted_prev_gen = sorted(generation, key=Individual.get_fitness)
        sorted_prev_gen.reverse()
        #for i in range(0, len(sorted_prev_gen)):
            #print("old:{}, calculated:{}".format(sorted_prev_gen[i].fitness, Genetic.fitness(sorted_prev_gen[i])))

        top_performer.configuration = sorted_prev_gen[0].configuration
        Genetic.fitness(top_performer)

        second_top.configuration = sorted_prev_gen[1].configuration
        Genetic.fitness(second_top)

        #print("top fitness:{} calculated: {}".format(top_performer.fitness, Genetic.fitness(top_performer)))
        #print("2 fitness:{} calculated: {}".format(second_top.fitness, Genetic.fitness(second_top)))

 


        #weighted random
        for individual in generation:      
            #print(individual.fitness)
            #print("repetitions:{}".format(math.floor(individual.fitness / 10)))
            selection_pool += int(math.floor(individual.fitness / 10))  * [individual]
            selection_pool += [individual]

        #print(selection_pool)

        #print("random choices:")

        #parent generation
        for i in range(0, gen_size):
            my_aux = random.choice(selection_pool)
            my_new_parent = Individual()
            my_new_parent.configuration = dict(my_aux.configuration)

            #print(my_new_parent)
            gen_parents.append(my_new_parent)

        #print(gen_parents)


        #creating offspring
        for i in range(0, 2 * gen_size):
            if i % 2 == 1:
                offspring1 = Individual()
                offspring2 = Individual()
                parent1 = gen_parents[(i % gen_size)-1]
                parent2 = gen_parents[(i % gen_size)]

                mirror = random.randint(0,4)

                #print(parent1)
                #print(parent2)
                counter = 0
                for k, v in offspring1.configuration.items():
                    if counter <= mirror:
                        offspring1.configuration[k] = list(parent1.configuration[k])
                        offspring2.configuration[k] = list(parent2.configuration[k])
                    else:
                        offspring1.configuration[k] = list(parent2.configuration[k])
                        offspring2.configuration[k] = list(parent1.configuration[k])
                    counter+=1
                #print("with a mirror of: {} created:".format(mirror))
                #print(offspring1)
                #print(offspring2)
                my_new_gen.append(offspring1)
                my_new_gen.append(offspring2)

            else:
                pass



        #mutate
        my_new_gen = Genetic.mutate(my_new_gen, my_registers)
        


        #evaluating fitness for new generation
        for item in my_new_gen:
            Genetic.fitness(item)


        #culling generation
        sorted_gen = sorted(my_new_gen, key=Individual.get_fitness)
        
        while len(sorted_gen) > gen_size - 2:
            del sorted_gen[0]

        
            
        sorted_gen.reverse()
        #for item in sorted_gen:
            #print(item.fitness)
        
        #inserting top of last generation
        

        #print("top fitness:{} calculated: {}".format(top_performer.fitness, Genetic.fitness(top_performer)))
        #print("2 fitness:{} calculated: {}".format(second_top.fitness, Genetic.fitness(second_top)))
        sorted_gen.append(top_performer)
        sorted_gen.append(second_top)

        #print("replaced the weakest")

        #for item in sorted_gen:
            #print("result: {} calc: {}".format(item.fitness, Genetic.fitness(item)))
        
        #print("MY weakest:{}, FITNESS: {}".format(sorted_gen[-3].configuration, sorted_gen[-3].fitness))


        return sorted_gen

    @staticmethod
    def mutate(generation, my_registers):
        #notes:
            

        #modifying the quantity of items per slot
        meta_chance = 10
        for individual in generation:
            #print(individual)
            for k, v in individual.configuration.items():
                roulette = random.randint(0, 1000)

                if roulette < meta_chance / (1 + len(v)):
                    #print("triggering a meta change for {}".format(k))
                    #print("inserting")
                    #gonna decide if we add or take
                    if len(individual.configuration[k]) > 1:
                        adding = (1 < random.randint(0,len(individual.configuration[k])))
                    else:
                        adding = True

                    if adding:
                        to_insert = (random.choice(my_registers))
                        individual.add(k, to_insert)
                    else:
                        individual.remove(k)
            #print(individual)
            #print("----------<>-----------")
        
        #print("----------------------------------------now for inner--------------------------")
        modi_chance = 5
        for individual in generation:
            #print(individual)
            for k, v in individual.configuration.items():
                for i in range(0, len(v)):
                    roulette = random.randint(0, 500)
                    if roulette < modi_chance:
                        #print("triggering an inner change")
                        new_item = random.choice(my_registers)
                        #print(new_item)
                        while new_item == v[i]:
                            new_item = random.choice(my_registers)
                        #print("{} became {}".format(v[i], new_item))
                        individual.configuration[k][i] = new_item
                   

            #print(individual)
            #print("----------<>-----------")

        return generation

