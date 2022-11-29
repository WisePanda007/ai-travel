import logging
import urllib.request
import requests


def get_open_ip():
    try:
        ip = requests.get('https://checkip.amazonaws.com').text.strip()
    except Exception as e:
        try:
            ip = requests.get('http://icanhazip.com').text.strip()
        except Exception as e:
            ip = urllib.request.urlopen(
                'https://ident.me').read().decode('utf8').strip()
    return ip


local_ip = get_open_ip()


def get_local_logger():
    logger = logging.getLogger(local_ip)
    console_handler = logging.StreamHandler()
    logger.addHandler(console_handler)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    return logger
