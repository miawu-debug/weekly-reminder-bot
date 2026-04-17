import os
from datetime import date

import requests
from dotenv import load_dotenv

from sheets_service import read_all_rows

load_dotenv()

SHEET_URL = "https://docs.google.com/spreadsheets/d/1AKsL0ixkU4rXMsmCMdd2FJjew9y9IHNlFySye4IrJNg/edit?gid=631295127#gid=631295127"

MEMBERS = {
    "吳奕蓁", "李孟儒", "林雨潔", "楊雅竹", "陳巧玲",
    "陳敏慈", "簡潔安", "李育維", "鄭如觀", "黃珮綺",
}

EXCLUDE_FROM_REMINDER = {"黃佩綺"}


def get_not_filled() -> list[str]:
    rows = read_all_rows()
    result = []
    for row in rows:
        name = row[1] if len(row) > 1 else ""
        status = row[3] if len(row) > 3 else ""
        if name in MEMBERS and status == "尚未填寫":
            result.append(name)
    return result


def build_message(today: str, not_filled: list[str]) -> str:
    header = f"每週TOP重要事件回報表已於 {today} 更新"
    if not_filled:
        names = "\n".join(not_filled)
        return (
            f"{header}\n"
            f"⚠️ 未填寫同仁請儘速完成（若遇休假請忽略）\n"
            f"\n未完成名單：\n{names}\n"
            f"\n{SHEET_URL}"
        )
    else:
        return (
            f"{header}\n"
            f"✅ 本週所有同仁皆已完成填寫，謝謝。\n"
            f"\n{SHEET_URL}"
        )


def send_webhook(message: str):
    webhook_url = os.getenv("CHAT_WEBHOOK_URL")
    if not webhook_url:
        raise ValueError("CHAT_WEBHOOK_URL 未設定，請確認 .env 檔案。")
    response = requests.post(webhook_url, json={"text": message})
    response.raise_for_status()


def main():
    today = date.today().strftime("%Y/%m/%d")
    not_filled = get_not_filled()
    not_filled = [name for name in not_filled if name not in EXCLUDE_FROM_REMINDER]

    print(f"today:      {today}")
    print(f"未填寫名單: {not_filled if not_filled else '（無）'}")

    message = build_message(today, not_filled)
    print(f"\nmessage:\n{message}\n")

    send_webhook(message)
    print("已發送至 Google Chat Webhook。")


if __name__ == "__main__":
    main()
