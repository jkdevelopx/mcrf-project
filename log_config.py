# log_config.py (update)
import logging
from logging.handlers import RotatingFileHandler
import json


class JsonFormatter(logging.Formatter):
def format(self, record):
obj = {
'ts': self.formatTime(record, self.datefmt),
'level': record.levelname,
'message': record.getMessage(),
}
# include extra fields if any
if hasattr(record, 'extra') and isinstance(record.extra, dict):
obj.update(record.extra)
return json.dumps(obj, ensure_ascii=False)




def setup_logging(log_file="logs/mcrf.log"):
logger = logging.getLogger('mcrf')
if logger.handlers:
return logger
logger.setLevel(logging.INFO)
fmt = JsonFormatter()


sh = logging.StreamHandler()
sh.setFormatter(fmt)


fh = RotatingFileHandler(log_file, maxBytes=10_000_000, backupCount=10)
fh.setFormatter(fmt)


logger.addHandler(sh)
logger.addHandler(fh)
return logger