import os
import google.generativeai as genai

genai.configure(api_key="")

model = genai.GenerativeModel("gemini-1.5-flash")

PROMPT_TEMPLATE = """
あなたはPythonのプラグインコードを生成するAIです。
ユーザーの要求に対して、EVO用のプラグインとして動作するPythonコードを出力してください。
コードは以下の仕様に従ってください：

- `can_handle(text)` を実装（条件に応じて True/False を返す）
- `handle(text)` を実装（テキストに応じた応答を返す）
- ファイル外の依存は避けてください
- コード部分のみ出力してください。説明やマークダウンは不要です。
- ファイルの先頭に'''python、ファイルの末尾に'''は不要です。
- ファイル名は要求と沿った名前にしてください。

要求: 「{prompt}」
"""

def generate_plugin_code(prompt: str) -> str:
    full_prompt = PROMPT_TEMPLATE.format(prompt=prompt)
    response = model.generate_content(full_prompt)
    if not response.text:
        return ""
    return response.text.strip()
