import logging
from logging.handlers import SMTPHandler
from colorlog import ColoredFormatter
from .config import loadConfig

USE_TELEGRAM = False
try:
    import telegram_handler
    USE_TELEGRAM = True
except:
    pass


config = loadConfig()

LOG_LEVEL = logging.DEBUG
LOGFORMAT = ("  %(log_color)s%(levelname)-8s%(reset)s |"
             " %(log_color)s%(message)s%(reset)s")
logging.root.setLevel(LOG_LEVEL)
formatter = ColoredFormatter(LOGFORMAT)
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
log = logging.getLogger(__name__)
log.setLevel(LOG_LEVEL)
log.addHandler(stream)

if "mailto" in config:
    # Mail
    log_handler_mail = SMTPHandler(
        config.get("mailhost", "localhost"),
        config.get("mailfrom", "bookied@localhost"),
        config.get("mailto"),
        config.get("mailsubject", "BookieD notification mail"))
    log_handler_mail.setFormatter(logging.Formatter(
        "Message type:       %(levelname)s\n" +
        "Location:           %(pathname)s:%(lineno)d\n" +
        "Module:             %(module)s\n" +
        "Function:           %(funcName)s\n" +
        "Time:               %(asctime)s\n" +
        "\n" +
        "Message:\n" +
        "\n" +
        "%(message)s\n"
    ))
    log_handler_mail.setLevel(logging.WARNING)
    log.addHandler(log_handler_mail)

if USE_TELEGRAM and "telegram_token" in config and "telegram_chatid" in config:
    tgHandler = telegram_handler.TelegramHandler(
        token=config.get("telegram_token"),
        chat_id=config.get("telegram_chatid")
    )
    tgHandler.setLevel(logging.WARNING)
    log.addHandler(tgHandler)

# logging.basicConfig(level=logging.DEBUG)
