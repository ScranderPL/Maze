import random


def recursive_backtracker(maze_graphics, maze):

    # W tej liście przechowujemy komórki labiryntu które już odwiedziliśmy, komórki z tej listy są potem przetwarzane
    # w pętli poniżej
    visited_stack = []

    # Ten algorytm startuje w losowym miejscu pustego jeszcze labiryntu, dlatego musimy wylosować
    # naszą pozycję
    init_x = random.randint(1, maze.x_size)
    init_y = random.randint(1, maze.y_size)

    # Jako że wybraliśmy już naszą pozycję początkową, to możemy ją oznaczyć jako odwiedzoną
    visited_stack.append([init_x, init_y])

    # W komórkach labiryntu możemy przechowywać różne informacje, które mogą nam pomóc w trakcie jego tworzenia,
    # w tym wypadku pomaga nam to natychmiast określić czy dana komórka była już odwiedzona ('V', z ang. visited).
    # Dodatkowo jest to informacja dla biblioteki do wyświetlania, w jakim stanie jest nasz labirynt.
    maze.set_cell(init_x, init_y, 'V')

    # Algorytm ściąga ze wspomnianej wcześniej listy odwiedzone komórki jedna po drugiej. W tym samym kroku, może też
    # dodać do niej kolejne komórki. Kiedy wszystko zostanie przetworzone, lista będzie pusta, a pętla skończy się.
    while visited_stack:
        # Pobieramy z listy ostatnio dodaną komórkę, nazwijmy ją aktualną
        current_cell = visited_stack.pop()

        # Uwaga: To służy do wyświetlania, nie ma wpływu na działanie algorytmu
        maze.set_cell(current_cell[0], current_cell[1], 'C')

        # Bierzemy wszystkich sąsiadów (maks. 4) aktualnej komórki, którzy nie byli jeszcze odwiedzeni
        neighbours = maze.get_cell_not_visited_neighbours(current_cell[0], current_cell[1])

        # Jeśli nie ma takich sąsiadów, to algorytm nie ma gdzie się udać, dlatego sprawdzamy poprzenie komórki
        # z listy, aż nie uda nam się pójść dalej
        if not neighbours:
            # Uwaga: To służy do wyświetlania, nie ma wpływu na działanie algorytmu
            if maze_graphics:
                maze_graphics.redraw(maze)

            # Oznaczamy aktualną komórkę jako odwiedzoną i przetworzoną (nie znajduje się już na liście)
            maze.set_cell(current_cell[0], current_cell[1], 'V')

            # Przechodzimy to kolejnej iteracji pętli
            continue

        # Jeśli aktualna komórka ma nieodwiedzonych sąsiadów, to dodajemy ją z powrotem do naszej listy, abyśmy byli
        # w stanie wrócić do niej rekurencyjnie
        visited_stack.append(current_cell)

        # Losowo wybieramy jednego z sąsiadów aktualnej komórki
        chosen_neighbour = random.choice(neighbours)

        # Uwaga: To służy do wyświetlania, nie ma wpływu na działanie algorytmu
        maze.set_wall(current_cell[0], current_cell[1], chosen_neighbour[0], chosen_neighbour[1], 'C')

        # Oznaczamy wybranego sąsiada jako odwiedzonego i dodajemy go do naszej listy
        maze.set_cell(chosen_neighbour[0], chosen_neighbour[1], 'V')
        visited_stack.append(chosen_neighbour)

        # Uwaga: To służy do wyświetlania, nie ma wpływu na działanie algorytmu
        if maze_graphics:
            maze_graphics.redraw(maze)

        # Początkowo labirynt ma wszystkie ściany wypełnione, wraz z kolejnym krokami algorytmu kolejne ściany są
        # usuwane. W tym momencie następuje usunięcie ściany między aktualną komórką, a jej wybranym wcześniej sąsiadem
        maze.set_wall(current_cell[0], current_cell[1], chosen_neighbour[0], chosen_neighbour[1], ' ')

        # Oznanczamy aktualną komórkę jako oznaczoną
        maze.set_cell(current_cell[0], current_cell[1], 'V')



def hunt_and_kill(maze_graphics, maze):

    def hunt_and_kill_scan(maze_graphics, maze):

        for y in range(1, maze.y_size + 1):
            for x in range(1, maze.x_size + 1):
                tmp_cell = maze.get_cell(x, y)

                if tmp_cell == 'V':
                    neighbours = maze.get_cell_not_visited_neighbours(x, y)

                    if not neighbours:
                        continue

                    return [x, y], random.choice(neighbours)

        return None, None

    curr_x = random.randint(1, maze.x_size)
    curr_y = random.randint(1, maze.y_size)
    curr_cell = [curr_x, curr_y]

    while True:
        maze.set_cell(curr_cell[0], curr_cell[1], 'V')
        neighbours = maze.get_cell_not_visited_neighbours(curr_cell[0], curr_cell[1])

        if not neighbours:
            curr_cell, next_cell = hunt_and_kill_scan(maze_graphics, maze)
            if not curr_cell:
                return
        else:
            next_cell = random.choice(neighbours)

        maze.set_wall(curr_cell[0], curr_cell[1], next_cell[0], next_cell[1], ' ')
        curr_cell = next_cell



def hunt_and_kill_mod(maze_graphics, maze, reuse = False):

    def hunt_and_kill_scan(maze_graphics, maze):

        for y in range(1, maze.y_size + 1):
            for x in range(1, maze.x_size + 1):

                if maze.get_cell(x, y) == 'F':
                    neighbours = maze.get_cell_neighbours(x, y, 'I')

                    if not neighbours:
                        continue

                    return random.choice(neighbours)

        return None, None

    if reuse:
        stop = True

        # step required for maze reuse
        for y in range(1, maze.y_size + 1):
            for x in range(1, maze.x_size + 1):

                if maze.get_cell(x, y) == 'F':
                    neighbours = maze.get_cell_neighbours(x, y, 'I')

                    if not neighbours:
                        continue

                    neigh_x, neigh_y = random.choice(neighbours)
                    maze.set_wall(neigh_x, neigh_y, x, y, ' ')
                    curr_x, curr_y = x, y
                    stop = False
                    break

            if not stop:
                break

        if stop:
            return

    else:
        curr_x = random.randint(1, maze.x_size)
        curr_y = random.randint(1, maze.y_size)

    while True:
        maze.set_cell(curr_x, curr_y, 'I')
        neighbours = maze.get_cell_neighbours(curr_x, curr_y, 'O')

        for x, y in neighbours:
            maze.set_cell(x, y, 'F')

        neighbours =  maze.get_cell_neighbours(curr_x, curr_y, 'F')

        if not neighbours:
            curr_x, curr_y = hunt_and_kill_scan(maze_graphics, maze)

            if not curr_x:
                return

            neighbours = maze.get_cell_neighbours(curr_x, curr_y, 'F')

        neigh_x, neigh_y = random.choice(neighbours)
        maze.set_wall(curr_x, curr_y, neigh_x, neigh_y, ' ')
        curr_x, curr_y = neigh_x, neigh_y



def eller(maze_graphics, maze):

    def get_set(set_list, x_it, y_it):
        for set_it in set_list:
            if (x_it, y_it) in set_it:
                return set_it

    # W tej zmiennej przechowujemy informację o tym, ile zbiorów zostało utworzonych do tej pory.
    set_counter = 0
    sets = []


    # W tej pętli tworzymy osobny obszar (zbiór) dla każdej komórki pierwszego rzędu (Ilustracja 2.)
    for x in range(1, maze.x_size + 1):
        new_set = set()
        sets.append(new_set)
        sets[-1].add((x, 1))
        set_counter = set_counter + 1
        maze.set_cell(x, 1, set_counter)

    # W tym algorytmie chodzimy po wierszach, jeden po drugim, w przeciwieństwie do drugiego algorytmu, który działa
    # na pojedynczych komórkach i ich sąsiadach.
    for y in range(1, maze.y_size+1):

        # Uwaga: To służy do wyświetlania, nie ma wpływu na działanie algorytmu
        if maze_graphics:
            maze_graphics.redraw(maze)

        # W tej pętli łączymy losowo zbiory znajdujące się w danym wierszu, robimy to poprzez usuwanie ścian między
        # między wylosowanymi komórkami, które są w różnych zbiorach (Ilustracja 3.)
        for x in range(1, maze.x_size):

            # W tym miejscu możemy wpływać na to jak często będziemy łączyć komórki
            if random.random() < 0.5 or y == maze.y_size:
                sets_ready = 0

                # Tutaj sprawdzamy czy w komórka w aktualnej kolumnie ma obcego sąsiada
                for set_t in sets:

                    if (x, y) in set_t:
                        if (x+1, y) in set_t:
                            break
                        set_a = set_t
                        sets_ready = sets_ready + 1
                    elif (x+1, y) in set_t:
                        set_b = set_t
                        sets_ready = sets_ready + 1

                    if sets_ready == 2:
                        break

                # Jeśli znajdziemy rzeczywiście jest mamy sąsiada z innego zbioru to wykonujemy poniższy blok kodu
                if sets_ready == 2:

                    # Usuwamy znalezione zbiory ze zbioru naszych zbiorów
                    sets.remove(set_a)
                    sets.remove(set_b)

                    # Łączymy znalezione zbiory
                    set_a = set_a.union(set_b)

                    # Dodajemy je jako jeden wspólny zbiór
                    sets.append(set_a)

                    # W tym miescu oznaczamy komórki które zostały wchłonięte do innego zbioru
                    for val in set_a:
                        maze.set_cell(val[0], val[1], maze.get_cell(x, y))

                    # Usuwamy naszą ścianę, po czym przechodzimy do kolejnej kolumny w pętli
                    maze.set_wall(x, y, x + 1, y, ' ')

        # Jeśli aktualny wiersz był naszym ostatnim, to algorytm kończy się
        if y == maze.y_size:
            return


        # Teraz musimy usunąć ściany do następnego wiersza, każdy zbiór powinien miec przynajmniej jedno takie
        # połączenie, gdyby tak nie było, to dany zbiór zostałby na stałe wyizolowany, przez co nasz algorytm
        # nie byłby idealny

        processed_sets = set()

        # Wybieramy losową kolejność kolumn w których będziemy rozważać usunięcie poziomej ściany do kolejnego wiersza
        x_range = list(range(1, maze.x_size+1))
        random.shuffle(x_range)

        # W tej pętli przechodzimy po kolumnach w losowej kolejności
        for x in x_range:
            # Tutaj mamy kolejny element losowy który możemy zmieniać. Jeśli dany zbiór nie ma jeszcze przejścia w dół,
            # to dodajemy je, jeśli natomiast posiada przynajmniej jedno takie przejście, to losowo określamy czy damy
            # mu kolejne (Ilustracja 4.)
            if (maze.get_cell(x, y) not in processed_sets) or random.random() < 0.5:
                processed_sets.add(maze.get_cell(x, y))
                maze.set_wall(x, y, x, y+1, ' ')
                maze.set_cell(x, y + 1, maze.get_cell(x, y))
                set_a = get_set(sets, x, y)
                sets.remove(set_a)
                set_a.add((x, y+1))
                sets.append(set_a)
            # Jeśli w danej kolumnie nie tworzymy przejścia, to musimy utworzyć nowy zbiór, w którym znajdzie się
            # tylko jedna komórka z następnego wiersza (Ilustracja 5.)
            else:
                new_set = set()
                sets.append(new_set)
                sets[-1].add((x, y+1))
                set_counter = set_counter + 1
                maze.set_cell(x, y+1, set_counter)