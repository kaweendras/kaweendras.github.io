"""Build the single-page, ATS-friendly downloadable CV."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "CV-SalithaWijerathna-2026-03-themed.pdf"

W, H = A4
INK = colors.HexColor("#171719")
MUTED = colors.HexColor("#5F5D63")
PAPER = colors.HexColor("#F7F5F1")
LINE = colors.HexColor("#C9C5BF")
PINK = colors.HexColor("#EFA0B0")
BLUE = colors.HexColor("#9AC4E7")

MARGIN = 16 * mm
LEFT_W = 58 * mm
GAP = 13 * mm
RIGHT_X = MARGIN + LEFT_W + GAP
RIGHT_W = W - RIGHT_X - MARGIN


def wrap(text, font, size, width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if stringWidth(trial, font, size) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def text_block(c, text, x, y, width, font="Helvetica", size=7.2, leading=10, color=INK):
    c.setFillColor(color)
    c.setFont(font, size)
    for line in wrap(text, font, size, width):
        c.drawString(x, y, line)
        y -= leading
    return y


def heading(c, label, x, y, width, size=15):
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", size)
    c.drawString(x, y, label.lower())
    y -= 6
    c.setStrokeColor(INK)
    c.setLineWidth(0.65)
    c.line(x, y, x + width, y)
    return y - 13


def label(c, text, x, y, size=7.5):
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", size)
    c.drawString(x, y, text)
    return y


def small(c, text, x, y, color=MUTED):
    c.setFillColor(color)
    c.setFont("Helvetica", 6.8)
    c.drawString(x, y, text)


def link(c, text, url, x, y, size=7):
    c.setFillColor(INK)
    c.setFont("Helvetica", size)
    c.drawString(x, y, text)
    width = stringWidth(text, "Helvetica", size)
    c.setStrokeColor(MUTED)
    c.setLineWidth(0.35)
    c.line(x, y - 1.2, x + width, y - 1.2)
    c.linkURL(url, (x, y - 2, x + width, y + size + 1), relative=0)


def bullet(c, text, x, y, width):
    return text_block(c, f"- {text}", x, y, width, size=8, leading=11.2)


def job(c, y, dates, location, title, company, company_url, intro, bullets):
    small(c, dates, RIGHT_X, y)
    location_width = stringWidth(location, "Helvetica", 6.8)
    small(c, location, RIGHT_X + RIGHT_W - location_width, y)
    y -= 16

    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 11.2)
    c.drawString(RIGHT_X, y, title)
    y -= 11

    c.setFont("Helvetica-Bold", 7.3)
    c.drawString(RIGHT_X, y, company)
    company_width = stringWidth(company, "Helvetica-Bold", 7.3)
    c.linkURL(company_url, (RIGHT_X, y - 2, RIGHT_X + company_width, y + 8), relative=0)
    y -= 14

    y = text_block(c, intro, RIGHT_X, y, RIGHT_W, size=8, leading=11.2)
    y -= 5
    for item in bullets:
        y = bullet(c, item, RIGHT_X, y, RIGHT_W)
        y -= 3

    c.setStrokeColor(LINE)
    c.setLineWidth(0.45)
    c.line(RIGHT_X, y - 3, RIGHT_X + RIGHT_W, y - 3)
    return y - 25


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(
        str(OUTPUT),
        pagesize=A4,
        pageCompression=1,
        invariant=1,
    )
    c.setTitle("Salitha Wijerathna - Software Engineer CV")
    c.setAuthor("Salitha Wijerathna")
    c.setSubject("ATS-friendly Software Engineer CV")

    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Blended vector colour washes. Radial PDF shadings keep this image-free.
    c.saveState()
    c.setFillAlpha(0.42)
    c.radialGradient(
        W - 25 * mm,
        H - 15 * mm,
        47 * mm,
        [PINK, PAPER],
        positions=[0, 1],
        extend=False,
    )
    c.setFillAlpha(0.36)
    c.radialGradient(
        W - 2 * mm,
        H - 37 * mm,
        44 * mm,
        [BLUE, PAPER],
        positions=[0, 1],
        extend=False,
    )
    c.restoreState()

    top = H - 18 * mm
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 5.5)
    c.drawString(MARGIN, top, "PORTFOLIO / 2026")

    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 30)
    c.drawString(MARGIN, top - 31, "salitha")
    c.drawString(MARGIN, top - 61, "wijerathna")
    c.setFont("Helvetica-Bold", 8.4)
    c.drawString(MARGIN, top - 82, "software engineer / blockchain / ai / backend")

    summary_y = top - 113
    summary = (
        "Software Engineer specialising in blockchain, AI and backend development. "
        "Experienced in MERN, AWS infrastructure, smart-contract platforms and "
        "delivering scalable technical solutions."
    )
    text_block(c, summary, MARGIN, summary_y, 135 * mm, size=9.1, leading=13)

    divider_y = top - 157
    c.setStrokeColor(LINE)
    c.setLineWidth(0.55)
    c.line(MARGIN, divider_y, W - MARGIN, divider_y)

    content_top = divider_y - 25

    # Left sidebar: ATS-readable skills, education, and contact.
    y = heading(c, "technical skills", MARGIN, content_top, LEFT_W, 14)
    skill_groups = [
        ("backend / web", "JavaScript, TypeScript, Node.js, Express.js, Python, FastAPI, REST, PHP"),
        ("blockchain", "Solidity, Web3.js, Ethers.js, Smart Contracts, Ethereum, EVM, L2, DeFi, Wallet Security"),
        ("ai", "LLMs, RAG, NLP, LangChain, Ollama, OpenAI, Google AI, Amazon Q, MCP, n8n"),
        ("cloud / data", "AWS, CDK, Lambda, Docker, CI/CD, MongoDB, Pinecone, ChromaDB, DynamoDB"),
    ]
    for title, body in skill_groups:
        label(c, title, MARGIN, y)
        y -= 11
        y = text_block(c, body, MARGIN, y, LEFT_W, size=7, leading=9.8, color=MUTED)
        y -= 12

    y = heading(c, "education", MARGIN, y - 2, LEFT_W, 14)
    small(c, "2019-2020", MARGIN, y)
    y -= 13
    y = text_block(
        c,
        "BSc Computer Science and Software Engineering",
        MARGIN,
        y,
        LEFT_W,
        font="Helvetica-Bold",
        size=7.7,
        leading=10.2,
    )
    y -= 2
    y = text_block(c, "University of Bedfordshire", MARGIN, y, LEFT_W, size=7, leading=9.2, color=MUTED)
    y = text_block(c, "First Class Honours", MARGIN, y, LEFT_W, size=7, leading=9.2, color=MUTED)
    y -= 13

    small(c, "2016-2019", MARGIN, y)
    y -= 13
    y = text_block(
        c,
        "Higher Diploma in Information Technology",
        MARGIN,
        y,
        LEFT_W,
        font="Helvetica-Bold",
        size=7.7,
        leading=10.2,
    )
    y -= 2
    y = text_block(c, "SLIIT, Sri Lanka", MARGIN, y, LEFT_W, size=7, leading=9.2, color=MUTED)

    y = heading(c, "contact", MARGIN, y - 13, LEFT_W, 14)
    link(c, "salitha.wijerathna@gmail.com", "mailto:salitha.wijerathna@gmail.com", MARGIN, y)
    y -= 13
    link(c, "+94 71 188 3899", "tel:+94711883899", MARGIN, y)
    y -= 13
    text_block(c, "Kurunegala, Sri Lanka", MARGIN, y, LEFT_W, size=7, leading=9.5)
    y -= 13
    link(c, "kaweendra.is-a.dev", "https://kaweendra.is-a.dev", MARGIN, y)
    y -= 13
    link(c, "linkedin.com/in/kaweendra", "https://linkedin.com/in/kaweendra", MARGIN, y)
    y -= 13
    link(c, "github.com/kaweendras", "https://github.com/kaweendras", MARGIN, y)

    # Right column: experience in reverse chronological order.
    y = heading(c, "experience", RIGHT_X, content_top, RIGHT_W, 14)
    y = job(
        c,
        y,
        "November 2023 - Present",
        "Sydney / Colombo",
        "Senior Software Engineer",
        "XigeniX / Full-Stack Blockchain",
        "https://xigenix.com/",
        "Full-stack blockchain and AI development with AWS, CDK, Lambda, Solidity, Ethers.js and Node.js.",
        [
            "AI Solutions: Developed multi-model natural-language ordering and RAG systems with OpenAI, Ollama, Pinecone and ChromaDB.",
            "SKY AI: Architected a multi-tenant Amazon Q Business assistant with AWS CDK, tool integrations, prompt fine-tuning and evaluation workflows.",
            "MCP Integration: Connected Claude Desktop to internal services and improved tool execution and context handling.",
            "MyCarbon Platform: Delivered an Arbitrum solution with custom smart contracts and Lokblok Toughbox wallet security.",
            "Code Quality Initiative: Led company-wide SonarQube adoption for automated code-quality and security analysis.",
        ],
    )

    y = job(
        c,
        y,
        "June 2021 - November 2023",
        "Seoul / Remote",
        "Software Engineer",
        "Block-Stars Pvt Ltd",
        "https://blockstarsglobal.com/",
        "Built MERN and Web3 products using Web3.js and Solidity; also contributed as Project Lead and supported QA.",
        [
            "K-Culture, NFT Real Estate and Fauna NFT: Delivered full-stack marketplaces with ERC-721/1155 contracts and OpenSea-compatible minting.",
            "Token Generator: Developed ERC-20 token-generation contracts and frontend functionality.",
            "StarApple: Re-engineered MetaMask for Polygon with custom-token support.",
            "Futures-Trading Platform: Built Ebest middleware and automated daily KRX market-data collection.",
            "GREEN P2P: Developed and deployed a containerised Tatum.io custodial wallet with gas-free transactions.",
        ],
    )

    y = job(
        c,
        y,
        "January 2020 - April 2022",
        "Independent / Remote",
        "Freelance Software Engineer",
        "iSotek / Upwork",
        "https://www.upwork.com/",
        "Delivered web, mobile, Web3 and machine-learning solutions using MERN, PHP, Python, Go and Java.",
        [
            "DIG-NFT: Built a decentralised NFT marketplace using the XRP Ledger.",
            "MathBuddy: Developed its Node.js, Express and MongoDB Atlas backend.",
            "Cloth Predictor: Built a Scikit-learn model exposed through FastAPI.",
            "Math Game: Developed an educational Java and MySQL application.",
        ],
    )

    # Footer.
    footer_y = 12 * mm
    c.setStrokeColor(LINE)
    c.line(MARGIN, footer_y + 7, W - MARGIN, footer_y + 7)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 5.5)
    c.drawString(MARGIN, footer_y, "SALITHA WIJERATHNA / SOFTWARE ENGINEER")
    c.drawRightString(W - MARGIN, footer_y, "01 / 01")

    c.showPage()
    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    build()
