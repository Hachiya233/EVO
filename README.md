## License

This project is licensed under the MIT License - see the [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) for details.

# EVO
ユーザの自然言語入力によって機能を追加するソフトウェアアーキテクチャのプロトタイプです。  
使用する際はmain.pyから実行して下さい。  

# セキュリティリスクについて
AIが意図せず、データ削除や情報漏洩をはじめとした、システムに損害を与えるコードを生成・組み込む可能性が潜在的にあります。  
信頼できない環境での実行や、重要なデータを扱うマシンでの使用は絶対に避けてください。   
本ソフトウェアを使用する際は、リスクを理解し、自己責任の上でお願いします。

# 更新履歴
2025.5.26  
EVOについて説明する図表を追加しました。   
EVO本体を公開しました。

2025.6.25  
gemini_util.py部分を変更しました。
2.0 Flashで安定することがわかったので、モデルをそちらに変更しました。  
また、プロンプト文もより厳密にしました。

2025.6.26  
EVOのGUIバージョンを公開しました。  
また、GUIバージョンはGeminiのモデルを2.5 Flashに変更しています。  

2025.7.9  
EVO_GUIのevo_first.pyとgemini_util.pyを改良しました。  
evo_first.pyには、機能改良機能(少し気持ち悪い表現ですが)を追加し、gemini_util.pyは現行のGemini APIの呼び出し方式に変更しました。  
改良の際は、テキストボックスに”改良”と入力し、実行すると改良機能が扱えます。  
また、説明し忘れていましたが、機能追加は、テキストボックスに”evo:追加したい何らかの機能”と入力し、実行すると機能が追加できます。 
