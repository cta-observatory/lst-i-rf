import os
from pathlib import Path

lstmcpipe_root_dir = Path(__file__).absolute().parents[1]
prod_logs = Path(os.getenv('LSTMCPIPE_PROD_LOGS')) if os.getenv('LSTMCPIPE_PROD_LOGS') is not None \
    else Path(os.getenv('HOME')).joinpath('LSTMCPIPE_PROD_LOGS')

__version__ = "0.6.2"
