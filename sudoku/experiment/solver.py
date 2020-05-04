import sys 
import os
import subprocess
import time
from CS3243_P2_Sudoku_10_exp import Sudoku as FirstSudoku
from CS3243_P2_Sudoku_10_AC3_only_exp import Sudoku as SecondSudoku
from CS3243_P2_Sudoku_10_AC3_MCV_exp import Sudoku as ThirdSudoku


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
    return puzzle

def write_solution(puzzle_num, puzzle_solution, heuristic_num, difficulty):
    output_file = "experiment_inputs/{difficulty}/{difficulty}_output{a}-{b}.txt".format(difficulty = difficulty, a = heuristic_num, b = puzzle_num)
    if os.path.isfile(output_file):
        os.remove(output_file)
    f = open(output_file, "w+")

    for i in range(9):
        for j in range(9):
            f.write(str(puzzle_solution[i][j]) + " ")
        f.write("\n")
    
    f.close()

def run_and_generate_stats(puzzle_num, puzzle, heuristic_num, num_of_iterations, difficulty):
    time_taken = []
    preprocessing_time = []
    nodes_explored = []
    for i in range (num_of_iterations):
        sudoku = 0
        if heuristic_num == 1:
            sudoku = FirstSudoku(puzzle)
        elif heuristic_num == 2:
            sudoku = SecondSudoku(puzzle)
        else:
            sudoku = ThirdSudoku(puzzle)
        ans = sudoku.solve()
        write_solution(puzzle_num, ans, heuristic_num, difficulty)
        stats = sudoku.get_statistics()
        time_taken.append(stats['time taken'])
        preprocessing_time.append(stats['pre-process'])
        nodes_explored.append(stats['nodes'])
    return time_taken, preprocessing_time, nodes_explored

def average(list_items):
    return sum(list_items) / len(list_items)

def pick_difficulty(num):
    if num == 1:
        return 'easy'
    elif num == 2:
        return 'medium'
    elif num == 3:
        return 'expert'
    else:
        return 'evil'

for k in range(1, 5):
    difficulty = pick_difficulty(k)

    output_file = "experiment_{difficulty}_output.txt".format(difficulty = difficulty)
    if os.path.isfile(output_file):
        os.remove(output_file)

    f = open(output_file, 'w+')

    for i in range (1, 6):
        puzzle_file_path = 'experiment_inputs/{difficulty}/{difficulty}_input{n}.txt'.format(difficulty = difficulty, n = i)
        num_of_iterations = int(sys.argv[1])
        puzzle = read_puzzle(puzzle_file_path)
        f.write("Input {}:\n".format(i))
        for j in range (1, 4):
            print('Currently running heuristic {j} on {difficulty} puzzle {i}'.format(difficulty = difficulty, j = j, i = i))
            time_taken, preprocessing_time, nodes_explored = run_and_generate_stats(i, puzzle, j, num_of_iterations, difficulty)
            f.write("Heuristic number {}\n".format(j))
            f.write("Average time taken: {}\n".format(average(time_taken)))
            f.write("Average preprocessing time: {}\n".format(average(preprocessing_time)))
            f.write("Average nodes explored: {}\n".format(average(nodes_explored)))
        f.write("\n")
        print("")
    f.close()
