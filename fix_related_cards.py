#!/usr/bin/env python3
"""
Fix related-post-card images across all 15 posts:
1. Replace broken /nvidia-images/ paths with Unsplash datacenter photos
2. Add class="related-post-card__image" so CSS aspect-ratio applies
3. Also fix any other inline /nvidia-images/ in article bodies
"""
import os, re, glob

POSTS_DIR = "/Volumes/ORICO/Claude/blog/posts"

# Real datacenter photos scraped from unsplash.com/s/photos/datacenter
DC_PHOTOS = [
    "photo-1558494949-ef010cbdcc31",  # server rows, dramatic blue
    "photo-1580106815433-a5b1d1d53d85",  # clean server room
    "photo-1488229297570-58520851e868",  # data center corridor
    "photo-1715026323215-a2dbb71272f6",  # modern data center
    "photo-1573164713988-8665fc963095",  # server rack close-up
    "photo-1504384308090-c894fdcc538d",  # computer lab rows
    "photo-1683322499436-f4383dd59f5a",  # server room blue light
    "photo-1579274216947-86eaa4b00475",  # network equipment
    "photo-1506399558188-acca6f8cbf41",  # data center aisle
    "photo-1650327034350-08e408a8f902",  # modern server room
    "photo-1695668548342-c0c1ad479aee",  # data center overhead
]

def dc_url(photo, w=800):
    return f"https://images.unsplash.com/{photo}?w={w}&q=90&auto=format&fit=crop"

def fix_post(filepath, dc_idx):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    changed = False

    # ── 1. Fix related-post-card <img> tags ──────────────────────
    # Pattern: inside an <a class="related-post-card"...> block, find the first <img>
    # We'll process the whole file and fix each related-post-card block

    def fix_card_img(m):
        nonlocal dc_idx, changed
        block = m.group(0)

        # Find the img tag within this card
        img_match = re.search(r'<img\s[^>]*>', block)
        if not img_match:
            return block

        img_tag = img_match.group(0)
        photo = DC_PHOTOS[dc_idx % len(DC_PHOTOS)]
        dc_idx += 1
        new_src = dc_url(photo)

        # Build clean img tag with proper class and new src
        # Preserve alt text if it has real content
        alt_match = re.search(r'alt="([^"]*)"', img_tag)
        alt = alt_match.group(1) if alt_match else ""

        new_img = f'<img class="related-post-card__image" src="{new_src}" alt="{alt}" loading="lazy">'
        new_block = block[:img_match.start()] + new_img + block[img_match.end():]
        changed = True
        return new_block

    # Match each related-post-card anchor block (non-greedy)
    content = re.sub(
        r'<a\s+class="related-post-card"[^>]*>.*?</a>',
        fix_card_img,
        content,
        flags=re.DOTALL
    )

    # ── 2. Fix any remaining /nvidia-images/ src in article body ──
    # Replace with datacenter photos (preserving inline styles if present)
    def fix_nvidia_img(m):
        nonlocal dc_idx, changed
        tag = m.group(0)
        photo = DC_PHOTOS[dc_idx % len(DC_PHOTOS)]
        dc_idx += 1
        new_tag = re.sub(r'src="[^"]*nvidia-images[^"]*"', f'src="{dc_url(photo, w=1400)}"', tag)
        changed = True
        return new_tag

    content = re.sub(
        r'<img\s[^>]*src="[^"]*nvidia-images[^"]*"[^>]*>',
        fix_nvidia_img,
        content,
        flags=re.DOTALL
    )

    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"FIXED: {os.path.basename(filepath)}")
    else:
        print(f"CLEAN: {os.path.basename(filepath)}")

    return dc_idx

dc_idx = 0
for filepath in sorted(glob.glob(os.path.join(POSTS_DIR, "*.html"))):
    dc_idx = fix_post(filepath, dc_idx)

print(f"\nDone. Used {dc_idx} datacenter photo slots.")
