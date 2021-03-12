import logging.config

import pyyaml

with open('logconf.YAML', 'r') as f:
    config = pyyaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

logger.debug('This is a debug message')
