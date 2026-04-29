# ai_analyzer.py

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def analyze_stock(info: dict, summary: dict) -> str:
    """
    把股票資料傳給 AI，請它分析並給出建議
    """

    prompt = f"""
以下是一支股票的近期資料：

公司：{info.get('公司名稱')}（{info.get('股票代號')}）
目前股價：{info.get('目前股價')}
52週區間：{info.get('52週最低')} ~ {info.get('52週最高')}
本益比：{info.get('本益比')}
分析期間：{summary.get('分析期間')}
期間漲跌：{summary.get('起始收盤價')} → {summary.get('最新收盤價')}（{summary.get('期間漲跌幅')}）
期間高低：{summary.get('期間最高價')} / {summary.get('期間最低價')}
平均成交量：{summary.get('平均成交量')}

請給出你的分析，用自然的口吻說明：
- 這支股票目前處於什麼狀況
- 這段期間的走勢說明了什麼
- 有什麼值得注意的地方
- 你的整體看法

風格要像一個朋友在幫你看股票，直接、有觀點、不廢話。
最後加一行免責聲明即可。
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "你是一個有點毒舌但很準的股票老手，"
                    "用繁體中文說話，講重點不廢話，"
                    "敢說漲也敢說跌，不給模糊答案。"
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.85,
        max_tokens=1024,
    )

    return response.choices[0].message.content
