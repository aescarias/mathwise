from . import lexer

class BinOpNode:
    def __init__(self, left_token, operator, right_token):
        self.left_token = left_token
        self.operator = operator
        self.right_token = right_token

        self.pos_start = left_token.pos_start
        self.pos_end = right_token.pos_end

    def __repr__(self):
        return f"({self.left_token}, {self.operator}, {self.right_token})"

class UnaryOpNode:
    def __init__(self, operator, token):
        self.operator = operator
        self.token = token

        if isinstance(operator, list):
            self.pos_start = operator[0].pos_start
        else:
            self.pos_start = operator.pos_start
        self.pos_end = token.pos_end
    
    def __repr__(self):
        return f"{self.operator}{self.token}"
    
class NumberNode:
    def __init__(self, number):
        self.number = number

        self.pos_start = number.pos_start
        self.pos_end = number.pos_end

    def __repr__(self):
        return f"{self.number}"

class Parser:
    def __init__(self, data, tokens):
        self.data = data
        self.tokens = tokens

        self.current_index = -1
        self.current_token = self.tokens[self.current_index]
        self.error = None
        self.advance()

    def advance(self):
        self.current_index += 1
        
        if self.current_index >= len(self.tokens):
            return
        self.current_token = self.tokens[self.current_index]

    def factor(self):        
        tok = self.current_token

        if tok.name in ["Plus", "Minus"]:
            self.advance()            
            factor = self.factor()
            return UnaryOpNode(tok, factor)
        elif tok.name == "LParen":
            pos_start = self.current_token.pos_start
            self.advance()
            expr = self.expr()

            if self.current_token.name == "RParen":
                self.advance()
                return expr
            else:
                self.error = lexer.Error('REPL', 'parse', 'SyntaxError', f'Did not find closing )', self.data.splitlines()[pos_start[0] - 1], pos_start, self.current_token.pos_end)
                return
        elif tok.name in ["Int", "Float"]:
            self.advance()
            if self.current_token.name == "Factorial":
                op = self.current_token
                unary = UnaryOpNode([op], NumberNode(tok))
                while self.current_token.name == "Factorial":
                    unary.operator.append(op)
                    self.advance()
                self.advance()
                return unary
            elif self.current_token.name == "LParen":
                expr = self.expr()
                return BinOpNode(NumberNode(tok), lexer.Token("Mul", None, self.current_token.pos_start, self.current_token.pos_end), expr)
            return NumberNode(tok)


        self.error = lexer.Error('REPL', 'parse', 'SyntaxError', f'Expected integer or float, received {tok}', self.data.splitlines()[tok.pos_start[0] - 1], tok.pos_start, tok.pos_end)

    def term(self):
        left = self.factor()

        while self.current_token.name in ["Mul", "Div"]:
            operator = self.current_token
            self.advance()
            right = self.factor()
            if self.error: return
            left = BinOpNode(left, operator, right)
        return left

    def expr(self):
        left = self.term()

        while self.current_token.name in ["Plus", "Minus"]:
            operator = self.current_token
            self.advance()
            right = self.term()
            if self.error: return
            left = BinOpNode(left, operator, right)
        return left

    def parse(self):
        res = self.expr()
        if not self.error and self.current_token.name != "EOF":
            self.error = lexer.Error('REPL', 'parse', 'SyntaxError', f"Expected either of the following operators: '+', '-', '*', '/', '!'; received {self.current_token} ", self.data.splitlines()[self.current_token.pos_start[0] - 1], self.current_token.pos_start, self.current_token.pos_end)
        return res