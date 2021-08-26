from . import lexer, parser, interpret
import os
print("Welcome to Mathwise. (type '.exit' to exit and '.run' to run the queued lines, '.clear' to clear the console, type '.help' for more info)")

data = ""

while True:
    inp = input("mw > ")
    if inp.lower().strip() == ".exit":
        break
    elif inp.lower().strip() == ".about":
        print("Mathwise - A math interpreter in Python")
        print("Version v0.1.0 developed by Angel Carias. 2021.")
    elif inp.lower().strip() == ".help":
        print("Mathwise REPL\n"
              "\t.exit - Exit the REPL interface\n"
              "\t.about - About this interpreter\n"
              "\t.run - Runs the currently queued lines\n"
              "\t.help - Runs this thing\n"
              "\t.clear - clears the console\n"
              )
    elif inp.lower().strip() == ".clear":
        os.system('cls' if os.name == 'nt' else 'clear')
    elif inp.lower().strip() == ".run":
        data = data.strip("\n")

        lex = lexer.Lexer(data)

        tokens, error = lex.lex()

        if error:
            print(error.to_string())
            data = ""
            continue

        ast = parser.Parser(data, tokens)
        ast_data = ast.parse()
        if ast.error:
            print(ast.error.to_string())
            data = ""
            continue

        inter = interpret.Interpreter(data)
        result = inter.goto(ast_data)
        if inter.error:
            print(inter.error.to_string())
        else:
            print(result)

        data = ""
    else:
        # if inp == None:
        #     continue
        data += inp + "\n"
