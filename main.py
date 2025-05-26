from evo_first import EvoCore

def main():
    core = EvoCore()
    print("=== EVO CUI プロトタイプ ===")
    print("自然言語で指示を入力してください。'exit'で終了。")

    while True:
        try:
            user_input = input(">>> ")
            if user_input.lower() in ["exit", "quit"]:
                break

            if user_input.startswith("evolve:"):
                parts = user_input.split(":")
                if len(parts) < 3:
                    print("[エラー] コマンド形式が不正です。'evolve:ファイル名:コード' の形式で入力してください。")
                    continue
                _, filename, *code_lines = parts
                code = ":".join(code_lines).strip()
                description = f"ユーザーが追加した {filename}"
                result = core.evolve(description, filename.strip(), code)
                print(result)
                continue

            response = core.handle_command(user_input)
            print(response)
        except Exception as e:
            print(f"[エラー] {e}")

if __name__ == "__main__":
    main()