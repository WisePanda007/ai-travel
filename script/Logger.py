import logging
local_ip="101.42.97.82"
def get_local_logger():
    logger = logging.getLogger(local_ip) 
    console_handler = logging.StreamHandler()
    logger.addHandler(console_handler)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    return logger
