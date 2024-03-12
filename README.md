# interpreter-learn

Изучаю работу и разработку интерпретаторов на практике.

## Terms

**Token** is an object that has a type and a value. For example, for the string “3” the type of the token will be 
INTEGER and the corresponding value will be integer 3.

**Lexeme** is a sequence of characters that form a token.

The process of breaking the input string into tokens is called **lexical analysis**.

The part of the interpreter that reads the input of characters and converts it into a stream of tokens is called a 
**lexical analyzer**, or lexer for short (aka scanner or tokenizer).

The process of finding the structure in the stream of tokens, or put differently, the process of recognizing a phrase in the stream of tokens is called **parsing**. The part of an interpreter or compiler that performs that job is called a **parser**.

## References
- Web
  - https://ruslanspivak.com/lsbasi-part1/
  - https://ruslanspivak.com/lsbasi-part2/
- Books
  - [Language Implementation Patterns](http://library.hazadus.ru/books/89/details/) · Terence Parr · «The Pragmatic Bookshelf» · 2009 г.