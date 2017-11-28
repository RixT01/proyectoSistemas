from individual import Individual
from genetic import Genetic



def main():

    population_size = 10
    my_registers = read_registries()
    initial_population = []

    #establishing a population with non-negative fitness
    for i in range(0, population_size):
        myInd = Individual()
        while myInd.fitness <= 0:
            myInd.randomize(my_registers)
            Genetic.fitness(myInd)

        initial_population.append(myInd)

    new_gen = Genetic.breed(initial_population, my_registers)

    #evaluating till we get top == 100
    top_fitness = 0
    try:
        while top_fitness < 100:
        
            if top_fitness != 0:
                new_gen = Genetic.breed(new_gen, my_registers)


            for item in new_gen:
                if item.fitness > top_fitness:
                    top_fitness = item.fitness
                    #print("{} broke to: {}".format(item, top_fitness))

    except KeyboardInterrupt:
        print_all_gen(new_gen)

    
    

    

def print_all_gen(generation):
    for indiv in generation:
        print("{} with a fitness:{}".format(indiv, indiv.fitness))


def read_registries():
    items_result = []
    f = open("clothing.txt")
    for line in f:
        if line[0] == "-" or line[0] == "\n":
            next
        else:
            items_result.append(line.replace("\n", ""))
    return items_result

def test():
    population_size = 10
    my_registers = read_registries()
    initial_population = []

    #establishing a population with non-negative fitness
    for i in range(0, population_size):
        myInd = Individual()
        while myInd.fitness <= 0:
            myInd.randomize(my_registers)
            Genetic.fitness(myInd)

        initial_population.append(myInd)

    
    #print_all_gen(initial_population)
    #print("----------------")

    print("\n/////////////////////////////////////////////GENERATION: {}".format(0))
    new_gen = Genetic.breed(initial_population, my_registers)
    for i in range(1, 50):
        print("\n/////////////////////////////////////////////GENERATION: {}".format(i))
        new_gen = Genetic.breed(new_gen, my_registers)
        #print_all_gen(new_gen)




if __name__ == "__main__":
   #main()
   test()


