from dotenv import load_dotenv
import sys
from scraper import get_page_content
from analyzer import analyze_content
from reviser import revise_content

load_dotenv()

def format_feedback(analysis: dict) -> str:
    parts = []
    for cat, val in analysis.items():
        parts.append(f"{cat.upper()}:\nScore: {val['score']}")
        parts += [f"- {x}" for x in val['suggestions']]
    return "\n".join(parts)

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <documentation_url>")
        return

    url = sys.argv[1]
    print("Scraping...")
    content = get_page_content(url)
    
    print("Analyzing...")
    analysis = analyze_content(url, content)
    print("Analysis:", analysis)

    print("Revising...")
    feedback_text = format_feedback(analysis)
    revised = revise_content(content, feedback_text)

    with open("revised.txt", "w", encoding="utf-8") as f:
        f.write(revised)

    print("✅ Done. Output saved to revised.txt")

if __name__ == "__main__":
    main()
