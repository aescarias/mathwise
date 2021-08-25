# Mathwise

A small math interpreter written in Python.

It can perform most basic calculations you would expect from one

- Standard arithmetic (addition, subtraction, division, multiplication)
- Respects your typical order of operations
- Can perform factorials (yay!)

## :computer: How to Run

1. Clone the repository or download it
2. Run the `shell.py` file using this: `python -m mathwise.shell`. Make sure you're outside the main `mathwise` directory.
3. Follow the instructions showed above

## :gear: Examples

```s
mw > (24 + 3) * 500
mw > .run
13500
mw > 5 * 2 + 10 * 86.45
mw > .run
874.5
mw > 9 * 8.51 - 4!
mw > .run
52.59
```

## :bookmark: Things to fix

- The factorial operator is still fairly buggy and may not work in some cases.
- Inputting nothing will cause an error
- Multiline support is also meh... It could be better.

## :books: Things to add

- Functions (like `sqrt`, `cube`, `log`, etc)
- Variable support

## :technologist: Contribute

If you'd like to contribute to the project, you're free to do so by opening an issue or a pull request on this Github repository.
