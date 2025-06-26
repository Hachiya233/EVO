from gemini_util import generate_plugin_code
import os
import importlib.util
import re

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
        count = 1
        while os.path.exists(path):
            filename = f"{base_name}_{count}.py"
            path = os.path.join("plugins", filename)
            count += 1

        with open(path, "w", encoding="utf-8") as f:
            f.write(code)

        with open("evolutions.log", "a", encoding="utf-8") as log:
            log.write(f"[進化] {user_request} -> {filename}\n")

        self.load_plugins()
        return f"{filename} を生成し、進化に成功しました。"