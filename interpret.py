from . import lexer
import math

interpreter_data = ''

class Number:
    def __init__(self, value):
        self.value = value
        self.error = None
        self.set_position()
    
    def set_position(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def __add__(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value)
    
    def __sub__(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value)

    def __truediv__(self, other):
        if isinstance(other, Number):
            if other.value != 0:
                return Number(self.value / other.value)
            else:
                num = Number(0)
                num.error = lexer.Error("REPL", "interpret", "MathError", "Cannot perform division by 0.", interpreter_data.splitlines()[self.pos_start[0] - 1], other.pos_start, other.pos_end)
                return num
                

    def __mul__(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value)
    
    def __repr__(self):
        return str(self.value)

    def __neg__(self):
        return Number(self.value * -1)
    

class Interpreter:
    def __init__(self, data):
        self.error = None
        global interpreter_data
        interpreter_data = data
    
    def goto(self, node):
        method_name = f"goto_{type(node).__name__}"
        method = getattr(self, method_name, self.goto_not_found)
        return method(node)

    def goto_not_found(self, node):
        print("INTERNAL PANIC")

        print("This is an internal error caused by the interpreter and shall not occur.")
        print(f"Error: Method for node type {node} not found: {type(node)}")
        print("If you encounter this error, please contact us on the Github repository for further guidance.")
        print("Exiting")
        exit()
    
    def goto_NumberNode(self, node):
        return Number(node.number.value).set_position(node.pos_start, node.pos_end)

    def goto_BinOpNode(self, node):
        left = self.goto(node.left_token)
        right = self.goto(node.right_token)

        if node.operator.name == "Plus":
            return (left + right).set_position(node.pos_start, node.pos_end)
        elif node.operator.name == "Minus":
            return (left - right).set_position(node.pos_start, node.pos_end)
        elif node.operator.name == "Mul":
            return (left * right).set_position(node.pos_start, node.pos_end)
        elif node.operator.name == "Div":
            res = (left / right).set_position(node.pos_start, node.pos_end)

            if res.error:
                self.error = res.error
                return Number(0)
            else:
                return res

    def goto_UnaryOpNode(self, node):
        num = self.goto(node.token)

        if isinstance(node.operator, list) and all(op.name == "Factorial" for op in node.operator):
            try:
                val = math.factorial(num.value)
                for op in node.operator[2:]:
                    val = math.factorial(val)
                return Number(val).set_position(node.pos_start, node.pos_end)
            except OverflowError:
                self.error = lexer.Error("REPL", "interpret", "MathError", "Cannot process factorial calculations that exceed the 32-bit signed limit.", interpreter_data.splitlines()[node.operator[0].pos_start[0] - 1], node.token.pos_end, node.operator[-1].pos_end)
                return Number(0)
        else:
            if node.operator.name == "Plus":
                return (num).set_position(node.pos_start, node.pos_end)
            elif node.operator.name == "Minus":
                return (-num).set_position(node.pos_start, node.pos_end) 
        