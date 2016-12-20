import sys

from . import Partay


api_key = sys.argv[1]
Partay(api_key).run()
