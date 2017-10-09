from constants import Constants
from random import randint, uniform

class GeneticAlgorithm:

    def __init__(self):
        # This is the array of agents in the population (starting with a population of around 20)
        self._agent_array = []
        # This is the target result for the genetic algorithm to try and work towards
        _target_result = 0.80

    def create_agents(self):
        for i in range(20):
            self._agent_array.append(self.create_random_constants_class())

    def crossover(self, agent1, agent2):
        pass

    def mutate(self):
        pass

    def select(self):
        pass

    def start(self):
        pass

    def create_random_constants_class(self):
        """
        Creates an instance of a constants class with random variables assigned
        :return: return the instance
        """
        constants_class = Constants()
        constants_class.set_pattern_len(randint(20, 50))
        constants_class.set_num_pattern_req(randint(2000, 10000))
        constants_class.set_required_difference(uniform(0.001, 0.0001))
        constants_class.set_interval_size(randint(1, 20))
        i = randint(10, 100)
        constants_class.set_ema_a_period(i)
        constants_class.set_ema_b_period(randint(i, i + 100))
        constants_class.set_signal_period(randint(5, i))
        constants_class.set_cci_period(randint(10, 50))
        constants_class.set_cci_constant(0.015)
        constants_class.set_typical_price_ema_period(randint(10, 100))
        return constants_class