#!/usr/bin/env python3
"""Inject 2 vibrant 3D-render Unsplash images into each blog post article-content."""
import os, re

POSTS_DIR = "/Volumes/ORICO/Claude/blog/posts"

# 15 real photo IDs scraped from unsplash.com/t/3d-renders
PHOTOS = [
    "photo-1776053473082-9520f829fbbb",  # 0
    "photo-1771230825735-d1f8005f0f38",  # 1
    "photo-1778393719064-609772896849",  # 2
    "photo-1778351983804-e1e267d1f94c",  # 3
    "photo-1777877714035-57392b1c99c4",  # 4
    "photo-1742717817785-54249562494c",  # 5
    "photo-1775887134611-d856f03b6edd",  # 6
    "photo-1777646346045-df4bd1114148",  # 7
    "photo-1777971911576-de6d56a93681",  # 8
    "photo-1752509929361-4471bdb102cf",  # 9
    "photo-1770723963625-77f54ed8086a",  # 10
    "photo-1771942202908-6ce86ef73701",  # 11
    "photo-1773681907553-15070fd7f8f7",  # 12
    "photo-1713640774386-86b5f18972f3",  # 13
    "photo-1687560466164-1eeddb3b119b",  # 14
]

# 2 unique photos per post, staggered so no two adjacent posts share an image
ASSIGNMENTS = {
    "autoquant.html":                        (0,  5),
    "claude-code-retrospective.html":        (1,  6),
    "ai-first-outreach.html":                (2,  7),
    "13-agents-one-saturday.html":           (3,  8),
    "ai-sales-stack-2026.html":              (4,  9),
    "ai-trends-2026-breakthrough-idea.html": (10, 0),
    "club-winner.html":                      (11, 1),
    "compounding-systems.html":              (12, 2),
    "five-vault-fixes.html":                 (13, 3),
    "llm-knowledge-base-obsidian.html":      (14, 4),
    "nvidia-data-center-guide.html":         (5, 10),
    "obsidian-vault.html":                   (6, 11),
    "portfolio-monitor.html":                (7, 12),
    "renamed-seven-agents.html":             (8, 13),
    "win-rate-trap.html":                    (9, 14),
}

# Labels that match each post's vibe (same order as ASSIGNMENTS)
LABELS = {
    "autoquant.html":                        ("3D Signal Architecture", "Market Regime Render"),
    "claude-code-retrospective.html":        ("Code System 3D", "Engineering Volume"),
    "ai-first-outreach.html":                ("Outreach Pipeline 3D", "Connection Render"),
    "13-agents-one-saturday.html":           ("Agent Network 3D", "Multi-System Render"),
    "ai-sales-stack-2026.html":              ("Sales Stack Render", "Pipeline Architecture"),
    "ai-trends-2026-breakthrough-idea.html": ("Breakthrough 3D", "Signal Horizon"),
    "club-winner.html":                      ("Trade Geometry", "Win Structure 3D"),
    "compounding-systems.html":              ("Growth System 3D", "Compound Render"),
    "five-vault-fixes.html":                 ("Vault Architecture", "System Render"),
    "llm-knowledge-base-obsidian.html":      ("Knowledge Graph 3D", "LLM Topology"),
    "nvidia-data-center-guide.html":         ("Data Center Render", "GPU Architecture"),
    "obsidian-vault.html":                   ("Graph Topology 3D", "Knowledge Render"),
    "portfolio-monitor.html":                ("Portfolio 3D", "Monitor Render"),
    "renamed-seven-agents.html":             ("Agent Persona Render", "System Architecture"),
    "win-rate-trap.html":                    ("Probability 3D", "Risk Geometry"),
}

IMG_TPL = """\n<figure class="article-img-break">
  <img class="article-img-break__img"
       src="https://images.unsplash.com/{photo}?w=1200&q=90&auto=format&fit=crop"
       alt="{label}" loading="lazy">
  <figcaption class="article-img-break__label">{label}</figcaption>
</figure>\n"""

def inject(filename, idx1, idx2, label1, label2):
    path = os.path.join(POSTS_DIR, filename)
    with open(path, encoding="utf-8") as f:
        content = f.read()

    if "article-img-break" in content:
        print(f"SKIP (already has img-breaks): {filename}")
        return

    # Find article-content div start
    ac_start = content.find('<div class="article-content">')
    if ac_start == -1:
        print(f"SKIP (no article-content): {filename}")
        return

    # Collect all <h2 positions within article-content
    h2_positions = []
    pos = ac_start
    while True:
        p = content.find("<h2 ", pos)
        if p == -1:
            break
        h2_positions.append(p)
        pos = p + 1

    n = len(h2_positions)
    if n < 2:
        print(f"SKIP (only {n} h2 tags): {filename}")
        return

    img1 = IMG_TPL.format(photo=PHOTOS[idx1], label=label1)
    img2 = IMG_TPL.format(photo=PHOTOS[idx2], label=label2)

    # Insert LATER position first (avoids shifting earlier position)
    # Image 2: before 4th h2 (index 3) or last h2
    pos2 = h2_positions[min(3, n - 1)]
    # Image 1: before 2nd h2 (index 1)
    pos1 = h2_positions[1]

    # Inject img2 first (later in document), then img1 (earlier)
    content = content[:pos2] + img2 + content[pos2:]
    content = content[:pos1] + img1 + content[pos1:]

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"OK: {filename}")

for fname, (i1, i2) in ASSIGNMENTS.items():
    l1, l2 = LABELS[fname]
    inject(fname, i1, i2, l1, l2)

print("\nDone.")
