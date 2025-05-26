from gemini_util import generate_plugin_code
import os
import importlib.util
import re
import ast

class EvoCore:
    def __init__(self):
        self.plugins = {}
        self.load_plugins()

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

    def handle_command(self, text):
        text = text.lower().strip()

        if text == "help":
            return "利用可能なプラグイン: " + ", ".join(self.plugins.keys())

        if text.startswith("evo:"):
            request = text.replace("evo:", "").strip()
            return self.evolve_with_gemini(request)

        for name, plugin in self.plugins.items():
            if hasattr(plugin, "can_handle") and plugin.can_handle(text):
                return plugin.handle(text)

        if text in self.plugins:
            plugin = self.plugins[text]
            if hasattr(plugin, "handle"):
                return plugin.handle("__direct__")

        return f"「{text}」に対応するコマンドやプラグインが見つかりません。"

    def evolve_with_gemini(self, user_request: str):
        print(f"[Geminiに送信中] 要求: {user_request}")
        code = generate_plugin_code(user_request)

        if not code or len(code.strip()) < 10:
            return "[エラー] Geminiのコード生成に失敗しました。"

        # 安全なファイル名生成
        base_name = user_request.split()[0].replace("する", "").replace("機能", "")
        base_name = re.sub(r'[^\w]', '_', base_name)
        if not base_name:
            base_name = "plugin"
        filename = f"{base_name}.py"
        path = os.path.join("plugins", filename)

        code_lines = code.strip().splitlines()
        if len(code_lines) > 2:
            code = "\n".join(code_lines[1:-1])
            
        # 危険なコード検出（簡易AST検査）
        #try:
        #    tree = ast.parse(code)
        #    for node in ast.walk(tree):
        #        if isinstance(node, (ast.Exec, ast.Call)):
        #            if isinstance(node, ast.Call) and hasattr(node.func, "id"):
        #                if node.func.id in ["exec", "eval", "os", "system", "subprocess"]:
        #                    return "[エラー] 危険なコードが検出されました。"
        #except Exception as e:
        #    return f"[エラー] コードの安全性チェックに失敗しました: {e}",code

        with open(path, "w") as f:
            f.write(code)

        with open("evolutions.log", "a") as log:
            log.write(f"[進化] {user_request} -> {filename}\n")

        self.load_plugins()
        return f"{filename} を生成し、進化に成功しました。"