import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def analyze_stock(info: dict, summary: dict) -> str:
    """
    把股票資料傳給 AI，請它分析並給出建議
    """

    # 把資料整理成 AI 看得懂的文字
    prompt = f"""
你是一位專業的股票分析師，請根據以下資料，用繁體中文給出簡短的分析報告。

【股票基本資訊】
- 股票代號：{info.get('股票代號')}
- 公司名稱：{info.get('公司名稱')}
- 目前股價：{info.get('目前股價')}
- 52週最高：{info.get('52週最高')}
- 52週最低：{info.get('52週最低')}
- 本益比：{info.get('本益比')}

【近期表現】
- 分析期間：{summary.get('分析期間')}
- 起始收盤價：{summary.get('起始收盤價')}
- 最新收盤價：{summary.get('最新收盤價')}
- 期間漲跌幅：{summary.get('期間漲跌幅')}
- 期間最高價：{summary.get('期間最高價')}
- 期間最低價：{summary.get('期間最低價')}
- 平均成交量：{summary.get('平均成交量')}

請用以下格式回答：

📊 整體評估
（2-3句話總結這支股票目前的狀況）

📈 近期走勢分析
（分析期間的表現，漲跌幅的意義）

⚠️ 注意事項
（投資人需要注意的風險或機會）

💡 小結
（一句話總結）

請注意：這只是資料分析，不構成投資建議。
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "你是一位專業的股票分析師，擅長用清楚易懂的繁體中文解釋股票資料。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,   # 創意程度，0=保守，1=有創意
        max_tokens=1024,   # 最長回應字數
    )

    return response.choices[0].message.content
