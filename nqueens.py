import random
import math

class Solver_8_gueens:

    # Конструктор
    def __init__(self, pop_size=8, cross_prob=0.85, mut_prob=0.75):
        self.N = pop_size
        self.PC = cross_prob
        self.PM = mut_prob

    # ОСНОВНОЕ РЕШЕНИЕ --------------------------------------------------------
    def solve(self, min_fitness=0.99, max_epochs=100):
        
        # Создание стартовой популяции
        start_pop = [[0] * self.N for i in range(self.N)]
        i = 0
        while i < self.N:
            start_pop[i] = self.create_entity()
            i += 1

        # ОСНОВНОЙ ЦИКЛ
        epochs = 0
        F = 0
        while F <= min_fitness:

            # Расчёт функций стартовой популяции
            functions = [0] * self.N
            i = 0
            while i < self.N:
                functions[i] = self.fitness_function(start_pop[i])
                if functions[i] > min_fitness:
                    best_fit = functions[i]
                    F = functions[i]
                    epochs_num = epochs
                    visualization = self.print_entity(start_pop[i])
                    break
                i += 1

            # Создание рулетки
            roulette = [0] * self.N
            roulette = self.roulette_wheel(functions)

            # Скрещивание родителей, создание промежуточной популяции
            middle_pop = self.create_middle(start_pop, roulette)

            # Мутация
            last_pop = self.mutation_pop(middle_pop)

            # Замена стартовой популяции новой
            start_pop = last_pop

            epochs += 1
            if epochs >= 100:
                best_fit = max(functions)
                epochs_num = epochs
                visualization = self.print_entity(start_pop[functions.index(best_fit)])
                best_fit = str(max(functions)) + " Fitness function should be 1.0! Wrong solution."
                break

        return best_fit, epochs_num, visualization
    # -------------------------------------------------------------------------

    # Создание особи
    def create_entity(self):
        base_entity = [0b000, 0b001, 0b010, 0b011, 0b100, 0b101, 0b110, 0b111]

        i = self.N - 1
        while i >= 0:
            j = random.randint(0,i)
            tmp = base_entity[j]
            base_entity[j] = base_entity[i]
            base_entity[i] = tmp
            i -= 1

        return base_entity

    # Выпод особи на экран в матричном виде
    def print_entity(self, entity):
        i = 0
        list = ""
        while i < self.N:
            j = 0
            while j < self.N:
                if i == entity[j]:
                    list = list + "Q"
                else:
                    list = list + "+"
                j += 1
            list = list + "\n"
            i += 1

        visual = list

        return visual

    # Расчёт фитнес-функции одной особи
    def fitness_function(self, entity):
        check = 0
        j = self.N - 1
        max = 0
        while j >= 1:
            max = max + j
            i = j - 1
            while i >= 0:
                if math.fabs(entity[j] - entity[i]) != j - i:
                    check += 1
                i -= 1
            j -= 1

        function = round(check / max, 2)

        return function

    # Создание колеса рулетки
    def roulette_wheel(self, func):
        sum = 0
        for f in func:
            sum = round(sum + f, 2)

        i = 0
        prob = [0] * len(func)
        roulette = [0] * len(func)
        while i < len(func):
            prob[i] = round(func[i] / sum, 2)
            if i == 0:
                roulette[i] = round(prob[i], 2)
            if i > 0:
                roulette[i] = round(roulette[i-1] + prob[i], 2)
            i += 1

        return roulette

    # Создание промежуточной популяции
    def create_middle(self, pop, roulette):
        second_pop = [[0] * self.N for i in range(self.N)]
        num = 0
        while num < self.N:
            i = 0
            prob = random.random()
            while i < len(roulette):
                if prob < roulette[i]:
                    pc = random.random()
                    if pc >= self.PC:
                        second_pop[num] = self.crossing_parents(pop[i])
                        num += 1
                        break
                    break
                i += 1

        return second_pop

    # Скрещивание родителей
    def crossing_parents(self, parent):
        new_entity = [0] * len(parent)
        k = random.randint(0, self.N - 2)

        second_part = [0] * (self.N - k)
        s = 0
        i = k
        while i < 8:
            second_part[s] = parent[i]
            s += 1
            i += 1

        m = 0
        while m < len(second_part) - 1:
            r = random.randint(0, m + 1)
            tmp = second_part[r];
            second_part[r] = second_part[m];
            second_part[m] = tmp;
            m += 1

        step = 0
        j = 0
        while j < self.N:
            if j < k:
                new_entity[j] = parent[j]
            else:
                new_entity[j] = second_part[step]
                step += 1
            j += 1

        return new_entity

    # Мутация промежуточной популяции
    def mutation_pop(self, pop):
        third_pop = pop
        i = 0
        while i < self.N:
            pm = random.random()
            if pm <= self.PM:
                third_pop[i] = self.mutation_entity(third_pop[i])
            i += 1

        return third_pop

    # Мутация особи
    def mutation_entity(self, entity):
        x = random.randint(0, self.N - 1)
        y = random.randint(0, self.N - 1)
        tmp = entity[x]
        entity[x] = entity[y]
        entity[y] = tmp

        return entity