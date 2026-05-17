#!/usr/bin/env python3
"""
Fix broken /nvidia-images/ paths in og:image, twitter:image, and JSON-LD image
meta tags across all posts. Uses the post's first PSH hero photo as the OG image.
"""
import os, re, glob

POSTS_DIR = "/Volumes/ORICO/Claude/blog/posts"

# Fallback OG photo (datacenter overhead) if no PSH photo found
FALLBACK = "https://images.unsplash.com/photo-1715026323215-a2dbb71272f6?w=1200&q=90&auto=format&fit=crop"

def fix_post(filepath):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    if "nvidia-images" not in content:
        return False

    # Extract first PSH hero photo URL
    psh_match = re.search(r'class="psh-photo psh-p1"[^>]*src="([^"]+)"', content)
    og_url = psh_match.group(1) if psh_match else FALLBACK
    # Strip query params and add clean OG params (1200px wide)
    base = og_url.split("?")[0]
    og_img = f"{base}?w=1200&q=90&auto=format&fit=crop"

    changed = False

    # Fix og:image
    def fix_og(m):
        nonlocal changed
        changed = True
        return f'<meta property="og:image" content="{og_img}" />'
    content = re.sub(r'<meta property="og:image" content="[^"]*nvidia-images[^"]*"\s*/>', fix_og, content)

    # Fix twitter:image
    def fix_tw(m):
        nonlocal changed
        changed = True
        return f'<meta name="twitter:image" content="{og_img}" />'
    content = re.sub(r'<meta name="twitter:image" content="[^"]*nvidia-images[^"]*"\s*/>', fix_tw, content)

    # Fix JSON-LD "image"
    def fix_jld(m):
        nonlocal changed
        changed = True
        return f'"image": "{og_img}",'
    content = re.sub(r'"image":\s*"[^"]*nvidia-images[^"]*",', fix_jld, content)

    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        # Verify no nvidia-images remain
        remaining = content.count("nvidia-images")
        print(f"FIXED: {os.path.basename(filepath)} (remaining nvidia refs: {remaining})")
    return changed

total = 0
for filepath in sorted(glob.glob(os.path.join(POSTS_DIR, "*.html"))):
    if fix_post(filepath):
        total += 1

print(f"\nDone. Fixed {total} posts.")
