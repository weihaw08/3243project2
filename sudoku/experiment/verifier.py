import os

def pick_difficulty(num):
    if num == 1:
        return 'easy'
    elif num == 2:
        return 'medium'
    elif num == 3:
        return 'expert'
    else:
        return 'evil'

def read_puzzle(file_path):
    f = open(file_path, 'r')
    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0
    f.close()
    return puzzle

def compare(puzzle_one, puzzle_two):
    for i in range(9):
        for j in range(9):
            if puzzle_one[i][j] != puzzle_two[i][j]:
                return False
    return True

def get_heuristic_name(num):
    if num == 1:
        return 'AC3 only'
    elif num == 2:
        return 'Normal only'
    elif num == 3:
        return 'Normal + MCV'
    elif num == 4:
        return 'Normal + MCV + LRV'


def verify(puzzle):
    for i in range(9):
        for j in range(9):
            for k in range(j + 1, 9):
                if puzzle[i][j] == puzzle[i][k]:
                    return False
    
    for i in range(9):
        for j in range(9):
            for k in range(j + 1, 9):
                if puzzle[j][i] == puzzle[k][i]:
                    return False

    count = 0
    for i in range(9):
        j = i // 3 # The row of the square
        k = i % 3 # The column of the square
        j = j * 3
        k = k * 3
        for r in range(9):
            for s in range(r + 1, 9):
                a1 = r // 3 # The row of the entry
                b1 = r % 3 # The col of the entry
                a2 = s // 3 # The row of the compared entry
                b2 = s % 3 # The col of the compared entry
                count += 1
                if puzzle[j + a1][k + b1] == puzzle[j + a2][k + b2]:
                    return False
    return True



for i in range(1, 5):
    difficulty = pick_difficulty(i)
    for j in range(1, 9):
        solution_path = 'experiment_inputs/{difficulty}/{difficulty}_output{n}.txt'.format(difficulty = difficulty, n = j)
        solution = read_puzzle(solution_path)
        for k in range(1, 5):
            heuristic_solution_path = "experiment_inputs/{difficulty}/{difficulty}_output{a}-{b}.txt".format(difficulty = difficulty, a = k, b = j)
            heuristic_solution = read_puzzle(heuristic_solution_path)
            is_correct = verify(heuristic_solution)
            if is_correct:
                print("The solution for {difficulty} puzzle {number} is correct for {heuristic}!".format(difficulty = difficulty, number = j, heuristic = get_heuristic_name(k)))
            else:
                print("The solution for {difficulty} puzzle {number} is wrong for {heuristic}!".format(difficulty = difficulty, number = j, heuristic = get_heuristic_name(k)))
        print("----------------------------------------------")
