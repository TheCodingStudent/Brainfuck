from brainfuck import run

# while True:
#     command = input('>>> ')
#     result, error = run(command)
#     if error is not None: print(error)
#     elif result: print(result)

#CHAPARRO = 67 72 65 80 65 82 82 79

code = """
++[>+++[>++++<-]<-]=
"""

result, error = run(code, debug=True)
if error is not None: print(error)
elif result != '': print(result)