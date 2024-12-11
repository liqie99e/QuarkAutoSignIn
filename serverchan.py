import logging
import os
import re
from typing import Any, Dict, Optional

import requests

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger()


def sc_send(title: str, desp: str = "", options: Optional[Dict[str, Any]] = None) -> None:
    if options is None:
        options = {}

    sendkey = os.environ.get("SENDKEY")

    try:
        if sendkey.startswith("sctp"):
            match = re.match(r"sctp(\d+)t", sendkey)
            if match:
                num = match.group(1)
                url = f"https://{num}.push.ft07.com/send/{sendkey}.send"
            else:
                raise ValueError("sctp 的发送密钥格式无效")
        else:
            url = f"https://sctapi.ftqq.com/{sendkey}.send"
        params = {"title": title, "desp": desp, **options}
        headers = {"Content-Type": "application/json;charset=utf-8"}
        response = requests.post(url, json=params, headers=headers)
        response.raise_for_status()
        logger.info("Server 酱推送成功")
    except requests.HTTPError as http_err:
        logger.error(f"HTTP错误发生: {http_err}")
        raise
    except requests.RequestException as req_err:
        logger.error(f"请求错误发生: {req_err}")
        raise
    except ValueError as val_err:
        logger.error(f"值错误: {val_err}")
        raise
    except Exception as ex:
        logger.error(f"未知错误: {ex}")
        raise
