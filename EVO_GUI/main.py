import tkinter as tk
from tkinter import ttk
from evo_first import EvoCore
from functools import partial

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EVO")
        self.geometry("800x600")

        self.core = EvoCore()
        
        self.style = ttk.Style(self)
        self.style.configure("TButton", padding=6, relief="flat", background="#ccc")
        self.style.configure("Sidebar.TButton", padding=(10, 6), anchor="w")

        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.sidebar_frame = ttk.Frame(main_frame, width=150)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        separator = ttk.Separator(main_frame, orient='vertical')
        separator.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        content_frame = ttk.Frame(main_frame)
        content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.log_text = tk.Text(content_frame, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 10))
        log_scrollbar = ttk.Scrollbar(content_frame, command=self.log_text.yview)
        self.log_text.config(yscrollcommand=log_scrollbar.set)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        input_frame = ttk.Frame(content_frame)
        input_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        self.input_entry = ttk.Entry(input_frame, font=("Arial", 11))
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input_entry.bind("<Return>", self.send_command)
        send_button = ttk.Button(input_frame, text="送信", command=self.send_command)
        send_button.pack(side=tk.RIGHT, padx=5)
        
        self.log_text.tag_config("user", foreground="blue")
        self.log_text.tag_config("system", foreground="green")
        self.log_text.tag_config("plugin", foreground="purple")
        self.log_text.tag_config("info", foreground="gray")

        self.update_sidebar()
        self.display_message("ようこそ！左のサイドバーから機能を選択するか、下の入力欄から 'evo: [内容]' で新しい機能を生成してください。", "info")
        if not self.core.plugin_names:
            self.display_message("まだ機能がありません。'evo: 電卓機能' のように入力して、最初の機能を生成してみましょう。", "info")


    def update_sidebar(self):
        for widget in self.sidebar_frame.winfo_children():
            widget.destroy()
        
        for name in self.core.plugin_names:
            button_command = partial(self.run_plugin_from_sidebar, name)
            button = ttk.Button(self.sidebar_frame, text=name.capitalize(), style="Sidebar.TButton", command=button_command)
            button.pack(fill=tk.X, pady=2)

    def display_message(self, message, tag="system"):
        self.log_text.config(state=tk.NORMAL)
        if self.log_text.index('end-1c') != "1.0":
            self.log_text.insert(tk.END, "\n")
        
        prefix = {"user": "You: ", "system": "EVO: ", "plugin": "Plugin: ", "info": "Info: "}
        self.log_text.insert(tk.END, prefix.get(tag, ""), tag)
        self.log_text.insert(tk.END, message)
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)

    def send_command(self, event=None):
        command = self.input_entry.get()
        if not command:
            return
        
        self.display_message(command, "user")
        self.input_entry.delete(0, tk.END)

        response = self.core.handle_command(command, self, self.handle_plugin_result)
        
        if response:
            self.display_message(response, "system")

        if command.lower().strip().startswith("evo:") and response and "成功しました" in response:
            self.update_sidebar()
            
    def run_plugin_from_sidebar(self, plugin_name):
        self.display_message(f"サイドバーから '{plugin_name}' を実行します...", "system")
        self.core.handle_command(plugin_name, self, self.handle_plugin_result)

    def handle_plugin_result(self, result_text):
        self.display_message(result_text, "plugin")

if __name__ == "__main__":
    app = App()
    app.mainloop()
