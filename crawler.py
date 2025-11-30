import sys
import time
import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLabel, QCheckBox,
    QGroupBox, QSplitter
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from bs4 import BeautifulSoup


# ===== Chrome profile directory (cross-platform) =====
CHROME_USER_DATA_DIR = str(Path.home() / ".zhihu_scraper_profile")


class ZhihuApp(QWidget):

    def __init__(self):
        super().__init__()
        self.driver = None

        self.setWindowTitle("Zhihu Scraper Assistant")
        self.resize(1000, 650)

        self.init_style()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        # Title
        title_label = QLabel("Zhihu Scraper Assistant")
        title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: 600; color: #111827;")

        subtitle_label = QLabel(
            "Steps: ① Open Chrome with login → ② Manually open the question page → ③ Crawl and export answers"
        )
        subtitle_label.setStyleSheet("color: #6B7280; font-size: 12px;")

        main_layout.addWidget(title_label)
        main_layout.addWidget(subtitle_label)

        # ===== Control Area =====
        control_group = QGroupBox("Controls")
        control_layout = QVBoxLayout()
        control_layout.setSpacing(8)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        self.btn_start_browser = QPushButton("① Open Chrome (with login)")
        self.btn_wait_and_scroll = QPushButton("② Crawl Current Question Page (Fast Scroll)")
        self.btn_parse = QPushButton("③ Parse HTML and Export TXT")

        self.btn_wait_and_scroll.setEnabled(False)
        self.btn_parse.setEnabled(False)

        btn_row.addWidget(self.btn_start_browser)
        btn_row.addWidget(self.btn_wait_and_scroll)
        btn_row.addWidget(self.btn_parse)

        option_row = QHBoxLayout()
        option_row.setSpacing(16)

        self.chk_sort_by_time = QCheckBox("Sort by time (newest first)")
        self.chk_sort_by_time.setChecked(True)

        hint_label = QLabel("Tip: First time, please manually log in inside the opened Chrome.")
        hint_label.setStyleSheet("color: #6B7280; font-size: 11px;")

        option_row.addWidget(self.chk_sort_by_time)
        option_row.addStretch()
        option_row.addWidget(hint_label)

        control_layout.addLayout(btn_row)
        control_layout.addLayout(option_row)
        control_group.setLayout(control_layout)

        main_layout.addWidget(control_group)

        # ===== Logs + Preview Splitter =====
        splitter = QSplitter(Qt.Horizontal)

        # Left: logs
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)

        left_label = QLabel("Logs")
        left_label.setStyleSheet("font-size: 13px; font-weight: 500; color: #111827;")

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        left_layout.addWidget(left_label)
        left_layout.addWidget(self.log)
        left_widget.setLayout(left_layout)

        # Right: preview
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)

        right_label = QLabel("Preview (answers.txt)")
        right_label.setStyleSheet("font-size: 13px; font-weight: 500; color: #111827;")

        self.result_view = QTextEdit()
        self.result_view.setReadOnly(True)

        right_layout.addWidget(right_label)
        right_layout.addWidget(self.result_view)
        right_widget.setLayout(right_layout)

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)

        main_layout.addWidget(splitter, stretch=1)

        self.setLayout(main_layout)

        # Bind events
        self.btn_start_browser.clicked.connect(self.start_browser)
        self.btn_wait_and_scroll.clicked.connect(self.scroll_page)
        self.btn_parse.clicked.connect(self.parse_html)

    # ---------------- UI Style ----------------
    def init_style(self):
        font = QFont("PingFang SC", 11)
        QApplication.instance().setFont(font)

        self.setStyleSheet("""
        QWidget { background-color: #F3F4F6; }
        QGroupBox {
            border: 1px solid #E5E7EB;
            border-radius: 10px;
            margin-top: 12px;
            padding: 8px 10px 12px 10px;
            background-color: #FFFFFF;
        }
        QGroupBox::title {
            left: 10px;
            padding: 0 4px;
            color: #6B7280;
            font-size: 12px;
        }
        QPushButton {
            background-color: #2563EB;
            color: white;
            border-radius: 8px;
            padding: 8px 14px;
            border: none;
            font-size: 13px;
        }
        QPushButton:hover { background-color: #1D4ED8; }
        QPushButton:pressed { background-color: #1E40AF; }
        QPushButton:disabled {
            background-color: #D1D5DB;
            color: #9CA3AF;
        }
        QTextEdit {
            background-color: #111827;
            color: #E5E7EB;
            border-radius: 8px;
            padding: 8px;
            border: 1px solid #1F2937;
            font-family: Menlo, Monaco, 'Courier New', monospace;
            font-size: 11px;
        }
        QCheckBox { font-size: 11px; color: #374151; }
        QLabel { font-size: 12px; }
        QSplitter::handle { background-color: #E5E7EB; }
        QSplitter::handle:hover { background-color: #CBD5F5; }
        """)

    #Feature 1: Start Chrome with Selenium

    def start_browser(self):
        try:
            self.log.append("🚀 Starting Chrome (Selenium mode)…")

            chrome_options = webdriver.ChromeOptions()

            # Use custom user directory to keep login session
            chrome_options.add_argument(f"--user-data-dir={CHROME_USER_DATA_DIR}")
            chrome_options.add_argument("--start-maximized")

            # Remove automation flags
            chrome_options.add_experimental_option(
                "excludeSwitches", ["enable-automation"]
            )
            chrome_options.add_experimental_option("useAutomationExtension", False)
            chrome_options.add_argument(
                "--disable-blink-features=AutomationControlled"
            )

            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)

            # Hide navigator.webdriver
            try:
                self.driver.execute_cdp_cmd(
                    "Page.addScriptToEvaluateOnNewDocument",
                    {
                        "source": """
                        Object.defineProperty(navigator, 'webdriver', {
                          get: () => undefined
                        });
                        """
                    },
                )
                self.log.append("✨ navigator.webdriver hidden.")
            except Exception as e:
                self.log.append(f"⚠️ Failed to hide webdriver flag: {e}")

            self.log.append("✅ Chrome launched successfully.")

            # Open Zhihu homepage
            try:
                self.log.append("🌐 Opening Zhihu homepage…")
                time.sleep(1)
                self.driver.get("https://www.zhihu.com/")
                self.log.append("✅ Zhihu homepage opened.")
            except Exception as e:
                self.log.append(f"⚠️ Failed to open Zhihu: {e}")

            self.log.append("👉 Please log in manually if needed.")
            self.log.append("👉 Then manually open the question page before clicking step ②.")
            self.btn_wait_and_scroll.setEnabled(True)

        except Exception as e:
            self.log.append(f"❌ Chrome failed to start: {e}")


    #Feature 2: High-speed scrolling

    def scroll_page(self):
        if not self.driver:
            self.log.append("❌ Chrome not started yet.")
            return

        self.log.append("📌 Switching to last tab…")

        try:
            handles = self.driver.window_handles
            self.driver.switch_to.window(handles[-1])
            self.log.append(f"📌 Current tab: {self.driver.current_url}")
        except Exception as e:
            self.log.append(f"⚠️ Tab switch failed: {e}")

        time.sleep(2)

        clicked = False
        try:
            btn = self.driver.find_element(By.XPATH, '//a[contains(text(),"View All")]')
            btn.click()
            clicked = True
            self.log.append("🔍 Clicked 'View All' (XPATH)")
        except:
            pass

        if not clicked:
            try:
                btn = self.driver.find_element(
                    By.CSS_SELECTOR,
                    '[data-za-detail-view-element_name="ViewAll"]'
                )
                btn.click()
                clicked = True
                self.log.append("🔍 Clicked 'View All' (CSS fallback)")
            except:
                self.log.append("⚠️ 'View All' not found.")

        time.sleep(2)

        self.log.append("⚡ Fast scrolling…")

        max_scroll = 200
        scroll_count = 0

        last_height = self.driver.execute_script("return document.body.scrollHeight")
        last_change_time = time.time()
        stuck_once = False

        while scroll_count < max_scroll:

            self.driver.execute_script("""
                window.scrollTo(0, document.body.scrollHeight);
                window.scrollBy(0, -200);
            """)

            scroll_count += 1
            time.sleep(0.4)

            new_height = self.driver.execute_script("return document.body.scrollHeight")
            now = time.time()

            if new_height != last_height:
                last_change_time = now
                last_height = new_height
                stuck_once = False
                continue

            if (not stuck_once) and (now - last_change_time >= 5):
                self.log.append("⚠️ No change for 5s, scrolling up slightly…")
                self.driver.execute_script("window.scrollBy(0, -window.innerHeight * 0.5);")
                stuck_once = True
                continue

            if stuck_once and (now - last_change_time >= 10):
                self.log.append("📌 No change for 10s, stopping scroll.")
                break

        self.log.append(f"🎉 Scroll finished. Total scrolls: {scroll_count}")

        html = self.driver.page_source
        with open("zhihu_page.html", "w", encoding="utf-8") as f:
            f.write(html)

        self.log.append("📁 Saved as zhihu_page.html")
        self.btn_parse.setEnabled(True)


# parse time str → datetime

    def parse_time_str(self, t: str) -> datetime.datetime:
        if not t:
            return datetime.datetime.min
        t = t.strip()
        if not t:
            return datetime.datetime.min

        patterns = [
            "%Y-%m-%d %H:%M",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d"
        ]
        for fmt in patterns:
            try:
                return datetime.datetime.strptime(t, fmt)
            except:
                continue
        return datetime.datetime.min


    #Feature 3: Parse HTML → TXT

    def parse_html(self):
        try:
            html_file = "zhihu_page.html"
            out_file = "answers.txt"

            with open(html_file, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "html.parser")

            answers = []

            # Question title
            question_title_tag = soup.select_one('meta[itemprop="name"]')
            question_title = (
                question_title_tag.get("content", "").strip()
                if question_title_tag else "(Question title not found)"
            )

            # Parse answers
            for ans in soup.select('[itemtype="http://schema.org/Answer"]'):

                author_tag = ans.select_one('.AuthorInfo [itemprop="name"]')
                if author_tag:
                    author = author_tag.get("content") or author_tag.get_text(strip=True)
                else:
                    link = ans.select_one(".AuthorInfo .UserLink-link")
                    author = link.get_text(strip=True) if link else "Unknown Author"

                time_a = ans.select_one(".ContentItem-time a")
                if time_a:
                    raw = (
                        time_a.get_text(strip=True)
                        or time_a.get("data-tooltip")
                        or time_a.get("aria-label")
                        or ""
                    )
                    raw = raw.replace("Published on", "").replace("Edited on", "")
                    publish_time = raw.strip()
                else:
                    meta_time = ans.select_one('meta[itemprop="dateCreated"]')
                    if meta_time and meta_time.has_attr("content"):
                        publish_time = meta_time["content"].replace("T", " ").replace(".000Z", "")
                    else:
                        publish_time = ""

                text_span = ans.select_one('.RichContent-inner span[itemprop="text"]')
                if text_span:
                    ps = text_span.find_all("p")
                    content = (
                        "\n".join(p.get_text(strip=True) for p in ps)
                        if ps else text_span.get_text("\n", strip=True)
                    )
                else:
                    rich = ans.select_one(".RichContent-inner")
                    content = rich.get_text("\n", strip=True) if rich else ""

                if author and content:
                    answers.append({
                        "author": author,
                        "time": publish_time,
                        "content": content
                    })

            if self.chk_sort_by_time.isChecked():
                answers.sort(
                    key=lambda x: self.parse_time_str(x["time"]),
                    reverse=True
                )
                self.log.append("⏱ Sorted by time (newest first).")
            else:
                self.log.append("⏱ Original webpage order preserved.")

            preview_lines = []

            with open(out_file, "w", encoding="utf-8") as f:
                f.write("Question:\n")
                f.write(question_title + "\n")
                f.write("=" * 40 + "\n\n")

                preview_lines.append("Question:")
                preview_lines.append(question_title)
                preview_lines.append("=" * 40)
                preview_lines.append("")

                for i, a in enumerate(answers, 1):
                    block = [
                        f"Answer #{i}",
                        f"Author: {a['author']}",
                        f"Time: {a['time']}",
                        "Content:",
                        a["content"],
                        "-" * 40,
                        ""
                    ]
                    for line in block:
                        f.write(line + "\n")
                    f.write("\n")
                    preview_lines.extend(block)

            self.log.append(f"🎉 Done! Exported {len(answers)} answers → {out_file}")

            preview_text = "\n".join(preview_lines)
            self.result_view.setPlainText(preview_text)
            self.result_view.moveCursor(self.result_view.textCursor().Start)

        except Exception as e:
            self.log.append(f"❌ Parsing failed: {e}")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ZhihuApp()
    window.show()
    sys.exit(app.exec_())