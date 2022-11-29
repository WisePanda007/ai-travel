import logging
import urllib.request
import requests


def get_open_ip():
    #自动获取本机ip
    ip=""
    ip_checkers=['https://checkip.amazonaws.com','http://icanhazip.com']
    while ip=="" and len(ip_checkers)>0:
        ip_c=ip_checkers.pop()
        try:
            ip = requests.get(url=ip_c,timeout=2).text.strip()
        except Exception as e:
            ip="未查到ip"
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
