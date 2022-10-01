def find_loops(text):
    starts, ends, line, column = [], [], 0, -1
    for i, letter in enumerate(text):
        if letter == '\n': line, column = line + 1, 0   
        else:
            if letter == '[': starts.append(i)
            elif letter == ']': ends.append(i)
            column += 1
    if len(starts) != len(ends): return None
    return [(starts[i], ends[-i-1]) for i in range(len(starts))]

def run(text):
    MEMORY, HEAD, RESULT = [0], 0, ''
    index, line, column = 0, 0, 0
    if not (loops := find_loops(text)): return None
    while index < len(text):
        if text[index] == '\n': line, column, index = line + 1, 0, index + 1
        else:
            current = text[index]
            if current in (' ', '\t', '['): pass
            elif current == '>': 
                HEAD += 1
                if HEAD == len(MEMORY): MEMORY.append(0)
            elif current == '<':
                HEAD -= 1
                if HEAD < 0: return None
            elif current == '+': MEMORY[HEAD] = (MEMORY[HEAD]+1) % 256
            elif current == '-': MEMORY[HEAD] = (MEMORY[HEAD]-1) % 256
            elif current == '.': RESULT += chr(MEMORY[HEAD])
            elif current == ']':
                for start, end in loops:
                    if end == index and MEMORY[HEAD] != 0: index = start  
            index, column = index + 1, column + 1
    return RESULT