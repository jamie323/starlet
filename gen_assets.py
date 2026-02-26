#!/usr/bin/env python3
"""
Generate 10 test dress-up assets as 1024x1024 PNGs with transparent backgrounds.
Character renders at scale 0.68 centered at (512,580) on a 1024x1024 canvas.
Effective character coords (pre-scale space, origin 512,512):
  Head center:  ~(512, 270)
  Hair top:     ~(512, 140)
  Neck:         ~(512, 360)
  Shoulders:    ~(370-654, 400)
  Torso:        y 400-590
  Waist:        ~(512, 590)
  Hips:         ~(512, 630)
  Legs:         y 630-890
  Feet/ankles:  y 870-920
  Hands:        ~(310,570) and ~(714,570)
"""
import os, base64, json
import cairosvg

OUT = os.path.dirname(os.path.abspath(__file__))

def svg_to_png_b64(svg_str, name):
    path = os.path.join(OUT, name)
    cairosvg.svg2png(bytestring=svg_str.encode(), write_to=path, output_width=1024, output_height=1024)
    size = os.path.getsize(path)
    with open(path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    print(f"  ✓ {name} ({size//1024}KB)")
    return f"data:image/png;base64,{b64}"

assets = {
    "outfits": [],
    "hairhats": [],
    "stickers": []
}

# ─── OUTFIT 1: Princess Dress ───────────────────────────────────────────────
svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">
  <!-- Bodice -->
  <path d="M390 400 Q512 380 634 400 L650 590 Q512 610 374 590 Z"
        fill="#E91E8C" stroke="#C0156F" stroke-width="4"/>
  <!-- Neckline trim -->
  <path d="M420 400 Q512 385 604 400" fill="none" stroke="#FFB6D9" stroke-width="6"/>
  <!-- Waist bow -->
  <ellipse cx="460" cy="590" rx="30" ry="12" fill="#FF69B4" stroke="#C0156F" stroke-width="2"/>
  <ellipse cx="564" cy="590" rx="30" ry="12" fill="#FF69B4" stroke="#C0156F" stroke-width="2"/>
  <circle cx="512" cy="590" r="10" fill="#FFD700"/>
  <!-- Skirt layers -->
  <path d="M374 590 Q300 650 260 820 Q350 840 512 845 Q674 840 764 820 Q724 650 650 590 Q512 610 374 590Z"
        fill="#F06292" stroke="#C2185B" stroke-width="3"/>
  <path d="M310 720 Q360 690 512 700 Q664 690 714 720 Q680 800 512 810 Q344 800 310 720Z"
        fill="#F48FB1" stroke="#C2185B" stroke-width="2"/>
  <path d="M330 790 Q420 760 512 768 Q604 760 694 790 Q660 840 512 845 Q364 840 330 790Z"
        fill="#FCE4EC" stroke="#F48FB1" stroke-width="2"/>
  <!-- Star decorations on skirt -->
  <polygon points="450,680 458,668 466,680 480,680 470,690 474,704 460,696 446,704 450,690 440,680"
           fill="#FFD700" opacity="0.8"/>
  <polygon points="570,710 576,700 582,710 594,710 585,718 588,730 576,723 564,730 567,718 558,710"
           fill="#FFD700" opacity="0.8"/>
  <polygon points="480,760 485,752 490,760 500,760 493,767 495,777 485,771 475,777 477,767 470,760"
           fill="#FFD700" opacity="0.6"/>
  <!-- Shoulder straps -->
  <path d="M420 400 Q400 370 380 355 Q370 350 375 360 Q390 380 400 400" fill="#E91E8C" stroke="#C0156F" stroke-width="2"/>
  <path d="M604 400 Q624 370 644 355 Q654 350 649 360 Q634 380 624 400" fill="#E91E8C" stroke="#C0156F" stroke-width="2"/>
</svg>'''
assets["outfits"].append({"id": "outfit_princess", "label": "Princess Dress", "dataUrl": svg_to_png_b64(svg, "outfit_princess.png")})

# ─── OUTFIT 2: Jeans + Colorful Top ─────────────────────────────────────────
svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">
  <!-- Top/shirt body -->
  <path d="M395 400 Q512 382 629 400 L640 590 Q512 608 384 590 Z"
        fill="#FF7043" stroke="#E64A19" stroke-width="4"/>
  <!-- Collar -->
  <path d="M460 400 L512 430 L564 400 Q512 390 460 400Z" fill="#FFE0B2" stroke="#E64A19" stroke-width="2"/>
  <!-- Shirt stripes -->
  <line x1="390" y1="450" x2="634" y2="450" stroke="#FFCC02" stroke-width="8" opacity="0.5"/>
  <line x1="387" y1="500" x2="637" y2="500" stroke="#FFCC02" stroke-width="8" opacity="0.5"/>
  <line x1="385" y1="550" x2="639" y2="550" stroke="#FFCC02" stroke-width="8" opacity="0.5"/>
  <!-- Belt -->
  <rect x="380" y="584" width="264" height="22" rx="4" fill="#5D4037" stroke="#3E2723" stroke-width="2"/>
  <rect x="502" y="584" width="20" height="22" rx="2" fill="#FFD700" stroke="#F9A825" stroke-width="2"/>
  <!-- Jeans waist band -->
  <path d="M378 606 Q512 622 646 606 L650 650 Q512 668 374 650 Z" fill="#1565C0" stroke="#0D47A1" stroke-width="3"/>
  <!-- Left leg -->
  <path d="M374 648 Q360 700 355 820 Q380 840 440 840 Q470 820 478 720 Q490 680 490 648 Z"
        fill="#1976D2" stroke="#0D47A1" stroke-width="3"/>
  <!-- Right leg -->
  <path d="M650 648 Q664 700 669 820 Q644 840 584 840 Q554 820 546 720 Q534 680 534 648 Z"
        fill="#1976D2" stroke="#0D47A1" stroke-width="3"/>
  <!-- Jeans center seam -->
  <path d="M512 650 Q510 710 512 780" fill="none" stroke="#0D47A1" stroke-width="3"/>
  <!-- Pocket stitching -->
  <path d="M400 665 Q415 660 430 665 L428 700 Q415 705 402 700 Z" fill="none" stroke="#42A5F5" stroke-width="2"/>
  <path d="M594 665 Q609 660 624 665 L622 700 Q609 705 596 700 Z" fill="none" stroke="#42A5F5" stroke-width="2"/>
  <!-- Jean cuffs -->
  <path d="M355 818 Q380 842 442 842 L440 828 Q410 828 356 806Z" fill="#1565C0" stroke="#0D47A1" stroke-width="2"/>
  <path d="M669 818 Q644 842 582 842 L584 828 Q614 828 668 806Z" fill="#1565C0" stroke="#0D47A1" stroke-width="2"/>
</svg>'''
assets["outfits"].append({"id": "outfit_jeans", "label": "Jeans & Top", "dataUrl": svg_to_png_b64(svg, "outfit_jeans.png")})

# ─── OUTFIT 3: Ballet Leotard + Tutu ─────────────────────────────────────────
svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">
  <!-- Leotard body -->
  <path d="M415 385 Q512 368 609 385 L618 560 Q512 575 406 560 Z"
        fill="#F8BBD0" stroke="#F06292" stroke-width="4"/>
  <!-- V-neck detail -->
  <path d="M460 388 L512 425 L564 388" fill="none" stroke="#F06292" stroke-width="4"/>
  <!-- Waist join -->
  <ellipse cx="512" cy="565" rx="106" ry="12" fill="#F48FB1"/>
  <!-- Tutu base -->
  <ellipse cx="512" cy="575" rx="160" ry="18" fill="#F06292" stroke="#E91E63" stroke-width="2"/>
  <!-- Tutu layers - multiple overlapping ellipses for fluffy effect -->
  <path d="M352 575 Q420 530 512 525 Q604 530 672 575 Q640 610 512 618 Q384 610 352 575Z"
        fill="#FCE4EC" stroke="#F48FB1" stroke-width="1" opacity="0.9"/>
  <path d="M332 585 Q400 540 512 535 Q624 540 692 585 Q660 625 512 635 Q364 625 332 585Z"
        fill="#F8BBD0" stroke="#F48FB1" stroke-width="1" opacity="0.85"/>
  <path d="M318 596 Q390 548 512 542 Q634 548 706 596 Q672 640 512 652 Q352 640 318 596Z"
        fill="#FCE4EC" stroke="#F06292" stroke-width="1" opacity="0.8"/>
  <path d="M310 608 Q384 558 512 552 Q640 558 714 608 Q678 655 512 668 Q346 655 310 608Z"
        fill="#F48FB1" stroke="#E91E63" stroke-width="1" opacity="0.7"/>
  <!-- Ballet tights on legs -->
  <path d="M440 560 Q430 650 428 820 Q450 835 480 830 Q494 720 500 620 Q508 590 512 575 Q516 590 524 620 Q530 720 544 830 Q574 835 596 820 Q594 650 584 560 Q512 578 440 560Z"
        fill="#FFCCBC" stroke="#FFAB91" stroke-width="2"/>
  <!-- Shoulder straps -->
  <line x1="450" y1="388" x2="434" y2="368" stroke="#F06292" stroke-width="7" stroke-linecap="round"/>
  <line x1="574" y1="388" x2="590" y2="368" stroke="#F06292" stroke-width="7" stroke-linecap="round"/>
  <!-- Sparkle on tutu -->
  <circle cx="420" cy="600" r="4" fill="#FFD700"/>
  <circle cx="512" cy="585" r="4" fill="#FFD700"/>
  <circle cx="604" cy="600" r="4" fill="#FFD700"/>
  <circle cx="466" cy="625" r="3" fill="#FFD700"/>
  <circle cx="558" cy="625" r="3" fill="#FFD700"/>
</svg>'''
assets["outfits"].append({"id": "outfit_ballet", "label": "Ballet Tutu", "dataUrl": svg_to_png_b64(svg, "outfit_ballet.png")})

# ─── HAIR 1: Long Blonde ─────────────────────────────────────────────────────
svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">
  <!-- Back hair (behind head) -->
  <path d="M370 245 Q330 320 310 450 Q305 580 315 700 Q330 780 345 830 Q360 810 368 760 Q372 680 375 580 Q378 460 385 370 Z"
        fill="#F9A825" stroke="#F57F17" stroke-width="2"/>
  <path d="M654 245 Q694 320 714 450 Q719 580 709 700 Q694 780 679 830 Q664 810 656 760 Q652 680 649 580 Q646 460 639 370 Z"
        fill="#F9A825" stroke="#F57F17" stroke-width="2"/>
  <!-- Head cap of hair -->
  <ellipse cx="512" cy="245" rx="158" ry="118" fill="#FDD835" stroke="#F9A825" stroke-width="3"/>
  <!-- Hair highlight -->
  <path d="M420 175 Q512 155 600 175 Q570 200 512 205 Q454 200 420 175Z" fill="#FFF9C4" opacity="0.6"/>
  <!-- Side hair flowing -->
  <path d="M360 290 Q335 380 330 500 Q328 600 338 700 Q348 760 355 810 Q342 805 330 770 Q308 690 305 580 Q302 440 325 320 Q338 270 360 250 Z"
        fill="#FDD835" stroke="#F9A825" stroke-width="2"/>
  <path d="M664 290 Q689 380 694 500 Q696 600 686 700 Q676 760 669 810 Q682 805 694 770 Q716 690 719 580 Q722 440 699 320 Q686 270 664 250 Z"
        fill="#FDD835" stroke="#F9A825" stroke-width="2"/>
  <!-- Strand details -->
  <path d="M345 400 Q340 500 345 600 Q350 680 355 750" fill="none" stroke="#F57F17" stroke-width="2" opacity="0.4"/>
  <path d="M679 400 Q684 500 679 600 Q674 680 669 750" fill="none" stroke="#F57F17" stroke-width="2" opacity="0.4"/>
  <!-- Fringe/bangs -->
  <path d="M400 195 Q440 230 480 235 Q510 238 512 238 Q514 238 544 235 Q584 230 624 195 Q590 180 512 175 Q434 180 400 195Z"
        fill="#FDD835" stroke="#F9A825" stroke-width="2"/>
  <!-- Hair tie/band at crown -->
  <ellipse cx="512" cy="172" rx="40" ry="16" fill="#FF69B4" stroke="#E91E63" stroke-width="2"/>
  <!-- Bow on top -->
  <path d="M472 160 Q490 145 512 155 Q534 145 552 160 Q534 172 512 168 Q490 172 472 160Z" fill="#FF69B4" stroke="#E91E63" stroke-width="2"/>
</svg>'''
assets["hairhats"].append({"id": "hair_long_blonde", "label": "Long Blonde", "dataUrl": svg_to_png_b64(svg, "hair_long_blonde.png")})

# ─── HAIR 2: Brown Bun ───────────────────────────────────────────────────────
svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">
  <!-- Main head cap -->
  <ellipse cx="512" cy="258" rx="155" ry="115" fill="#6D4C41" stroke="#4E342E" stroke-width="3"/>
  <!-- Hair highlight -->
  <path d="M425 185 Q512 168 600 185 Q575 205 512 210 Q449 205 425 185Z" fill="#A1887F" opacity="0.5"/>
  <!-- Side hair (short, updo) -->
  <path d="M358 285 Q342 330 345 390 Q350 430 362 450 Q375 430 380 390 Q385 340 382 288 Z"
        fill="#5D4037" stroke="#4E342E" stroke-width="2"/>
  <path d="M666 285 Q682 330 679 390 Q674 430 662 450 Q649 430 644 390 Q639 340 642 288 Z"
        fill="#5D4037" stroke="#4E342E" stroke-width="2"/>
  <!-- Bun on top -->
  <ellipse cx="512" cy="152" rx="62" ry="52" fill="#795548" stroke="#4E342E" stroke-width="3"/>
  <ellipse cx="512" cy="148" rx="55" ry="46" fill="#8D6E63" stroke="#5D4037" stroke-width="2"/>
  <!-- Bun spiral detail -->
  <path d="M480 145 Q512 130 544 145 Q544 165 512 168 Q480 165 480 145Z" fill="#A1887F" opacity="0.5"/>
  <!-- Bun texture lines -->
  <path d="M465 150 Q512 138 559 150" fill="none" stroke="#4E342E" stroke-width="1.5" opacity="0.4"/>
  <path d="M462 162 Q512 148 562 162" fill="none" stroke="#4E342E" stroke-width="1.5" opacity="0.4"/>
  <!-- Hair pins -->
  <line x1="490" y1="125" x2="496" y2="148" stroke="#FFD700" stroke-width="3" stroke-linecap="round"/>
  <line x1="534" y1="125" x2="528" y2="148" stroke="#FFD700" stroke-width="3" stroke-linecap="round"/>
  <!-- Fringe/bangs -->
  <path d="M400 200 Q440 238 480 242 Q512 245 544 242 Q584 238 624 200 Q590 185 512 180 Q434 185 400 200Z"
        fill="#6D4C41" stroke="#4E342E" stroke-width="2"/>
  <!-- Wispy strands around bun -->
  <path d="M455 135 Q448 120 452 108" fill="none" stroke="#6D4C41" stroke-width="2" stroke-linecap="round"/>
  <path d="M569 135 Q576 120 572 108" fill="none" stroke="#6D4C41" stroke-width="2" stroke-linecap="round"/>
  <path d="M512 102 Q508 90 512 80" fill="none" stroke="#6D4C41" stroke-width="2" stroke-linecap="round"/>
</svg>'''
assets["hairhats"].append({"id": "hair_bun_brown", "label": "Brown Bun", "dataUrl": svg_to_png_b64(svg, "hair_bun_brown.png")})

# ─── HAIR 3: Crown/Tiara ─────────────────────────────────────────────────────
svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">
  <!-- Crown band -->
  <path d="M380 215 L380 248 Q512 260 644 248 L644 215 Q512 200 380 215Z"
        fill="#FFD700" stroke="#F9A825" stroke-width="3"/>
  <!-- Crown points -->
  <polygon points="380,218 360,160 400,200" fill="#FFD700" stroke="#F9A825" stroke-width="2"/>
  <polygon points="440,210 430,145 460,198" fill="#FFD700" stroke="#F9A825" stroke-width="2"/>
  <polygon points="512,206 512,132 540,200" fill="#FFD700" stroke="#F9A825" stroke-width="2"/>
  <polygon points="584,210 594,145 564,198" fill="#FFD700" stroke="#F9A825" stroke-width="2"/>
  <polygon points="644,218 664,160 624,200" fill="#FFD700" stroke="#F9A825" stroke-width="2"/>
  <!-- Gem in center point -->
  <ellipse cx="512" cy="152" rx="14" ry="10" fill="#E91E63" stroke="#C2185B" stroke-width="2"/>
  <ellipse cx="512" cy="150" rx="8" ry="6" fill="#FF80AB" opacity="0.7"/>
  <!-- Side gems -->
  <circle cx="437" cy="165" r="8" fill="#7C4DFF" stroke="#651FFF" stroke-width="1.5"/>
  <circle cx="587" cy="165" r="8" fill="#7C4DFF" stroke="#651FFF" stroke-width="1.5"/>
  <!-- Band gems -->
  <circle cx="420" cy="232" r="7" fill="#00BCD4" stroke="#0097A7" stroke-width="1.5"/>
  <circle cx="512" cy="228" r="9" fill="#E91E63" stroke="#C2185B" stroke-width="1.5"/>
  <circle cx="604" cy="232" r="7" fill="#00BCD4" stroke="#0097A7" stroke-width="1.5"/>
  <!-- Band shimmer -->
  <path d="M382 220 Q512 210 642 220" fill="none" stroke="#FFF9C4" stroke-width="2" opacity="0.6"/>
</svg>'''
assets["hairhats"].append({"id": "hair_crown", "label": "Princess Crown", "dataUrl": svg_to_png_b64(svg, "hair_crown.png")})

# ─── STICKER 1: Gold Star ────────────────────────────────────────────────────
svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">
  <!-- Outer glow -->
  <circle cx="512" cy="512" r="220" fill="#FFD700" opacity="0.15"/>
  <!-- Star shape -->
  <polygon points="512,292 560,430 710,430 592,514 638,655 512,572 386,655 432,514 314,430 464,430"
           fill="#FFD700" stroke="#FF8F00" stroke-width="6"/>
  <!-- Inner star highlight -->
  <polygon points="512,330 548,435 660,435 574,498 606,604 512,542 418,604 450,498 364,435 476,435"
           fill="#FFF176" opacity="0.7"/>
  <!-- Center sparkle -->
  <circle cx="512" cy="512" r="30" fill="#FFFFFF" opacity="0.4"/>
  <!-- Sparkle rays -->
  <line x1="512" y1="340" x2="512" y2="380" stroke="#FFFFFF" stroke-width="4" opacity="0.6"/>
  <line x1="512" y1="644" x2="512" y2="684" stroke="#FFFFFF" stroke-width="4" opacity="0.6"/>
  <line x1="340" y1="512" x2="380" y2="512" stroke="#FFFFFF" stroke-width="4" opacity="0.6"/>
  <line x1="644" y1="512" x2="684" y2="512" stroke="#FFFFFF" stroke-width="4" opacity="0.6"/>
</svg>'''
assets["stickers"].append({"id": "sticker_star", "label": "Gold Star", "dataUrl": svg_to_png_b64(svg, "sticker_star.png")})

# ─── STICKER 2: Heart ────────────────────────────────────────────────────────
svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">
  <!-- Glow -->
  <ellipse cx="512" cy="520" rx="240" ry="220" fill="#FF69B4" opacity="0.12"/>
  <!-- Heart -->
  <path d="M512 690 Q360 580 300 480 Q260 400 300 330 Q340 260 420 280 Q470 295 512 350 Q554 295 604 280 Q684 260 724 330 Q764 400 724 480 Q664 580 512 690Z"
        fill="#FF1744" stroke="#C62828" stroke-width="5"/>
  <!-- Highlight -->
  <path d="M380 320 Q410 295 450 305 Q460 330 440 345 Q410 340 380 320Z" fill="#FFFFFF" opacity="0.35"/>
  <!-- Shimmer dots -->
  <circle cx="580" cy="340" r="8" fill="#FFFFFF" opacity="0.4"/>
  <circle cx="600" cy="380" r="5" fill="#FFFFFF" opacity="0.3"/>
</svg>'''
assets["stickers"].append({"id": "sticker_heart", "label": "Pink Heart", "dataUrl": svg_to_png_b64(svg, "sticker_heart.png")})

# ─── STICKER 3: Rainbow ──────────────────────────────────────────────────────
svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">
  <!-- Rainbow arcs -->
  <path d="M180 640 Q180 300 512 300 Q844 300 844 640" fill="none" stroke="#FF1744" stroke-width="32"/>
  <path d="M212 640 Q212 332 512 332 Q812 332 812 640" fill="none" stroke="#FF9800" stroke-width="32"/>
  <path d="M244 640 Q244 364 512 364 Q780 364 780 640" fill="none" stroke="#FFEB3B" stroke-width="32"/>
  <path d="M276 640 Q276 396 512 396 Q748 396 748 640" fill="none" stroke="#4CAF50" stroke-width="32"/>
  <path d="M308 640 Q308 428 512 428 Q716 428 716 640" fill="none" stroke="#2196F3" stroke-width="32"/>
  <path d="M340 640 Q340 460 512 460 Q684 460 684 640" fill="none" stroke="#9C27B0" stroke-width="32"/>
  <!-- Clouds at base -->
  <ellipse cx="200" cy="640" rx="70" ry="50" fill="white"/>
  <ellipse cx="155" cy="648" rx="50" ry="38" fill="white"/>
  <ellipse cx="250" cy="650" rx="50" ry="36" fill="white"/>
  <ellipse cx="824" cy="640" rx="70" ry="50" fill="white"/>
  <ellipse cx="869" cy="648" rx="50" ry="38" fill="white"/>
  <ellipse cx="774" cy="650" rx="50" ry="36" fill="white"/>
</svg>'''
assets["stickers"].append({"id": "sticker_rainbow", "label": "Rainbow", "dataUrl": svg_to_png_b64(svg, "sticker_rainbow.png")})

print("\nAll assets generated. Now injecting into game JSON...")

# ─── LOAD + MERGE EXISTING JSON ──────────────────────────────────────────────
merged = {}
for i in range(1, 5):
    fname = os.path.join(OUT, f'starlet-v6-part{i}.json')
    with open(fname) as f:
        data = json.load(f)
    if i == 1:
        base = dict(data)  # keep all metadata from part1
    if 'assets' in data:
        for k, v in data['assets'].items():
            merged.setdefault(k, []).extend(v)

# Add new assets to merged
for cat, items in assets.items():
    merged.setdefault(cat, []).extend(items)

base['assets'] = merged

# Write merged output
out_path = os.path.join(OUT, 'starlet-v6-merged.json')
with open(out_path, 'w') as f:
    json.dump(base, f, separators=(',', ':'))

size_mb = os.path.getsize(out_path) / 1024 / 1024
print(f"\n✅ Written: starlet-v6-merged.json ({size_mb:.1f}MB)")
print("\nAsset summary:")
for cat, items in merged.items():
    print(f"  {cat}: {len(items)} items")
print("\nNew assets added:")
for cat, items in assets.items():
    for item in items:
        print(f"  [{cat}] {item['label']}")
