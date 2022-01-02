# Python

```python
class myLogger:

    def __init__(self, debug_enabled=False):
        self.logger = logging.getLogger('mylogger')

        log_level = 10 if debug_enabled else 0
        log_format = logging.Formatter('[%(asctime)s] [%(levelname)8s] %(message)s', '%H:%M:%S')

        self.logger.setLevel(log_level)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_format)
        console_handler.setLevel(log_level)
        self.logger.addHandler(console_handler)

    def log(self, lvl, msg):
        level = logging.getLevelName(lvl.upper())
        self.logger.log(level, msg)
```