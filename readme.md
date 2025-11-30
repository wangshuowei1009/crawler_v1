# 🇯🇵 **日本語 README **
# 📘 Zhihu Crawler Assistant（知乎スクレイパー）

**PyQt5 + Selenium** で作られたデスクトップアプリです。  
知乎（Zhihu）の質問ページから **すべての回答を取得** し、  
**遅延読み込み（Lazy Loading）** や **時系列で並ばない公式ソート** を解決し、  
回答を **時間順（新しい順）に並べて** `answers.txt` として出力できます。

## なぜこのツールが必要？

知乎の回答ページは：

- 遅延読み込みのため、下までスクロールしないと内容が読み込まれない  
- 公式の並び順が時間順ではなく、**最新の回答が埋もれる**  
- 回答数が数千件に及ぶこともあり、手作業で確認するのは困難  

このツールは次のことを実現します：

✔ 全回答を自動スクロールで読み込み  
✔ 「すべてを見る」ボタンを自動クリック  
✔ **時間順（新しい→古い）で並べ替え可能**  
✔ 読みやすい `answers.txt` へ出力  

---

## ✨ 機能

- 🖥️ デスクトップ GUI（PyQt5）
- 🌐 ユーザー自身の Chrome プロファイルで起動（ログイン状態保持）
- ⚡ 高速オートスクロールで Lazy Loading を強制読み込み
- 🔍 「すべてを見る」を自動で探してクリック
- 📝 出力内容：
  - 質問タイトル  
  - 各回答の **投稿者 / 時間 / 内容**  
- ⏱ **時間順ソート（新しい順）をサポート**
- 📄 出力ファイルのプレビュー機能付き

---

## 🔧 必要環境

- Python 3.8+
- Google Chrome
- 必要なパッケージ：

```bash
pip install selenium webdriver-manager PyQt5 beautifulsoup4

仮想環境の使用を推奨します。

⸻

🚀 使い方

1. アプリを起動

python zhihu_app_en.py


⸻

2. GUI の手順

① Chrome を開く（ログイン状態で起動）

以下のカスタムプロファイルで Chrome が起動します：

~/.zhihu_scraper_profile

初回のみ、この Chrome で知乎にログインしてください。

⸻

② Chrome で取得したい知乎の質問ページを開く

例：

https://www.zhihu.com/question/xxxx


⸻

③ アプリに戻り「高速スクロールで取得」をクリック

プログラムは：
	•	最後のタブに自動切替
	•	「すべてを見る」を試行クリック
	•	ページの高さが変わらなくなるまで自動スクロール
	•	ページを zhihu_page.html として保存

⸻

④ 「解析して TXT 出力」をクリック
	•	すべての回答を解析
	•	チェックが付いていれば時間順（新しい順）で並べ替え
	•	出力：

answers.txt

	•	右側のプレビューパネルにも表示

⸻

📜 ライセンス

本ツールは学習・研究用途で自由にご利用いただけます。
知乎の利用規約に反する目的で使用しないでください。


⸻

🇺🇸 English README 

# 📘 Zhihu Crawler Assistant

A desktop application built with **PyQt5 + Selenium** to scrape all answers from a Zhihu question.  
It solves issues such as **lazy loading**, **non-chronological official sorting**, and supports exporting answers in **time-sorted order** (newest → oldest) to `answers.txt`.

## Why this tool?

Zhihu's answer pages often:
- Load content lazily (require continuous scrolling)
- Do not sort by time, causing **new answers to be buried**
- Contain thousands of answers, making manual browsing difficult

This tool helps you:
✔ Fully load all answers  
✔ Automatically click “View All Answers”  
✔ Sort answers by time (descending)  
✔ Export clean, readable `answers.txt`  

---

## ✨ Features

- 🖥️ Desktop GUI (PyQt5)
- 🌐 Launch Chrome with your own profile (keeps login session)
- ⚡ High-speed auto-scroll to trigger lazy loading
- 🔍 Automatically attempts to click “View All”
- 📝 Extracts and exports:
  - Question title  
  - Answer author / time / content  
- ⏱ Optional: **Sort by time (newest first)**
- 📄 Built-in preview panel for `answers.txt`

---

## 🔧 Requirements

- Python 3.8+
- Google Chrome
- Required packages:

```bash
pip install selenium webdriver-manager PyQt5 beautifulsoup4

Using a virtual environment is recommended.

⸻

🚀 Usage

1. Run the program

python zhihu_app_en.py

2. Steps in the GUI

⸻

① Open Chrome (with login)

Chrome is launched with a custom profile:

~/.zhihu_scraper_profile

Log into Zhihu manually (first time only).

⸻

② In Chrome, manually open the Zhihu question page you want to crawl

Example:

https://www.zhihu.com/question/xxxx


⸻

③ Back in the app, click “Crawl Current Page (Fast Scroll)”

The program will:
	•	Switch to the last opened tab
	•	Attempt to click “View All”
	•	Auto-scroll repeatedly until the page stops growing
	•	Save the HTML as:

zhihu_page.html


⸻

④ Click “Parse HTML and Export TXT”

The app will:
	•	Parse all answers
	•	Sort by time if the option is checked
	•	Generate:

answers.txt

	•	Display the result in the preview panel

⸻

📜 License

You may freely use and modify this tool for learning or research.
Do not use it for activities that violate Zhihu’s terms of service.

---

