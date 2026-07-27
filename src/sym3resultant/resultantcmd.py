#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Command line interface

    Copyright (C) 2026 Gien van den Enden - swvandenenden@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import symexpress3
import sym3resultant

from sym3resultant import version


def CalcSolution( formula1:str, formula2:str, variable:None|str, outputFormat:None|str ) -> None:
  """
  Calculate the resultant of two polynomials
  """
  if len( formula1 ) == 0:
    print( "No parameters are given, nothing to do" )
    return

  if len( formula2 ) == 0:
    print( "Formula two is not given" )
    return

  # default output format, solutions as string and calculated values
  if outputFormat in( "", None ):
    outputFormat = "s"

  try:

    clsResultant = sym3resultant.Sym3Resultant()
    output   = None

    # set variables
    # pylint: disable=multiple-statements
    if formula1 != None: clsResultant.formula1  = formula1
    if formula2 != None: clsResultant.formula2  = formula2
    if variable != None: clsResultant.variable  = variable

    if 'h' in outputFormat:
      output = symexpress3.SymToHtml( None, "Resultant of two polynomials" )
      clsResultant.htmlOutput = output

    # calculate the solutions
    clsResultant.calcResultant()

    # output data
    for cOutput in outputFormat:
      if cOutput == "s":
        # print( f"Resultant: {clsResultant.resultant}" )
        print( str( clsResultant.resultant ) )

      elif cOutput == "h":
        pass # do nothing html (output) is already set

      else:
        print( f"Unknown output format '{cOutput}' ignored" )

    if output != None:
      output.closeFile()
      output = None

  except Exception as exceptAll: # pylint: disable=broad-exception-caught
    print( f"Error: {str( exceptAll )}" )



def DisplayVersion() -> None :
  """
  Display version information
  """
  print( "Version    : " + version.__version__    )

  print( "Author     : " + version.__author__     )
  print( "Copyright  : " + version.__copyright__  )
  print( "License    : " + version.__license__    )
  print( "Maintainer : " + version.__maintainer__ )
  print( "Email      : " + version.__email__      )
  print( "Status     : " + version.__status__     )


def DisplayHelp() -> None :
  """
  Display help
  """
  print( "Calculate the resultant of two polynomials" )
  print( " " )
  print( "usage: python -m sym3resultant [options] [arg]" )
  print( "options: " )
  print( "  -h           : Help" )
  print( "  -v           : Version information" )
  print( "  -o <format>  : Output format" )
  print( "                 s - string format (default)" )
  print( "                 h - html" )
  print( "  -d <name>    : Variable in polynomial, default is 'x'" )
  print( "arg: <symexpress3 string> <symexpress3 string>" )
  print( " " )
  print( "Example: " )
  print( 'python -m sym3resultant "x^^2+x+1" "x^^2+2x+2"' )
  print( 'python -m sym3resultant -o s -d x  "x^^2+x+1" "x^^2+2x+2"' )

def CommandLine( argv:list[str] ) -> None :
  """
  Process the command line parameters
  """
  outputFormat = ""
  formula1     = ""
  formula2     = ""
  variable     = None  # variable in polynomial

  nrarg = len( argv )

  # nothing given, then display help
  if nrarg <= 1:
    DisplayHelp()

  mode = ""
  for iCnt in range( 1, nrarg ) :
    cArg = argv[ iCnt ]

    if mode == "output":
      outputFormat = cArg
      mode = ""
      continue

    if mode == "variable":
      variable = cArg
      mode = ""
      continue

    if cArg == "-h" :
      DisplayHelp()
      return  # direct stop by help

    if cArg == "-v" :
      DisplayVersion()
      return  # direct stop by version information

    # pylint: disable=multiple-statements
    if   cArg == "-o": mode = "output"
    elif cArg == "-d": mode = "variable"

    else:
      if cArg.startswith( "-" ):
        print( f"Unknown option: {cArg}, use -h for help")
      else:
        # collect arguments
        if len( formula1 ) == 0:
          formula1 = cArg
        elif len( formula2 ) == 0:
          formula2 = cArg
        else:
          print( f"More then 2 polynomials given: {cArg}")
          return  # direct stop


  CalcSolution( formula1, formula2, variable, outputFormat )


# ---------------------------
# The end
# ---------------------------
