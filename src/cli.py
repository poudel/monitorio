import sys
import time
import logging
import argparse

from src.monitor import create_app


logger = logging.getLogger("monitoria")


def parse_args():
    parser = argparse.ArgumentParser(description="Monitoria: monitor your HTTP service.")
    parser.add_argument("command", type=str, choices=["monitor", "report"])

    parser.add_argument(
        "-l",
        "--loglevel",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Loglevel for verbosity. Default is INFO.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    command = args.command

    logging.basicConfig(level=args.loglevel)

    if args.command not in ["monitor", "report"]:
        logger.error(f"Unknown command: %s", command)
        return 1

    try:
        app = create_app()
    except Exception as err:
        logger.error("Failed to start. Reason: \n%s", err)
        return 1

    logger.info("Starting %s", command)
    exit_code = 0

    while True:
        try:
            if args.command == "report":
                app.report()
                break
            else:
                app.check_and_log()
                time.sleep(app.config.FREQUENCY_SECONDS)
        except KeyboardInterrupt:
            logger.info("Gracefully stopping %s", command)
            break
        except Exception as err:
            logger.exception(err)
            logger.error("Abruptly stopping %s", command)
            exit_code = 1
            break

    logger.info("Finito..")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
