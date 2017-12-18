import sys

from .config import Config
from .partay import Partay



config = Config('config.yaml')

replica_addresses = sys.argv[1:]

Partay(config.genius_api_key, config.hue_username, config.hue_group, replica_addresses).run()
