from gemini_util import generate_plugin_code
import os
import importlib.util
import re
import tkinter as tk
from tkinter import simpledialog, ttk

class EvoCore:
    def __init__(self):
        self.plugins = {}
        self.load_plugins()

    @property
    def plugin_names(self):
        return sorted(list(self.plugins.keys()))

    def load_plugins(self):
        self.plugins = {}
        plugin_dir = "plugins"
        os.makedirs(plugin_dir, exist_ok=True)

        for filename in os.listdir(plugin_dir):
            if filename.endswith(".py") and ".." not in filename:
                name = filename[:-3]
                path = os.path.join(plugin_dir, filename)
                try:
                    spec = importlib.util.spec_from_file_location(name, path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    self.plugins[name] = mod
                except Exception as e:
                    print(f"[プラグイン読み込みエラー] {filename}: {e}")

    def handle_command(self, text, root, result_callback):
        original_text = text
        command_text = text.lower().strip()

        if command_text == "help":
            return "利用可能なプラグイン: " + ", ".join(self.plugins.keys())

        if command_text.startswith("evo:"):
            request = original_text.replace("evo:", "").strip()
            return self.evolve_with_gemini(request)

        if command_text == "改良":
            return self.show_improvement_dialog(root)

        if command_text in self.plugins:
            plugin = self.plugins[command_text]
            if hasattr(plugin, "handle"):
                return plugin.handle(command_text, root, result_callback)

        for name, plugin in self.plugins.items():
            if hasattr(plugin, "can_handle") and plugin.can_handle(command_text):
                if hasattr(plugin, "handle"):
                    return plugin.handle(command_text, root, result_callback)

        return f"「{original_text}」に対応するコマンドやプラグインが見つかりません。"

    def evolve_with_gemini(self, user_request: str):
        print(f"[Geminiに送信中] 要求: {user_request}")
        code = generate_plugin_code(user_request)

        if not code or len(code.strip()) < 10:
            return "[エラー] Geminiのコード生成に失敗しました。"

        base_name_req = user_request.split("を")[0].split("の")[0].strip()
        base_name = re.sub(r'[^\w]', '_', base_name_req)
        if not base_name:
            base_name = "plugin"

        filename = f"{base_name}.py"
        path = os.path.join("plugins", filename)

        with open(path, "w", encoding="utf-8") as f:
            f.write(code)

        with open("evolutions.log", "a", encoding="utf-8") as log:
            log.write(f"[進化] {user_request} -> {filename}\n")

        self.load_plugins()
        return f"{filename} を生成し、進化に成功しました。"

    def show_improvement_dialog(self, root):
        dialog = tk.Toplevel(root)
        dialog.title("機能の改良")
        dialog.geometry("400x200")
        dialog.grab_set()

        ttk.Label(dialog, text="改良する機能を選択:").pack(pady=(10, 2))
        plugin_var = tk.StringVar()
        plugin_combo = ttk.Combobox(dialog, textvariable=plugin_var, values=self.plugin_names, state="readonly")
        plugin_combo.pack(pady=(0, 10))
        if self.plugin_names:
            plugin_combo.set(self.plugin_names[0])

        ttk.Label(dialog, text="改良の要望を入力:").pack()
        request_entry = ttk.Entry(dialog, width=50)
        request_entry.pack(pady=(0, 10))

        result_label = ttk.Label(dialog, text="")
        result_label.pack()

        def apply_improvement():
            plugin_name = plugin_var.get()
            request_text = request_entry.get().strip()
            if not plugin_name or not request_text:
                result_label.config(text="入力が不足しています。", foreground="red")
                return

            dialog.destroy()
            result = self.improve_plugin_with_gemini(f"{plugin_name}を{request_text}")
            tk.messagebox.showinfo("改良結果", result)

        ttk.Button(dialog, text="改良を実行", command=apply_improvement).pack(pady=(5, 10))

    def improve_plugin_with_gemini(self, user_request: str):
        print(f"[Geminiに送信中: 改良] 要求: {user_request}")

        plugin_name_candidate = user_request.split("を")[0].split("の")[0].strip()
        base_name = re.sub(r'[^\w]', '_', plugin_name_candidate)
        plugin_path = os.path.join("plugins", f"{base_name}.py")

        if not os.path.exists(plugin_path):
            return f"[エラー] 「{base_name}」に対応する既存のプラグインが見つかりません。"

        with open(plugin_path, "r", encoding="utf-8") as f:
            original_code = f.read()

        prompt = f"""以下のTkinterベースのプラグインコードを改良してください。具体的には、ユーザーの要望に従って使いやすさ・機能性・表示を改善してください。

# ユーザーの改良要望:
{user_request}

# 元のコード:
{original_code}
"""

        improved_code = generate_plugin_code(prompt)

        if not improved_code or len(improved_code.strip()) < 10:
            return "[エラー] Geminiによる改良に失敗しました。"

        with open(plugin_path, "w", encoding="utf-8") as f:
            f.write(improved_code)

        with open("evolutions.log", "a", encoding="utf-8") as log:
            log.write(f"[改良] {user_request} -> {base_name}.py (上書き)\n")

        self.load_plugins()
        return f"{base_name}.py を上書きし、改良に成功しました。"
