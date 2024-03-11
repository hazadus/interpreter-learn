"""
Basic interpreter of expressions like "X+Y", where X and Y – integers.
"""

from enum import Enum


class ParseError(Exception):
    pass


class Token:
    class Type(str, Enum):
        INTEGER = "INTEGER"
        PLUS = "PLUS"
        EOF = "EOF"

    def __init__(self, type_: Type, value):
        self.type_ = type_
        self.value = value

    def __str__(self):
        return f"Token({self.type_}, {self.value})"


class Interpreter:
    def __init__(self, code: str):
        self.code = code.replace(" ", "")  # code to interpret
        self.pos = 0  # index into self.code
        self.current_token: Token | None = None

    def _error(self):
        raise ParseError(
            f"Error parsing code at symbol {self.pos+1}: '{self.code[self.pos]}'"
        )

    @property
    def _eof(self):
        return self.pos > len(self.code) - 1

    def _get_next_token(self) -> Token:
        """
        Lexical analyzer (aka lexer, scanner or tokenizer).
        Breaks sentence into tokens.
        :return:
        """
        if self._eof:
            return Token(Token.Type.EOF, None)

        current_char = self.code[self.pos]

        # Try to parse integer
        number = ""
        while current_char.isdigit():
            number += current_char
            self.pos += 1
            if self._eof:
                break
            current_char = self.code[self.pos]

        if number:
            return Token(Token.Type.INTEGER, int(number))

        # Try to parse operation
        if current_char == "+":
            self.pos += 1
            return Token(Token.Type.PLUS, current_char)

        self._error()

    def _eat(self, token_type: Token.Type):
        """
        Compare the current token type with the passed token type and if they match then "eat" the current token
        and assign the next token to the self.current_token, otherwise raise an exception.
        """
        if self.current_token.type_ == token_type:
            self.current_token = self._get_next_token()
        else:
            self._error()

    def expr(self) -> int:
        """
        Try to parse and evaluate the only expression we know: "X+Y", where X and Y are integers.
        Expected structure to find: INTEGER -> PLUS -> INTEGER
        :return: result of parsed expression
        """
        # Parse the first token
        self.current_token = self._get_next_token()

        # Expect firtst digit
        left = self.current_token
        self._eat(Token.Type.INTEGER)

        # Expect "+"
        op = self.current_token
        self._eat(Token.Type.PLUS)

        # Expect second digit
        right = self.current_token
        self._eat(Token.Type.INTEGER)
        # NB: After the last call, current_token is set to EOF

        result = left.value + right.value
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
