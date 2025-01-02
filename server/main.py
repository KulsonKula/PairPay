import logging
from app import create_app
from flask_compress import Compress

TRACE_LEVEL_NUM = 1


def trace(self, message, *args, **kws):
    if self.isEnabledFor(TRACE_LEVEL_NUM):
        self._log(TRACE_LEVEL_NUM, message, args, **kws)


def trace_enabled(self):
    return self.isEnabledFor(TRACE_LEVEL_NUM)


logging.addLevelName(TRACE_LEVEL_NUM, "TRACE")
logging.Logger.trace = trace
logging.Logger.trace_enabled = trace_enabled

logfile_format = logging.Formatter(
    "%(actime)s - %(name)s - %(levelname)s - %(message)s"
)
console_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")

console_handler = logging.StreamHandler()
console_handler.setFormatter(console_format)

logging.basicConfig(level=TRACE_LEVEL_NUM, handlers=[console_handler])
console_handler.setLevel(logging.INFO)


if __name__ == "__main__":
    app = create_app(config_name="development")
    Compress(app)
    app.run(host="0.0.0.0", port=5000, debug=True)
