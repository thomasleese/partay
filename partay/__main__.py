import sys

from .config import Config
from .partay import Partay



config = Config('config.yaml')

Partay(config.genius_api_key, config.hue_username, []).run()
