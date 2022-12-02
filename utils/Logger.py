import logging
import subprocess

def get_eth0_ip():
    # 自动获取本机ip
    ip = ""
    try:
        ipinfo = subprocess.getstatusoutput("ifconfig")
        ip = ipinfo[1].split("\n")[1].split("inet")[1].split("netmask")[0].strip()
    except Exception as e:
        ip = "ip not find"
    return ip

def get_local_logger():
    logger = logging.getLogger(get_eth0_ip())
    console_handler = logging.StreamHandler()
    logger.addHandler(console_handler)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    return logger
    
logger=get_local_logger()