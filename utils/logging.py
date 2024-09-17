import logging

from utils.os import get_data_dir


filedir = get_data_dir()

# Configure the logging
logging.basicConfig(filename= filedir + '/app.log', 
                    filemode='a',  # 'a' for append mode, 'w' for overwrite
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    level=logging.INFO)


def log_info(message: str):
    logging.info(message) 

def log_warning(message: str):
    logging.warning(message) 

def log_error(message: str):
    logging.error(message) 
