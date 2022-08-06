from pathlib import Path

import logging
import logging.config


project_root = Path(__file__).absolute().parent.parent
app_root = Path(__file__).absolute().parent
logs_path = Path(project_root/'logs')
if not logs_path.exists():
    logs_path.mkdir()

logging.config.fileConfig(f'{app_root}/logging.conf', disable_existing_loggers=False)


def get_logger(name):
    return logging.getLogger(name)
