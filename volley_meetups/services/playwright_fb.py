import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE_PATH = PROJECT_ROOT / ".env"
DEFAULT_SESSION_FILE_PATH = PROJECT_ROOT / ".facebook_session.json"


def _load_env_file(path: Path = ENV_FILE_PATH) -> dict[str, str]:
    """讀取專案根目錄的 .env，格式為 KEY=VALUE。"""
    if not path.exists():
        return {}

    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")

    return values


def _get_config_value(key: str, default: str = "") -> str:
    return os.getenv(key) or ENV_FILE_VALUES.get(key, default)


def _resolve_project_path(path_value: str, default_path: Path) -> Path:
    if not path_value:
        return default_path

    path = Path(path_value)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


ENV_FILE_VALUES = _load_env_file()

# 登入與目標網址請填在專案根目錄的 .env。
FACEBOOK_EMAIL = _get_config_value("FACEBOOK_EMAIL")
FACEBOOK_PASSWORD = _get_config_value("FACEBOOK_PASSWORD")
FACEBOOK_GROUP_URL = _get_config_value(
    "FACEBOOK_GROUP_URL", "https://www.facebook.com/groups/186877438033868?locale=zh_TW"
)
FACEBOOK_SESSION_FILE = _resolve_project_path(
    _get_config_value("FACEBOOK_SESSION_FILE"), DEFAULT_SESSION_FILE_PATH
)

# 爬取範圍設定。
DEFAULT_SCROLL_PIXELS = 5000
DEFAULT_MAX_POSTS = 20
DEFAULT_HEADLESS = False

# 只留下可能是「徵臨打」的貼文；不想過濾可改成空 list。
MEETUP_KEYWORDS = ["徵", "臨打", "缺", "排球", "零打"]


@dataclass
class FacebookPost:
    author: str
    content: str
    post_url: str

    def as_dict(self) -> dict[str, str]:
        return {
            "author": self.author,
            "content": self.content,
            "post_url": self.post_url,
        }


def _login_to_facebook(page: Any, email: str, password: str) -> None:
    """登入 Facebook；若沒有提供帳密則略過，嘗試直接瀏覽公開社團。"""
    if not email or not password:
        return

    page.goto("https://www.facebook.com/login", wait_until="domcontentloaded")
    _close_common_popups(page)

    email_input = page.locator('input[name="email"], input#email').first
    password_input = page.locator('input[name="pass"], input#pass').first

    email_input.wait_for(state="visible", timeout=10000)
    email_input.fill(email)
    password_input.fill(password)

    login_buttons = [
        'button[name="login"]',
        'button[type="submit"]',
        'div[role="button"][aria-label="Log in"]',
        'div[role="button"][aria-label="登入"]',
    ]

    for selector in login_buttons:
        try:
            page.locator(selector).first.click(timeout=3000)
            break
        except PlaywrightTimeoutError:
            continue
    else:
        password_input.press("Enter")

    try:
        page.wait_for_load_state("networkidle", timeout=15000)
    except PlaywrightTimeoutError:
        # Facebook 登入後常有長連線，DOM 已可用時不用因 networkidle 卡住。
        page.wait_for_timeout(3000)


def _new_facebook_context(browser: Any, session_file: Path | None) -> Any:
    context_options = {
        "locale": "zh-TW",
        "viewport": {"width": 1366, "height": 900},
        "user_agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
    }

    if session_file and session_file.exists():
        context_options["storage_state"] = str(session_file)

    return browser.new_context(**context_options)


def _page_requires_login(page: Any) -> bool:
    if "login" in page.url.lower():
        return True

    login_inputs = page.locator('input[name="email"], input[name="pass"]')
    return login_inputs.count() > 0


def _save_session(context: Any, session_file: Path | None) -> None:
    if not session_file:
        return

    session_file.parent.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=str(session_file))


def _close_common_popups(page: Any) -> None:
    """關掉常見的 cookie / 通知彈窗，避免擋住頁面操作。"""
    button_names = [
        "Allow all cookies",
        "允許所有 Cookie",
        "拒絕非必要 Cookie",
        "Not now",
        "稍後再說",
    ]

    for name in button_names:
        try:
            page.get_by_role("button", name=re.compile(name, re.I)).click(timeout=1500)
        except PlaywrightTimeoutError:
            continue


def _extract_post_url(article: Any) -> str:
    links = article.locator(
        'a[href*="/posts/"], a[href*="permalink"], a[href*="story_fbid"]'
    )

    if links.count() == 0:
        return ""

    href = links.first.get_attribute("href") or ""
    if href.startswith("/"):
        return f"https://www.facebook.com{href}"
    return href


def _extract_author(article: Any) -> str:
    headings = article.locator('strong, h2, h3, span[dir="auto"]').all_inner_texts()
    headings = [heading.strip() for heading in headings if heading.strip()]
    return headings[0] if headings else ""


def _extract_visible_text(article: Any) -> str:
    text = article.inner_text(timeout=3000)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(dict.fromkeys(lines))


def _should_keep_post(content: str, keywords: list[str] | None) -> bool:
    if not keywords:
        return True

    return any(keyword in content for keyword in keywords)


def scrape_new_fb_posts(
    group_url: str = FACEBOOK_GROUP_URL,
    email: str = FACEBOOK_EMAIL,
    password: str = FACEBOOK_PASSWORD,
    session_file: Path | None = FACEBOOK_SESSION_FILE,
    scroll_pixels: int = DEFAULT_SCROLL_PIXELS,
    max_posts: int = DEFAULT_MAX_POSTS,
    keywords: list[str] | None = MEETUP_KEYWORDS,
    headless: bool = DEFAULT_HEADLESS,
) -> list[dict[str, str]]:
    """使用 Playwright 從公開 Facebook 社團往下捲指定範圍並擷取貼文資料。"""
    if not group_url:
        raise ValueError("請先填入 FACEBOOK_GROUP_URL 或設定同名環境變數。")

    posts: list[FacebookPost] = []
    seen_contents: set[str] = set()

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=headless)
        context = _new_facebook_context(browser, session_file)
        page = context.new_page()

        try:
            page.goto(group_url, wait_until="domcontentloaded")
            _close_common_popups(page)
            try:
                page.wait_for_load_state("networkidle", timeout=15000)
            except PlaywrightTimeoutError:
                page.wait_for_timeout(3000)

            if _page_requires_login(page):
                context.close()
                context = _new_facebook_context(browser, None)
                page = context.new_page()
                _login_to_facebook(page, email, password)
                _save_session(context, session_file)
                page.goto(group_url, wait_until="domcontentloaded")
                _close_common_popups(page)
                try:
                    page.wait_for_load_state("networkidle", timeout=15000)
                except PlaywrightTimeoutError:
                    page.wait_for_timeout(3000)

            scrolled_pixels = 0
            while scrolled_pixels <= scroll_pixels and len(posts) < max_posts:
                articles = page.locator('[role="article"]')

                for index in range(articles.count()):
                    if len(posts) >= max_posts:
                        break

                    article = articles.nth(index)
                    try:
                        content = _extract_visible_text(article)
                    except PlaywrightTimeoutError:
                        continue

                    if not content or content in seen_contents:
                        continue
                    if not _should_keep_post(content, keywords):
                        continue

                    seen_contents.add(content)
                    posts.append(
                        FacebookPost(
                            author=_extract_author(article),
                            content=content,
                            post_url=_extract_post_url(article),
                        )
                    )

                page.mouse.wheel(0, 1000)
                page.wait_for_timeout(1200)
                scrolled_pixels += 1000
        finally:
            context.close()
            browser.close()

    return [post.as_dict() for post in posts]


def get_fb_posts() -> list[dict[str, str]]:
    """爬取 FB 社團目前可能是徵臨打的貼文。"""
    try:
        new_posts = scrape_new_fb_posts()
    except (PlaywrightError, ValueError) as error:
        print(f"Facebook 爬取失敗：{error}")
        return []

    # TODO: 後續可在這裡與資料庫資料合併、過濾過期貼文。
    return new_posts
