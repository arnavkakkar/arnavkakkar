#!/usr/bin/env python3
import sys, os, html

OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "wordmark.svg")

ASCII_ART = [
    "  █▀▀█  █▀▀█  █▄  █  █▀▀█  █  █",
    "  █▄▄█  █▄▄▀  █ █ █  █▄▄█  ▀▄▄▀",
    "  █  █  █  █  █  ▀█  █  █    ██"
]

CANVAS_W, CANVAS_H, PAD, TITLEBAR_H = 860, 260, 20, 32
BG, BG2, FRAME, MUTED = "#0a0e14", "#0d1420", "#1f6feb", "#7d8590"
TEXT, ACCENT, GREEN = "#e6edf3", "#22d3ee", "#39d353"

svg_parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<defs>',
    f'<linearGradient id="wbg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient>',
    '</defs>',
    f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#wbg)"/>',
    f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1" stroke-opacity="0.55"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}" stroke-opacity="0.35"/>',
]

for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    svg_parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dot}"/>')

svg_parts.append(f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" text-anchor="middle">arnavkakkar@github: ~$ neofetch</text>')

y_offset = 65
for idx, line in enumerate(ASCII_ART):
    y = y_offset + idx * 30
    svg_parts.append(f'<text x="20" y="{y}" fill="{ACCENT}" font-size="18" font-weight="bold" xml:space="preserve">{html.escape(line)}</text>')

info_x = 430
info_items = [
    ("OS", "macOS", GREEN),
    ("Host", "MacBook Air", TEXT),
    ("Role", "Software Developer & Data Scientist", ACCENT),
    ("Languages", "Python, JavaScript, SQL, Jupyter", TEXT),
    ("Focus", "Data Science & Software Engineering", GREEN),
    ("Status", "Building open-source software on GitHub 🚀", TEXT)
]

info_y = 65
for label, val, color in info_items:
    svg_parts.append(f'<text x="{info_x}" y="{info_y}" font-size="13"><tspan fill="{MUTED}" font-weight="bold">{label}: </tspan><tspan fill="{color}">{html.escape(val)}</tspan></text>')
    info_y += 26

svg_parts.append('</svg>')

svg_code = "".join(svg_parts)
with open(OUT_PATH, "w") as f:
    f.write(svg_code)

print(f"Generated {OUT_PATH} successfully!")
