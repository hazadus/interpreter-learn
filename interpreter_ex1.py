"""
Basic interpreter of expressions like "X+Y", "X-Y", "X*Y", "X/Y", where X and Y – integers.
"""

import operator
from enum import Enum


class ParseError(Exception):
    pass


class Token:
    class Type(str, Enum):
        INTEGER = "INTEGER"
        PLUS = "PLUS"
        MINUS = "MINUS"
        MULTIPLY = "MULTIPLY"
        DIVIDE = "DIVIDE"
        EOF = "EOF"

        @staticmethod
        def from_operation(char: str) -> "Token.Type":
            symbol_to_type = {
                "+": Token.Type.PLUS,
                "-": Token.Type.MINUS,
                "*": Token.Type.MULTIPLY,
                "/": Token.Type.DIVIDE,
            }
            return symbol_to_type[char]

    def __init__(self, type_: Type, value):
        self.type_ = type_
        self.value = value

    def __str__(self):
        return f"Token({self.type_}, {self.value})"


class Interpreter:
    def __init__(self, code: str):
        self.code = code  # code to interpret
        self.pos = 0  # index into self.code
        self.current_token: Token | None = None
        self.current_char = self.code[self.pos]

    def _error(self):
        raise ParseError(
            " " * (self.pos + 3) + "^\n"
            f"Error parsing code at symbol {self.pos+1}: '{self.code[self.pos]}'"
        )

    @property
    def _eof(self) -> bool:
        return self.pos > len(self.code) - 1

    def _advance(self) -> None:
        """Advance the `self.pos` pointer and set `self.current_char` property."""
        self.pos += 1
        if self._eof:
            self.current_char = None  # Indicates EOF
        else:
            self.current_char = self.code[self.pos]

    def _skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self._advance()

    def _integer(self) -> int:
        """Return a (multidigit) integer consumed from the code. Advances `pos` through the code."""
        number = ""
        while self.current_char is not None and self.current_char.isdigit():
            number += self.current_char
            self._advance()
        return int(number)

    def _is_operation(self) -> bool:
        """Return true if current char represents an operation, i.e. '+-*/'."""
        return self.current_char in ["+", "-", "*", "/"]

    def _get_next_token(self) -> Token:
        """
        Lexical analyzer (aka lexer, scanner or tokenizer).
        Breaks sentence into tokens.
        :return:
        """
        while self.current_char is not None:
            if self.current_char.isspace():
                self._skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(Token.Type.INTEGER, self._integer())

            # Try to parse operation
            if self._is_operation():
                operation = self.current_char
                self._advance()
                return Token(Token.Type.from_operation(operation), operation)

            self._error()
        return Token(Token.Type.EOF, None)

    def _eat(self, token_type: Token.Type | list[Token.Type]):
        """
        Compare the current token type with the passed token type and if they match then "eat" the current token
        and assign the next token to the self.current_token, otherwise raise an exception.
        """
        if (
            isinstance(token_type, Token.Type)
            and self.current_token.type_ == token_type
        ) or (isinstance(token_type, list) and self.current_token.type_ in token_type):
            self.current_token = self._get_next_token()
        else:
            self._error()

    def expr(self) -> int:
        """
        Try to parse and evaluate expression we know.
        Expected structure to find: INTEGER -> PLUS | MINUS | MULTIPLY | DIVIDE -> INTEGER
        :return: result of parsed expression
        """
        # Parse the first token
        self.current_token = self._get_next_token()

        # Expect firtst digit
        left = self.current_token
        self._eat(Token.Type.INTEGER)

        # Expect "+" | "-" | "*" | "/"
        op = self.current_token
        self._eat(
            [Token.Type.PLUS, Token.Type.MINUS, Token.Type.MULTIPLY, Token.Type.DIVIDE]
        )

        # Expect second digit
        right = self.current_token
        self._eat(Token.Type.INTEGER)
        # NB: After the last call, current_token is set to EOF

        # "Translate" operation token type to Python built-in operation, and get the result
        op_to_operator = {
            Token.Type.PLUS: operator.add,
            Token.Type.MINUS: operator.sub,
            Token.Type.MULTIPLY: operator.mul,
            Token.Type.DIVIDE: operator.truediv,
        }
        operation = op_to_operator[op.type_]
        result = operation(left.value, right.value)
        return result


if __name__ == "__main__":
    while True:
        try:
            if not (expression := input(">> ")):
                continue
            print(Interpreter(expression).expr())
        except ParseError as ex:
            print(ex)
        except KeyboardInterrupt:
            print("\nProgram interrupted by user.")
            break
