import logging
import urllib.request
import socket
from datetime import datetime
from collections import defaultdict

import asciichartpy as asciichart

from src.config import Config
from src.storage import Storage

logger = logging.getLogger("monitoria")


class App:
    def __init__(self, config: Config):
        self.config = config
        self.storage = Storage(config)
        self.health_code_map = {
            1: "success",
            0: "failure",
            -1: "unresponsive",
            -2: "unreachable",
            -3: "unknown errs",
        }

    def check(self):
        try:
            code = urllib.request.urlopen(
                self.config.SERVICE_URL, timeout=self.config.REQUEST_TIMEOUT_SECONDS
            ).getcode()
        except urllib.error.HTTPError as err:
            code = err.code
        except socket.timeout:
            code = -1
        except urllib.error.URLError:
            code = -2
        except Exception:
            code = -3

        now = datetime.utcnow()
        unix_ts = int(now.timestamp())
        self.storage.set(unix_ts, code)
        return now, code

    def check_and_log(self):
        dt, code = self.check()
        is_healthy = code == self.config.HEALTHY_STATUS

        status_display = "success" if is_healthy else "failure"
        message = (
            f"{dt.isoformat()} service {self.config.SERVICE_URL} "
            f"status: {status_display}, code: {code}"
        )

        log_func = logger.info if is_healthy else logger.error
        log_func(message)

    def report(self):
        """
        Displays maximum last {Config.REPORT_WAY_BACK_MINUTES} minutes
        of statistics grouped by minute.
        """
        logger.info(f"Success/failure stats by minute for: {self.config.SERVICE_URL}\n")

        stats_by_dt = defaultdict(lambda: defaultdict(int))

        for idx, item in enumerate(self.storage.items()):
            ts, code = item
            dt = datetime.fromtimestamp(ts)
            key = dt.replace(second=0, microsecond=0)

            stats_by_dt[key][code] += 1

            if len(stats_by_dt.keys()) == (self.config.REPORT_WAY_BACK_MINUTES - 1):
                break

        for key, stats in sorted(stats_by_dt.items(), key=lambda i: i[0], reverse=True):
            messages = [f"{key.isoformat()} "]

            for code, code_display in self.health_code_map.items():
                messages.append(f"{code_display}: {stats.get(code, 0)}")

            logger.info(", ".join(messages))


def create_app():
    config = Config.from_environment()
    app = App(config)
    return app
