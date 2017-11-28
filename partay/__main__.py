import sys

from .partay import Partay


api_key = sys.argv[1]
hue_username = sys.argv[2]
replica_addresses = sys.argv[3:]
Partay(api_key, hue_username, replica_addresses).run()
