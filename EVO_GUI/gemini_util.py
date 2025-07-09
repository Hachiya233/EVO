import os
from google import genai

client = genai.Client()

PROMPT_TEMPLATE = """
あなたは、Pythonの標準ライブラリであるTkinterをベースにしたプラグインを生成するAIです。
ユーザーの要求に応じて、EVO用のプラグインとして動作するPythonコードを出力してください。

### 基本仕様
- `import tkinter as tk` と `from tkinter import ttk` を必ず含めてください。
- `can_handle(text)`: ユーザーの入力テキストに基づき、このプラグインが処理すべきかどうかをTrue/Falseで返します。
- `handle(text, root, result_callback)`: プラグインの本体です。以下の2つのモードのいずれかで動作します。

### 動作モード
1.  **テキスト応答モード**:
    - 簡単な応答で済む場合、処理結果の文字列を `return` してください。
    - 例: `return "こんにちは！"`

2.  **GUI生成モード**:
    - 電卓やフォームなど、専用のUIが必要な場合、**`tkinter.Toplevel`** ウィンドウを生成してください。この場合、`handle`関数は何も`return`しません。
    - このモードでは、`handle`関数の引数が重要になります。
        - `root`: メインアプリケーションのTkinterルートウィンドウです。`Toplevel`を生成する際の親として `tk.Toplevel(root)` のように指定します。
        - `result_callback`: プラグインの処理が完了した際に、最終結果をメイン画面に通知するための関数です。`result_callback("計算結果は 42 です")` のように、結果の文字列を引数として呼び出します。
    - `Toplevel`ウィンドウ内に、`tk.Label`, `tk.Entry`, `tk.Button` などのウィジェットを配置してUIを構築します。
    - 中核となるボタン（例：計算実行ボタン）の `command` には、以下の処理を行う関数を紐付けてください。
        1. 必要な計算や処理を実行する。
        2. `result_callback`を呼び出して、最終結果をメインウィンドウに送信する。
        3. `Toplevel`ウィンドウ自身を閉じる (`toplevel_window.destroy()`)。
    - 以下は実装する機能のコードの設計例です。以下にならって必ず生成して下さい。
        # 必ず以下の構造に従って下さい：

        import tkinter as tk
        from tkinter import ttk

        def can_handle(text):
            return "〇〇" in text

        def handle(text, root, result_callback):
            window = tk.Toplevel(root)
            window.title("〇〇機能")

            # 必要なUI構築
            ...

            def on_submit():
                result = "処理結果"
                result_callback(result)
                window.destroy()

            tk.Button(window, text="実行", command=on_submit).pack()
    - can_handle()では実行した際に他の機能と被らない、ユニークなキーワードで実行されるようにして下さい。

    - また、例外として物理演算機能などのアニメーションが必要な機能は、Pygameの使用を許可します。以下はプロンプトと実装例です。
        風の影響も考慮した斜方投射シミュレーション
        import pygame
        import math
        import tkinter as tk
        from tkinter import ttk

        def can_handle(text):
            keywords = ["斜方投射", "シミュレーション", "風", "影響"]
            return any(keyword in text for keyword in keywords)

        def handle(text, root, result_callback):
            toplevel = tk.Toplevel(root)
            toplevel.title("斜方投射シミュレーション")

            # 入力欄
            ttk.Label(toplevel, text="初速度 (m/s):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
            velocity_entry = ttk.Entry(toplevel)
            velocity_entry.insert(0, "20")
            velocity_entry.grid(row=0, column=1)

            ttk.Label(toplevel, text="角度 (度):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
            angle_entry = ttk.Entry(toplevel)
            angle_entry.insert(0, "45")
            angle_entry.grid(row=1, column=1)

            ttk.Label(toplevel, text="風速 (m/s):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
            wind_entry = ttk.Entry(toplevel)
            wind_entry.insert(0, "5")
            wind_entry.grid(row=2, column=1)

            ttk.Label(toplevel, text="風向き (度):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
            wind_angle_entry = ttk.Entry(toplevel)
            wind_angle_entry.insert(0, "0")
            wind_angle_entry.grid(row=3, column=1)

            ttk.Label(toplevel, text="重力加速度 (m/s^2):").grid(row=4, column=0, padx=5, pady=5, sticky="e")
            gravity_entry = ttk.Entry(toplevel)
            gravity_entry.insert(0, "9.81")
            gravity_entry.grid(row=4, column=1)

            def run_simulation():
                try:
                    v = float(velocity_entry.get())
                    angle = float(angle_entry.get())
                    wind_v = float(wind_entry.get())
                    wind_theta = float(wind_angle_entry.get())
                    g = float(gravity_entry.get())
                except ValueError:
                    result_callback("無効な数値入力があります")
                    toplevel.destroy()
                    return

                toplevel.destroy()  # 入力ウィンドウを閉じる

                pygame.init()
                width, height = 800, 600
                screen = pygame.display.set_mode((width, height))
                pygame.display.set_caption("斜方投射シミュレーション")
                clock = pygame.time.Clock()

                # 色
                white = (255, 255, 255)
                red = (255, 0, 0)
                blue = (0, 0, 255)

                # 初期値
                x, y = 50, height - 50
                theta_rad = math.radians(angle)
                wind_rad = math.radians(wind_theta)

                vx = v * math.cos(theta_rad)
                vy = -v * math.sin(theta_rad)

                wind_x = wind_v * math.cos(wind_rad)
                wind_y = -wind_v * math.sin(wind_rad)

                trail = []

                running = True
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False

                    vx += wind_x / 60
                    vy += g / 60
                    x += vx
                    y += vy

                    if y > height - 50:
                        y = height - 50
                        vy *= -0.6

                    trail.append((int(x), int(y)))

                    screen.fill(white)
                    pygame.draw.rect(screen, (0, 128, 0), (0, height - 50, width, 50))  # 地面
                    for pt in trail:
                        pygame.draw.circle(screen, blue, pt, 2)
                    pygame.draw.circle(screen, red, (int(x), int(y)), 10)

                    pygame.display.flip()
                    clock.tick(60)

                pygame.quit()
                result_callback("シミュレーションが終了しました。")

            ttk.Button(toplevel, text="シミュレーション開始", command=run_simulation).grid(row=5, column=0, columnspan=2, pady=10)


### 禁止事項
- `flet`, `PyQt`など、**`tkinter`,`Pygame`以外のGUIライブラリの使用は固く禁止します。**
- `input()` 関数の使用は禁止です。
- `os`, `subprocess`など、セキュリティ上問題のあるモジュールの使用は禁止です。
- 必要に応じ、`os`,`subprocess`などのセキュリティ上問題のあるモジュールと、`flet`, `PyQt`など、**`tkinter`,`Pygame`以外のGUIライブラリ以外であれば、使用を認めます。例：OpenCVなど

### その他ルール
- コード部分のみを出力し、説明やマークダウンは含めないでください。
- ファイル名は要求に沿った名前にしてください。
- 物理演算機能などのグラフが必要な機能は必ずその機能も実装して下さい。グラフは入力された値に応じて変化するものでなければなりません。
- また、生成される機能の中でデータ保存が必要な場合は、フォルダを作成し、その中に.txtや.csvでデータを保存することを許可します。

要求: 「{prompt}」
"""

def generate_plugin_code(prompt: str) -> str:
    full_prompt = PROMPT_TEMPLATE.format(prompt=prompt)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
    )
    if not response.text:
        return ""
    
    code = response.text.strip()
    if code.startswith("```python"):
        code = code[9:]
    if code.endswith("```"):
        code = code[:-3]
    return code.strip()
