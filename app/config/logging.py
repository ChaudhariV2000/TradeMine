from loguru import logger
from app.config.settings import settings

logger.remove()

logger.add(
    settings.LOG_DIR / "trademind.log",
    rotation="10 MB",
    retention="30 days",
    level="INFO",
)

logger.add(
    lambda msg: print(msg, end=""),
    level="INFO",
)