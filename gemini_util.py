import os
import google.generativeai as genai

genai.configure(api_key="")

model = genai.GenerativeModel("gemini-2.0-flash")


PROMPT_TEMPLATE = """
あなたはPythonのプラグインコードを生成するAIです。
ユーザーの要求に対して、EVO用のプラグインとして動作するPythonコードを出力してください。
コードは以下の仕様に従ってください：

- `can_handle(text)` を実装（入力された内容に応じて True/False を返す。内容と条件が一致した場合、Trueを返す。）
- `handle(text)` を実装（テキストに応じた応答を返す）
-上記二つの関数を別の関数またはクラスで内包することを禁止する。
-ユーザーが計算機能を実装たい場合、コマンドライン上で変数に値を入力できるようにしてください。
- ファイル外の依存は避けてください。
- 基本的に機能はTkinterでフロントエンドを実装してください。
- また、ゲームならPygame,モダンなUIが必要ならFletで実装するようにしてください。
- subprocess,os等のセキュリティに問題のあるモジュールは禁止です。
- 簡略化などは禁止します。要求に対して沿った機能を必ず実装して下さい。
- ダミーをコード内に含ませることを禁止します。
- コード部分のみ出力してください。説明やマークダウンは不要です。
- コード部分は直接実行できる形にしてください。コードをクォーテーション等で囲って文字列化し、それをそのまま表示するだけなどは禁止します。
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
