from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
import re

@tool
def web_scrape(url: str) -> str:
    """
    Scrape and extract clean text content from a web page.

    Use this tool when you need to read the full content of a specific URL
    found during web search. Removes navigation, ads, scripts, and other
    clutter using both tag and regex-based class/ID matching.

    Args:
        url (str): The full URL of the web page to scrape.

    Returns:
        str: Clean, structured text extracted from the page with metadata,
             capped at approximately 3000 words.
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=8)
        response.raise_for_status()
    except requests.exceptions.RequestException as fetch_error:
        return f"[ERROR] Failed to fetch URL: {url}\nDetails: {fetch_error}"

    soup = BeautifulSoup(response.text, "html.parser")

    # Decompose Unwanted Tags
    unwanted_tags = [
        "script",
        "style",
        "nav",
        "footer",
        "header",
        "aside",
        "noscript",
        "iframe",
        "form",
        "button",
        "svg",
        "canvas",
        "video",
        "audio",
        "source",
        "dialog",
        "meta",
        "link",
    ]
    for tag_name in unwanted_tags:
        for tag_element in soup.find_all(tag_name):
            tag_element.decompose()

    # Regex Class & ID Decomposer
    clutter_pattern = re.compile(
        r"nav|menu|sidebar|footer|header|ad-|ads-|advert|banner|popup|modal|cookie|comment|social|share|widget",
        re.IGNORECASE,
    )

    clutter_selectors = [
        {"class_": clutter_pattern},
        {"id": clutter_pattern},
    ]

    for selector in clutter_selectors:
        for clutter_element in soup.find_all(**selector):
            clutter_element.decompose()

    # Extract Text while Preserving Paragraphs
    raw_text = soup.get_text(separator="\n", strip=True)

    # Clean up excessive newlines
    cleaned_lines = [line.strip() for line in raw_text.splitlines() if line.strip()]

    # Smart Truncation
    word_count = 0
    final_lines = []

    for line in cleaned_lines:
        line_words = line.split()
        if word_count + len(line_words) <= 3000:
            final_lines.append(line)
            word_count += len(line_words)
        else:
            remaining_words = 3000 - word_count
            if remaining_words > 0:
                final_lines.append(" ".join(line_words[:remaining_words]))
            final_lines.append("\n\n[NOTE: Content truncated at 3000 words.]")
            word_count = 3000
            break

    cleaned_text = "\n".join(final_lines)

    page_title = soup.title.get_text(strip=True) if soup.title else "No Title Found"

    output = (
        f"URL: {url}\n"
        f"Title: {page_title}\n"
        f"Word Count: {word_count}\n"
        f"{'=' * 60}\n\n"
        f"{cleaned_text}"
    )

    return output
