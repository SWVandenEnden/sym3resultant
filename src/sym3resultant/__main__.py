# pylint: disable=invalid-name
"""
Command line handling
"""

import sys

if __name__ == '__main__':
  from sym3resultant import resultantcmd
  resultantcmd.CommandLine( sys.argv )
