#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Resultant of 2 polynomials

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


    Based on: https://en.wikipedia.org/wiki/Resultant
              https://en.wikipedia.org/wiki/Determinant


    Control: https://numbersandshapes.net/posts/tschirnhausens_transformations_quartic/

"""

import symexpress3

class Sym3Resultant():
  """
  Calculate the resultant of 2 polynomials
  """

  def __init__( self ):
    # defaults
    self._variable  = 'x'  # the variable
    self._formula1  = None # symexpress3 formula
    self._formula2  = None # symexpress3 formula
    self._output    = None # symexpress3.SymToHtml object
    self._resultant = None # resultant, see calcResultant()

  @property
  def formula1(self):
    """
    Symexpress3 formula 1
    """
    return self._formula1

  @formula1.setter
  def formula1(self, val):
    self._formula1 = symexpress3.ConvertToSymexpress3String( val )


  @property
  def formula2(self):
    """
    Symexpress3 formula 2
    """
    return self._formula2

  @formula2.setter
  def formula2(self, val):
    self._formula2 = symexpress3.ConvertToSymexpress3String( val )


  @property
  def resultant(self):
    """
    Symexpress3 resultant from calcResultant()
    """
    return self._resultant


  @property
  def htmlOutput(self):
    """
    Set html output object
    """
    return self._output

  @htmlOutput.setter
  def htmlOutput(self, val):
    if val != None and ( not isinstance( val, symexpress3.SymToHtml )) :
      raise NameError( f'htmlOutput is incorrect: {type(val)}, expected SymToHtml object ' )
    self._output = val


  @property
  def variable(self):
    """
    The variable
    """
    return self._variable

  @variable.setter
  def variable(self, val):
    if not isinstance( val, str ):
      raise NameError( f'Variable is incorrect: {type(val)}, expected str' )
    self._variable = val


  #
  # Resultant calculation
  #
  def calcResultant(self):
    """
    Do the resultant calculation
    """

    def RaiseError( cError ):
      """
      Raise an error and put the message also in the output file if set
      """
      if self._output != None:
        self._output.writeLine( f'Error: {cError}' )
      raise NameError( cError )


    def BuildMatrix( iSize ):
      """
      Build a matrix of given size
      """
      matrix = []
      for _ in range( iSize ):
        row = []
        for _ in range( iSize ):
          row.append( symexpress3.SymNumber( 1,0,1 ) )
        matrix.append( row )
      return matrix


    def PrintMatrix( matrix ):
      """
      Print matrix is output is defined
      """
      if self._output == None:
        return

      matrixSize = len( matrix[0] )
      self._output.write( '<table style="border: 1px solid; border-collapse: collapse">')
      for iRow in range( matrixSize ):
        self._output.write( '<tr>')
        for iCol in range( matrixSize ):
          self._output.write( '<td style="border: 1px solid; border-collapse: collapse; padding: 5px">')
          # self._output.write( str( matrix[ iRow ][ iCol ] ))
          self._output.writeSymExpress( matrix[ iRow ][ iCol ] )
          self._output.write( '</td>')
        self._output.write( '</tr>')

      self._output.write( '</table>')
      self._output.writeLine( '')


    def CalcResulant( matrix ):
      """
      Calculate the resultant of a given matrix (recursive)
      """
      matrixSize = len( matrix[0] )

      if matrixSize == 2:
        # [0,0] * [1.1] - [0,1] * [1,0]
        mult1 = symexpress3.SymExpress( '*')
        mult1.add( matrix[0][0] )
        mult1.add( matrix[1][1] )

        mult2 = symexpress3.SymExpress( '*')
        mult2.add( matrix[0][1] )
        mult2.add( matrix[1][0] )
        mult2.add( symexpress3.SymNumber( -1,1,1 ) )

        plus = symexpress3.SymExpress( '+' )
        plus.add( mult1 )
        plus.add( mult2 )

        valResulant = plus
        valResulant.optimizeNormal()

        # if self._output != None:
        #   PrintMatrix( matrix )
        #   self._output.writeSymExpressWithStr( valResulant, "calcResultant" )
      else:
        # walk row 0
        # create new matrix for each row delete
        matrixSize  = len( matrix[0] )
        valResulant = symexpress3.SymExpress( '+')


        # if self._output != None:
        #   self._output.writeLine( f'Calc matrix size {matrixSize}' )
        #   PrintMatrix( matrix )

        for iCol in range( matrixSize ):
          # skip zero's
          if isinstance( matrix[ 0 ][ iCol ], symexpress3.SymNumber ) and matrix[ 0 ][ iCol ].factCounter == 0 :
            continue

          # odd cols has -1 sign
          if iCol % 2 == 0:
            iSign = 1
          else:
            iSign = -1

          matrixNew = BuildMatrix( matrixSize - 1 )
          # fill matrixNew wihtput rol,col = iCol
          for iRowNew in range( 1, matrixSize ):
            for iColNew in range( matrixSize ):
              iColCalc = iColNew
              iRowCalc = iRowNew - 1

              if iColCalc == iCol:
                continue

              if iColCalc > iCol:
                iColCalc -= 1

              matrixNew[ iRowCalc ][ iColCalc ] = matrix[ iRowNew ][ iColNew ]

          # if self._output != None:
          #   self._output.writeLine( f'Matrix col: {iCol}' )
          #   PrintMatrix( matrixNew )

          valRow     = CalcResulant( matrixNew )
          valRowCalc = symexpress3.SymExpress( '*' )

          if iSign == -1:
            valRowCalc.add( symexpress3.SymNumber( -1,1,1 )) # -1

          valRowCalc.add( matrix[0][iCol] )
          valRowCalc.add( valRow )

          valRowCalc.optimizeNormal()

          # if self._output != None:
          #   self._output.writeSymExpressWithStr( valRowCalc, "Resultant" )

          valResulant.add( valRowCalc )

      # safety check, return 0 is nothing is available
      if valResulant.numElements() == 0:
        valResulant.add( symexpress3.SymNumber( 1,0,1))  # 0

      return valResulant


    if self._output != None:
      self._output.writeLine( 'Resultant calculation' )
      self._output.writeLine( 'Based on <a target="_blank" href="https://en.wikipedia.org/wiki/Resultant">https://en.wikipedia.org/wiki/Resultant</a>' )
      self._output.writeLine( '' )


    # get formula in symexpress3 format
    sym3Formula1 = symexpress3.SymFormulaParser( self._formula1 )
    sym3Formula2 = symexpress3.SymFormulaParser( self._formula2 )

    # only principal root supported, so force it
    sym3Formula1.optimizeNormal()
    sym3Formula1.optimize( 'setOnlyOne')

    sym3Formula2.optimizeNormal()
    sym3Formula2.optimize( 'setOnlyOne')

    if self._output != None:
      self._output.writeSymExpressWithStr( sym3Formula1, "Formula 1" )
      self._output.writeSymExpressWithStr( sym3Formula2, "Formula 2" )
      self._output.writeLine( f'Variable: {self._variable}')
      self._output.writeLine( '' )

    try:
      coef1 = symexpress3.PolynomialCoefficients( sym3Formula1, self._variable )
      coef2 = symexpress3.PolynomialCoefficients( sym3Formula2, self._variable )
    except Exception as err: # pylint: disable=broad-exception-caught
      RaiseError( str( err ) )

    # add missing powers
    maxPower = max( coef1 )
    for iCnt in range( 0, maxPower ):
      if iCnt not in coef1:
        coef1[ iCnt ] = symexpress3.SymNumber( 1, 0, 1 ) # zero

    maxPower = max( coef2 )
    for iCnt in range( 0, maxPower ):
      if iCnt not in coef2:
        coef2[ iCnt ] = symexpress3.SymNumber( 1, 0, 1 ) # zero

    # ChatGPT: How do i in Python reverse sort a dictionary. The key is a integer de value is an object
    coef1 = dict(sorted(coef1.items(), reverse=True))
    coef2 = dict(sorted(coef2.items(), reverse=True))

    if self._output != None:
      self._output.writeLine( 'Coefficient formula 1')
      for key, value in coef1.items():
        self._output.writeLine( f'Power: {key}, Coefficient: {str( value) }')
      self._output.writeLine( '')

      self._output.writeLine( 'Coefficient formula 2')
      for key, value in coef2.items():
        self._output.writeLine( f'Power: {key}, Coefficient: {str( value) }')

      self._output.writeLine( '')

    maxPower1  = max( coef1 )
    maxPower2  = max( coef2 )
    matrixSize = maxPower1 + maxPower2

    if self._output != None:
      self._output.writeLine( f'Max power formula 1: {maxPower1}')
      self._output.writeLine( f'Max power formula 2: {maxPower2}')
      self._output.writeLine( f'Matrix size: {matrixSize}')
      self._output.writeLine( '')

    # build matrix
    matrix = BuildMatrix( matrixSize )

    # fill matrix
    numberCols1 = matrixSize - maxPower1
    numberCols2 = matrixSize - maxPower2

    numRow      = -1
    for key, value in coef1.items():
      numRow += 1
      for iCol in range( numberCols1 ):
        matrix[ numRow + iCol ][ iCol ] = value

    numRow      = -1
    for key, value in coef2.items():
      numRow += 1
      for iCol in range( numberCols2 ):
        matrix[ numRow + iCol ][ iCol + numberCols1 ] = value

    if self._output != None:
      self._output.writeLine( 'Matrix')
      PrintMatrix( matrix )

    # calculate resultant
    resultantValue = CalcResulant( matrix )
    resultantValue.optimizeNormal()

    self._resultant = resultantValue

    if self._output != None:
      self._output.writeSymExpressWithStr( resultantValue, "Resulant" )

    return resultantValue
