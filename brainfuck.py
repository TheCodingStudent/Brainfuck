from keyboard import is_pressed as key
from time import sleep
from os import system

def error(text, line, column, description):
    lines = text.split('\n')
    error = f'Error at line {line} column {column}.\n'
    error += f'  {lines[line]}\n'
    error += f'  {" "*column}^\n'
    error += description
    return error

def print_memory(memory, head):
    actual = f'{memory}\n'
    actual += f' {" "*head*3}^\n'
    actual += f' {" "*head*3}{head}\n'
    print(actual)

def find_loops(text):
    starts, ends = [], []
    line, column = 0, -1
    for i, letter in enumerate(text):
        if letter == '\n':
            line, column = line + 1, 0
            continue
        if letter == '[': starts.append(i)
        elif letter == ']': ends.append(i)
        column += 1

    if len(starts) != len(ends):
        return None, error(text, line, column, 'Unmatching brackets.')
    
    loops = []
    # print(starts)
    for i in range(len(starts)):
        start = starts.pop(-1)
        ends.sort(key=lambda x: x - start)
        # print(start, ends)
        end = ends.pop(0)
        loops.append((start, end))

    return loops, None

def run(text, debug=False):
    MEMORY = [0]
    HEAD = 0
    RESULT = ''

    index, line, column = 0, 0, 0
    loops, loop_error = find_loops(text)
    # print(loops)
    if loop_error is not None: return None, loop_error

    while index < len(text):
        if text[index] == '\n':
            line, column, index = line + 1, 0, index + 1
            continue

        current = text[index]
        if current in (' ', '\t', '['): pass
        elif current == '=': print_memory(MEMORY, HEAD)
        elif current == '>': 
            HEAD += 1
            if HEAD == len(MEMORY): MEMORY.append(0)
        elif current == '<':
            HEAD -= 1
            if HEAD < 0:
                return None, error(text, line, column, 'Memory out of bounds.')
        elif current == '+': MEMORY[HEAD] += 1
        elif current == '-':
            if MEMORY[HEAD] > 0: MEMORY[HEAD] -= 1
            else: return None, error(text, line, column, f'Invalid negative counter at {HEAD} memory position.') 
        elif current == '.': RESULT += chr(MEMORY[HEAD])
        elif current == ']':
            for start, end in loops:
                if end == index and MEMORY[HEAD] != 0: 
                    # print(f'return to {start} from {end}')
                    index = start
                # else: print(f'exited from {end} because memory is {MEMORY[HEAD]}')
        
        index, column = index + 1, column + 1
        if debug:
            print_memory(MEMORY, HEAD)
            # while not key(' '): pass
            sleep(0.1)
            system('cls')

    return RESULT, None