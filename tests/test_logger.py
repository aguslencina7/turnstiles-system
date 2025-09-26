from loguru import logger

logger.add("test.log", rotation = "1 MB")

logger.debug("This is a DEBUG messge.")
logger.info("This is an INFO message.")
logger.warning("This is a WARNING message.")
logger.error("This is an ERROR message.")