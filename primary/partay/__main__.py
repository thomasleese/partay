import sys

from . import Partay


api_key = sys.argv[1]
hue_username = sys.argv[2]
Partay(api_key, hue_username).run()
