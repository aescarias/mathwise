class Error:
    def __init__(self, filepath: str, proc: str, name: str, details: str, 
                       line: str, pos_start: tuple, pos_end: tuple = None):
        self.filepath = filepath
        self.proc = proc
        self.name = name
        self.details = details
        self.line = line
        self.line_start, self.col_start = pos_start
        self.line_end, self.col_end = pos_end or pos_start

    def to_string(self):
        return \
            f"{self.proc} error in '{self.filepath}' @ line {self.line_start}-{self.line_end} column {self.col_start}-{self.col_end}:\n" \
            f"\t{self.line}\n" \
            f"\t{' '*(self.col_start-1)}{('^'*(self.col_end+1 - self.col_start))}\n" \
            f"{self.name}: {self.details}\n"


class Token:
    def __init__(self, name, value, pos_start, pos_end=None):
        self.name = name
        self.value = value
        self.pos_start = pos_start
        self.pos_end = pos_end or pos_start

    def __repr__(self):
        return f"<TokenType.{self.name}{(f':{self.value}')*bool(self.value)}>"


class Lexer:
    ignore = [' ', '\t', '\r']
    nextline = '\n'
    digits = '0123456789'
    float_point = '.'
    toks = {
        '+': 'Plus',
        '-': 'Minus',
        '*': 'Mul',
        '/': 'Div',
        '!': 'Factorial',
        '(': 'LParen',
        ')': 'RParen'
    }

    def __init__(self, data: str):
        self.data = data
        
        self.current_index = -1
        self.current_char = None

        self.line_num = 1
        self.line_col = 0
        
        self.advance()

    def __construct_error(self, name, details, pos_start, pos_end=None):
        line = self.data.splitlines()[self.line_num - 1]
        return Error("REPL", 'lex', name, details, line, pos_start, pos_end)

    def advance(self):
        self.current_index += 1

        nextline = False
        if self.current_char and self.current_char in Lexer.nextline:
            self.line_num += 1
            self.line_col = 0
            nextline = True

        if self.current_index >= len(self.data):
            self.current_char = None
            return

        self.current_char = self.data[self.current_index]
        self.line_col += 1

        if nextline:
            return Token('EOL', None, (self.line_num - 1, self.line_col))


    def lex(self):
        tokens = []
        while self.current_char:
            if self.current_char in Lexer.ignore + [Lexer.nextline]:
                token = self.advance()
                tokens.append(token) if token else None
                continue

            if self.current_char in Lexer.toks:
                tokens.append(Token(
                    Lexer.toks[self.current_char], None, 
                    (self.line_num, self.line_col)
                ))
            elif self.current_char in Lexer.digits + Lexer.float_point:
                token, error = self.lex_digits()
                if error:
                    return None, error
                tokens.append(token)
                continue
            else:
                return None, self.__construct_error(
                    "SyntaxError", f"Unknown value {ascii(self.current_char)}", 
                    (self.line_num, self.line_col)
                )
            self.advance()
        tokens.append(Token('EOF', None, (self.line_num, self.line_col)))
        
        return tokens, None

    def lex_digits(self):
        pos_start = (self.line_num, self.line_col)
        dot_count = 0
        has_digits = False
        digit_str = ''

        while self.current_char and self.current_char in Lexer.digits + Lexer.float_point:
            if self.current_char == Lexer.float_point:
                dot_count += 1
            
            if self.current_char in Lexer.digits:
                has_digits = True
            
            digit_str += self.current_char

            self.advance()

        if dot_count:
            if not has_digits:
                return None, self.__construct_error(
                    "SyntaxError", f"Expected numeric value after or before floating point.",
                    pos_start, (self.line_num, self.line_col)
                )
            if dot_count > 1:
                return None, self.__construct_error(
                    "SyntaxError", 
                    f"Expected single floating point in numeric sequence. Received {dot_count}\n" \
                    f"TIP: If you are trying to store a version number like '1.0.4', consider a string instead.",
                    pos_start, (self.line_num, self.line_col)
                )
            else:
                return Token("Float", float(digit_str), pos_start, (self.line_num, self.line_col)), None
        else:
            return Token("Int", int(digit_str), pos_start, (self.line_num, self.line_col)), None