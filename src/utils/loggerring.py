import logging

stream_handler = logging.StreamHandler()
logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
