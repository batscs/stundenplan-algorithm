from src.python.log.logger import logger_app
from src.python.io import reader_json as parser
from src.python.app import config, core


def main() -> None:
    logger_app.debug("Starting Application")
    app_config = parser.parse(config.get_application_path_config())
    config.set_config(app_config)

    core.run()

    exit(0)


if __name__ == "__main__":
    main()
