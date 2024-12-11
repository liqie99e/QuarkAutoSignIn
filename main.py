import logging
import os
from typing import Any, Dict, Optional, Tuple
from urllib.parse import urljoin

import requests

from serverchan import sc_send

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger()


class Quark:
    BASE_URL_GROWTH = "https://drive-m.quark.cn/1/clouddrive/capacity/growth/"
    params = {
        "pr": "ucpro",
        "fr": "android",
    }

    def __init__(self, user_data: Dict[str, str]) -> None:
        self.params.update(user_data)

    def convert_bytes(self, b: float) -> str:
        if b == 0:
            return "0 MB"

        units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        idx = 0
        while b >= 1024 and idx < len(units) - 1:
            b /= 1024
            idx += 1
        return f"{b:.2f} {units[idx]}"

    def get_growth_info(self) -> Optional[Dict[str, Any]]:
        url = urljoin(self.BASE_URL_GROWTH, "info")
        try:
            response = requests.get(url=url, params=self.params)
            response.raise_for_status()
            data = response.json()
            return data.get("data")
        except requests.RequestException as e:
            logger.error(f"❌ 签到异常：获取成长信息失败\n {e}")
            sc_send(
                "❌ 夸克网盘签到异常",
                f"获取成长信息失败\n\n {e}",
            )
            return None

    def get_growth_sign(self) -> Tuple[bool, Any]:
        url = urljoin(self.BASE_URL_GROWTH, "sign")
        data = {"sign_cyclic": True}
        try:
            response = requests.post(url=url, json=data, params=self.params)
            response.raise_for_status()
            res_data = response.json()
            if res_data.get("data"):
                return True, res_data["data"]["sign_daily_reward"]
            else:
                return False, res_data.get("message", "未知错误")
        except requests.RequestException as e:
            return False, str(e)

    def do_sign(self) -> None:
        growth_info = self.get_growth_info()

        if not growth_info:
            return

        total_capacity = growth_info.get("total_capacity", 0)
        sign_reward = growth_info.get("cap_composition", {}).get("sign_reward", 0)
        cap_sign = growth_info.get("cap_sign", {})
        sign_daily_reward = cap_sign.get("sign_daily_reward", 0)
        sign_progress = cap_sign.get("sign_progress", 0)
        sign_target = cap_sign.get("sign_target", 7)

        messages = []

        if cap_sign.get("sign_daily"):
            messages.append("🌟 今日已签到")
            messages.append(f"📥 增加容量：{self.convert_bytes(sign_daily_reward):>14}")
        else:
            success, result = self.get_growth_sign()
            if success:
                messages.append("✅ 今日签到成功")
                messages.append(f"📥 增加容量：{self.convert_bytes(result):>14}")
                sign_progress += 1
                sign_reward += result
                total_capacity += result
            else:
                logger.error(f"❌ 签到异常：{result}")
                sc_send(
                    "❌ 夸克网盘签到异常",
                    result,
                )
                return

        messages.append(f"📅 连签进度：{f'({sign_progress}/{sign_target})':>10}")
        messages.append(f"💾 签到累计容量：{self.convert_bytes(sign_reward):>10}")
        messages.append(f"🌐 网盘总容量：{self.convert_bytes(total_capacity):>10}")

        for msg in messages:
            logger.info(msg)

        sc_send(
            f"夸克网盘签到成功 ({sign_progress}/{sign_target})",
            "\n\n".join(messages),
        )


if __name__ == "__main__":
    user_data = {
        "kps": os.environ.get("KPS"),
        "sign": os.environ.get("SIGN"),
        "vcode": os.environ.get("VCODE"),
    }

    if not all(user_data.values()):
        logger.error("环境变量未设置完整，请检查KPS、SIGN、VCODE。")
    else:
        Quark(user_data).do_sign()
