from datetime import datetime
import logging
import os

class Logger:
    def start_logging() -> None:
        logging.basicConfig(
            filename=(
                f"{os.path.dirname(os.path.realpath(__file__))}" \
                f"/Logs/" \
                f"{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.log"
            ),
            level=logging.INFO
        )