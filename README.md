# Python module to calculate the resultant of two polynomials

Python module to calculate the resultant of two polynomials

## Usage

### Calculate resultant of two polynomials
The solutions is a symexpress3 object
```py
>>> import sym3resultant
>>> objResultant = sym3resultant.Sym3Resultant()
>>> objResultant.formula1 = "x^^2+x+1"
>>> objResultant.formula2 = "x^^2+2x+2"
>>> objResultant.calcResultant()
>>> print( f"Resultant: {objResultant.resultant}\n" )
Resultant: 1
```

### Options
Options for the resultant
```py
>>> import sym3resultant
>>> objResultant = sym3resultant.Sym3Resultant()
>>> objResultant.formula1 = "y^^2+y+1"
>>> objResultant.formula2 = "y^^2+2y+2"
>>> objResultant.variable = "y"
>>> objResultant.calcResultant()
>>> print( f"Resultant: {objResultant.resultant}\n" )
Resultant: 1
```

### Command line
python -m sym3resultant

- *Help*: python -m sym3resultant -h
- *Resultant*: python -m sym3resultant "x^^2+x+1" "x^^2+2x+2"

### Graphical user interface
https://github.com/SWVandenEnden/websym3
