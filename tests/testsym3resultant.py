#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Test resultant

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

from datetime import datetime

import sym3resultant
import symexpress3

testData = [ # 1
             { 'formula1'   : 'y^^2+y+1'
             , 'formula2'   : 'y^^2+2y+2'
             , 'variable'   : 'y'
             , 'check'      : '1'
             }
           , # 2
             { 'formula1'   : 'x^4 - 94 x^2 - 480 x - 671'
             , 'formula2'   : 'y - x^2 - r x - s'
             , 'variable'   : 'x'
             , 'check'      : 'y^^4 + y^^3 * s * (-4) + y^^2 * s^^2 * 6 + y * s^^3 * (-4) + s^^4 + r^^2 * (-94) * y^^2 + r^^2 * 188 * y * s + r^^2 * (-94) * s^^2 + r^^4 * (-671) + r^^3 * (-480) * y + r^^3 * 480 * s + r^^2 * y * (-2684) + r^^2 * s * 2684 + r * y^^2 * (-1440) + r * y * s * 2880 + r * s^^2 * (-1440) + y^^3 * (-188) + y^^2 * s * 564 + y * s^^2 * (-564) + y^^2 * 7494 + y * s * (-14988) + s^^3 * 188 + s^^2 * 7494 + 63074 * r^^2 + 45120 * r * y + (-45120) * r * s + (-104252) * y + 104252 * s + 450241 + (-322080) * r'
             }
           ]

startTime = datetime.now()

# test resultant
iTests = 0
iGood  = 0
iBad   = 0

clsResultant = sym3resultant.Sym3Resultant()

for dData in testData :
  iTests += 1
  print( f"Test: {iTests}", end='\r')

  clsResultant.formula1   = dData.get( 'formula1' )
  clsResultant.formula2   = dData.get( 'formula2' )
  clsResultant.variable   = dData.get( 'variable' )

  clsResultant.calcResultant()

  clsCheck = symexpress3.SymFormulaParser( dData.get( 'check' )  )

  clsCheck.optimize()

  if not clsCheck.isEqual( clsResultant.resultant ) :
    iBad += 1

    print( f'Entry {iTests} not equal'  )
    print( f'{clsResultant.resultant}, expected: {clsCheck}' )

  else:
    iGood += 1

endTime   = datetime.now()
timeInSec = ( endTime - startTime ).total_seconds()

print( f"Number of tests: {iTests}, passed: {iGood}, failed; {iBad}, total time: {timeInSec} (sec)" )
