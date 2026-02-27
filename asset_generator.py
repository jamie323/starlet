#!/usr/bin/env python3
"""Generate quick placeholder dress-up assets as SVGs and convert to PNG."""
import base64
import json
import math
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Callable, Dict, Tuple
from xml.etree.ElementTree import Element, SubElement, tostring

WIDTH = HEIGHT = 1024
ROOT = Path(__file__).parent
PNG_DIR = ROOT / 'generated_assets'
SVG_DIR = PNG_DIR / 'svg'
for d in (PNG_DIR, SVG_DIR):
    d.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# SVG HELPERS
# ------------------------------------------------------------

def new_svg():
    svg = Element('svg', {
        'xmlns': 'http://www.w3.org/2000/svg',
        'width': str(WIDTH),
        'height': str(HEIGHT),
        'viewBox': '0 0 1024 1024'
    })
    defs = SubElement(svg, 'defs')
    return svg, defs


def add(parent: Element, tag: str, **attrs) -> Element:
    clean = {k: str(v) for k, v in attrs.items() if v is not None}
    return SubElement(parent, tag, clean)


def add_linear_gradient(defs: Element, grad_id: str, stops):
    lg = add(defs, 'linearGradient', id=grad_id, x1='0%', y1='0%', x2='0%', y2='100%')
    for offset, color, opacity in stops:
        add(lg, 'stop', offset=f'{offset}%', style=f'stop-color:{color};stop-opacity:{opacity}')
    return f'url(#{grad_id})'


def add_radial_gradient(defs: Element, grad_id: str, stops):
    rg = add(defs, 'radialGradient', id=grad_id, cx='50%', cy='50%', r='50%')
    for offset, color, opacity in stops:
        add(rg, 'stop', offset=f'{offset}%', style=f'stop-color:{color};stop-opacity:{opacity}')
    return f'url(#{grad_id})'


# ------------------------------------------------------------
# SHAPE BUILDERS
# ------------------------------------------------------------

def build_princess(svg, defs):
    grp = add(svg, 'g')
    skirt_grad = add_linear_gradient(defs, 'princessSkirt', [
        (0, '#ffb3f2', 1),
        (50, '#f36dd5', 1),
        (100, '#bf5fff', 1)
    ])
    bodice_grad = add_linear_gradient(defs, 'princessBodice', [
        (0, '#ffd1fb', 1),
        (100, '#e05cd6', 1)
    ])
    add(grp, 'path', d='M390 350 C420 300 604 300 634 350 L664 530 C590 560 442 560 370 530 Z', fill=bodice_grad)
    add(grp, 'rect', x=470, y=330, width=84, height=50, rx=26, fill='#ffe5ff', opacity='0.85')
    add(grp, 'circle', cx=512, cy=385, r=18, fill='#ffdcdc')
    add(grp, 'path', d='M320 520 C 280 700 300 880 360 930 L 664 930 C 716 864 734 688 702 520 Z', fill=skirt_grad)
    for i, offset in enumerate([0, 40, 80]):
        add(grp, 'path', d=f'M340 {600+offset} C 360 {560+offset} 664 {560+offset} 684 {600+offset} L 682 {640+offset} C 620 {700+offset} 404 {700+offset} 342 {640+offset} Z',
            fill='rgba(255,255,255,0.22)')
    for heart_x in range(360, 680, 60):
        add(grp, 'path', d=f'M{heart_x} 720 C {heart_x-30} 690 {heart_x-10} 650 {heart_x} 660 C {heart_x+10} 650 {heart_x+30} 690 {heart_x} 720 Z', fill='rgba(255,255,255,0.35)')
    add(grp, 'ellipse', cx=512, cy=540, rx=130, ry=26, fill='rgba(255,255,255,0.4)')


def build_jeans(svg, defs):
    grp = add(svg, 'g')
    top_grad = add_linear_gradient(defs, 'topGradient', [
        (0, '#ffde7d', 1),
        (50, '#ff8fb1', 1),
        (100, '#ff66a6', 1)
    ])
    add(grp, 'path', d='M400 360 C 430 320 594 320 624 360 L 640 520 C 576 540 448 540 384 520 Z', fill=top_grad)
    add(grp, 'path', d='M384 520 L 640 520 L 664 860 C 636 900 386 900 358 860 Z', fill='#3a6ba5')
    add(grp, 'rect', x=380, y=520, width=264, height=40, rx=18, fill='#2a4f7a')
    belt_grad = add_linear_gradient(defs, 'beltGrad', [
        (0, '#ffe082', 1),
        (100, '#fbc02d', 1)
    ])
    add(grp, 'rect', x=388, y=520, width=248, height=22, rx=12, fill=belt_grad)
    add(grp, 'circle', cx=512, cy=534, r=12, fill='#d172c2')
    for i in range(4):
        add(grp, 'rect', x=410+i*60, y=574, width=28, height=90, rx=14, fill='rgba(255,255,255,0.2)')
    add(grp, 'path', d='M380 520 L 360 860 C 380 900 644 900 664 860 L 640 520 Z', fill='none', stroke='rgba(255,255,255,0.15)', **{'stroke-width': 6})
    add(grp, 'circle', cx=430, cy=410, r=18, fill='#fff')
    add(grp, 'circle', cx=470, cy=400, r=12, fill='#ffd54f')
    add(grp, 'circle', cx=610, cy=400, r=14, fill='#64b5f6')


def build_ballet(svg, defs):
    grp = add(svg, 'g')
    leo_grad = add_linear_gradient(defs, 'balletLeo', [
        (0, '#ffd1e8', 1),
        (100, '#ff85c1', 1)
    ])
    add(grp, 'path', d='M420 360 C 440 320 584 320 604 360 L 620 560 C 560 600 464 600 404 560 Z', fill=leo_grad)
    tutu_grad = add_radial_gradient(defs, 'balletTutu', [
        (0, '#ffe6f3', 1),
        (70, '#ff9bcf', 0.9),
        (100, '#ff6fb4', 0.8)
    ])
    add(grp, 'path', d='M340 600 C 320 700 340 840 512 860 C 684 840 704 700 684 600 Z', fill=tutu_grad, opacity='0.92')
    for angle in range(0, 360, 12):
        length = 160 + 20 * math.sin(math.radians(angle*2))
        x1 = 512 + 10 * math.cos(math.radians(angle))
        y1 = 620 + 10 * math.sin(math.radians(angle))
        x2 = 512 + length * math.cos(math.radians(angle))
        y2 = 620 + length * math.sin(math.radians(angle))
        add(grp, 'line', x1=x1, y1=y1, x2=x2, y2=y2, stroke='rgba(255,255,255,0.25)', **{'stroke-width': 4})
    add(grp, 'ellipse', cx=512, cy=620, rx=150, ry=34, fill='rgba(255,255,255,0.6)')


def build_hair_long(svg, defs):
    grp = add(svg, 'g')
    grad = add_linear_gradient(defs, 'longHair', [
        (0, '#fff2b0', 1),
        (40, '#ffd161', 1),
        (100, '#f7b733', 1)
    ])
    add(grp, 'path', d='M340 160 C 320 280 330 420 360 520 C 260 520 260 780 360 870 C 420 920 600 940 680 860 C 760 780 744 520 660 520 C 690 420 700 280 680 160 C 600 100 420 100 340 160 Z', fill=grad)
    add(grp, 'path', d='M360 220 C 390 180 634 180 664 220 C 674 260 674 320 660 360 C 600 310 420 310 360 360 C 346 320 346 260 360 220 Z', fill='rgba(255,255,255,0.35)')
    for wave in range(6):
        add(grp, 'path', d=f'M{360+wave*60} 260 C {340+wave*60} 420 {420+wave*60} 620 {360+wave*60} 780', stroke='rgba(255,255,255,0.2)', fill='none', **{'stroke-width': 12})


def build_hair_bun(svg, defs):
    grp = add(svg, 'g')
    grad = add_linear_gradient(defs, 'bunBase', [
        (0, '#6d3b1f', 1),
        (100, '#a25f2a', 1)
    ])
    add(grp, 'path', d='M360 220 C 370 160 654 160 664 220 L 676 380 C 644 430 380 430 348 380 Z', fill=grad)
    add(grp, 'ellipse', cx=512, cy=180, rx=110, ry=70, fill='#8c4a24')
    add(grp, 'circle', cx=512, cy=150, r=72, fill='#b26a38')
    add(grp, 'path', d='M420 250 C 420 400 604 400 604 250', fill='rgba(0,0,0,0.1)')
    for ring in range(5):
        add(grp, 'ellipse', cx=512, cy=150, rx=72-ring*10, ry=60-ring*8, stroke='rgba(255,255,255,0.08)', fill='none', **{'stroke-width': 4})


def build_shoes_heels(svg, defs):
    grp = add(svg, 'g')
    grad = add_linear_gradient(defs, 'heelsGrad', [
        (0, '#ff66a6', 1),
        (100, '#d81b60', 1)
    ])
    add(grp, 'path', d='M380 870 C 420 840 500 830 520 880 C 528 900 520 940 480 950 C 420 960 360 930 360 900 Z', fill=grad)
    add(grp, 'path', d='M540 880 C 560 830 660 830 700 870 C 720 900 680 960 620 960 C 580 960 548 930 540 900 Z', fill=grad)
    add(grp, 'circle', cx=420, cy=872, r=12, fill='rgba(255,255,255,0.4)')
    add(grp, 'circle', cx=640, cy=872, r=12, fill='rgba(255,255,255,0.4)')


def build_shoes_sneakers(svg, defs):
    grp = add(svg, 'g')
    add(grp, 'path', d='M360 880 C 420 820 520 820 540 880 C 520 920 420 940 360 910 Z', fill='#fdfdfd', stroke='#d1d1d1', **{'stroke-width': 6})
    add(grp, 'path', d='M540 880 C 560 820 660 820 720 880 C 700 930 600 940 540 910 Z', fill='#fdfdfd', stroke='#d1d1d1', **{'stroke-width': 6})
    for idx, cx in enumerate([400, 430, 460, 490, 600, 630, 660, 690]):
        add(grp, 'circle', cx=cx, cy=880+(idx//4)*20, r=8, fill='#ff6fb4')
    add(grp, 'rect', x=360, y=900, width=360, height=26, rx=12, fill='rgba(255,105,180,0.18)')


def build_glasses(svg, defs):
    grp = add(svg, 'g', transform='translate(0,-40)')
    add(grp, 'ellipse', cx=420, cy=320, rx=90, ry=80, fill='rgba(255,255,255,0.05)', stroke='#ff82c3', **{'stroke-width': 18})
    add(grp, 'ellipse', cx=604, cy=320, rx=90, ry=80, fill='rgba(255,255,255,0.05)', stroke='#ff82c3', **{'stroke-width': 18})
    add(grp, 'rect', x=506, y=300, width=92, height=24, rx=12, fill='#ff82c3')
    add(grp, 'path', d='M330 320 C 280 320 250 300 220 280', stroke='#ff82c3', fill='none', **{'stroke-width': 18, 'stroke-linecap': 'round'})
    add(grp, 'path', d='M694 320 C 744 320 774 300 804 280', stroke='#ff82c3', fill='none', **{'stroke-width': 18, 'stroke-linecap': 'round'})
    add(grp, 'circle', cx=362, cy=300, r=10, fill='#ffd1e8')
    add(grp, 'circle', cx=662, cy=300, r=10, fill='#ffd1e8')


def build_handbag(svg, defs):
    grp = add(svg, 'g')
    body_grad = add_linear_gradient(defs, 'bagBody', [
        (0, '#ff9dc8', 1),
        (100, '#ff5fa2', 1)
    ])
    add(grp, 'rect', x=580, y=600, width=160, height=150, rx=40, fill=body_grad)
    add(grp, 'path', d='M600 600 C 600 520 720 520 720 600', fill='none', stroke='#ffc9e1', **{'stroke-width': 26, 'stroke-linecap': 'round'})
    add(grp, 'circle', cx=660, cy=672, r=18, fill='#ffe082')
    add(grp, 'path', d='M620 640 L 700 640 L 690 700 C 660 730 640 730 610 700 Z', fill='rgba(255,255,255,0.2)')
    add(grp, 'circle', cx=620, cy=620, r=10, fill='#ffeef7')


def build_star(svg, defs):
    grp = add(svg, 'g')
    grad = add_radial_gradient(defs, 'starSparkle', [
        (0, '#fff8c6', 1),
        (60, '#ffd700', 0.95),
        (100, '#ffb347', 0.6)
    ])
    points = []
    for i in range(10):
        angle = math.pi / 5 * i
        radius = 200 if i % 2 == 0 else 80
        x = 512 + math.cos(angle - math.pi / 2) * radius
        y = 512 + math.sin(angle - math.pi / 2) * radius
        points.append(f'{x},{y}')
    add(grp, 'polygon', points=' '.join(points), fill=grad, stroke='#ffe082', **{'stroke-width': 12, 'stroke-linejoin': 'round'})
    for i in range(40):
        angle = math.radians(i * 9)
        length = 260
        add(grp, 'line', x1=512, y1=512, x2=512 + math.cos(angle) * length, y2=512 + math.sin(angle) * length,
            stroke='rgba(255,255,255,0.2)', **{'stroke-width': 3})


ASSET_SPECS = [
    {
        'file': 'outfit_princess_dress.png',
        'category': 'outfits',
        'name': 'Layered sparkle princess gown',
        'builder': build_princess
    },
    {
        'file': 'outfit_jeans_top.png',
        'category': 'outfits',
        'name': 'Bright top + comfy jeans',
        'builder': build_jeans
    },
    {
        'file': 'outfit_ballet.png',
        'category': 'outfits',
        'name': 'Ballet leotard with tutu',
        'builder': build_ballet
    },
    {
        'file': 'hair_long_blonde.png',
        'category': 'hairhats',
        'name': 'Long flowing blonde hair',
        'builder': build_hair_long
    },
    {
        'file': 'hair_bun_brown.png',
        'category': 'hairhats',
        'name': 'Chic brown bun',
        'builder': build_hair_bun
    },
    {
        'file': 'shoes_heels.png',
        'category': 'shoes',
        'name': 'Pink party heels',
        'builder': build_shoes_heels
    },
    {
        'file': 'shoes_sneakers.png',
        'category': 'shoes',
        'name': 'Bright white sneakers',
        'builder': build_shoes_sneakers
    },
    {
        'file': 'accessory_glasses.png',
        'category': 'accessories',
        'name': 'Round glitter glasses',
        'builder': build_glasses
    },
    {
        'file': 'accessory_handbag.png',
        'category': 'accessories',
        'name': 'Pink bow handbag',
        'builder': build_handbag
    },
    {
        'file': 'sticker_star.png',
        'category': 'stickers',
        'name': 'Golden sparkle star',
        'builder': build_star
    }
]


# ------------------------------------------------------------
# CONVERSION PIPELINE
# ------------------------------------------------------------


def converter_from_cairosvg_module():
    try:
        import cairosvg  # type: ignore
    except Exception:
        return None

    def run(svg_text: str, out_path: Path):
        cairosvg.svg2png(bytestring=svg_text.encode('utf-8'), write_to=str(out_path), output_width=WIDTH, output_height=HEIGHT)

    return ('cairosvg (python)', run)


def converter_from_svglib():
    try:
        from svglib.svglib import svg2rlg  # type: ignore
        from reportlab.graphics import renderPM  # type: ignore
    except Exception:
        return None

    def run(svg_text: str, out_path: Path):
        with tempfile.NamedTemporaryFile('w', suffix='.svg', delete=False) as tmp:
            tmp.write(svg_text)
            tmp_path = tmp.name
        try:
            drawing = svg2rlg(tmp_path)
            renderPM.drawToFile(drawing, str(out_path), fmt='PNG')
        finally:
            os.unlink(tmp_path)

    return ('svglib/reportlab', run)


def converter_from_cli(exe_name: str):
    exe = shutil.which(exe_name)
    if not exe:
        return None

    def run(svg_text: str, out_path: Path, exe=exe_name):
        with tempfile.TemporaryDirectory() as tmpdir:
            svg_path = Path(tmpdir) / 'asset.svg'
            svg_path.write_text(svg_text)
            if exe == 'cairosvg':
                subprocess.run([exe, str(svg_path), '-o', str(out_path)], check=True)
            elif exe == 'rsvg-convert':
                subprocess.run([exe, str(svg_path), '-o', str(out_path)], check=True)
            elif exe == 'inkscape':
                subprocess.run([exe, str(svg_path), '--export-type=png', f'--export-filename={out_path}', '--export-width=1024', '--export-height=1024'], check=True)
            else:
                raise RuntimeError(f'Unsupported CLI {exe}')

    return (f'{exe_name} CLI', run)


def converter_from_qlmanage():
    exe = shutil.which('qlmanage')
    if not exe:
        return None

    def run(svg_text: str, out_path: Path):
        with tempfile.TemporaryDirectory() as tmpdir:
            svg_path = Path(tmpdir) / 'asset.svg'
            svg_path.write_text(svg_text)
            cmd = ['qlmanage', '-t', '-s', '1024', '-o', tmpdir, str(svg_path)]
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            generated = Path(tmpdir) / (svg_path.name + '.png')
            if not generated.exists():
                raise RuntimeError('qlmanage did not produce PNG')
            shutil.move(str(generated), out_path)

    return ('qlmanage thumbnailer', run)


def html_fallback(svg_text: str, out_path: Path):
    html_path = out_path.with_suffix('.html')
    data_url = 'data:image/svg+xml;base64,' + base64.b64encode(svg_text.encode('utf-8')).decode('ascii')
    html_path.write_text(f"""<!DOCTYPE html><html><body><a download='{out_path.name}' href='{data_url}'>Download {out_path.name}</a><script>setTimeout(()=>document.querySelector('a').click(),200);</script></body></html>""")
    raise RuntimeError('No PNG converter available; wrote HTML fallback instead')


CONVERTERS = [
    converter_from_cairosvg_module(),
    converter_from_svglib(),
    converter_from_cli('cairosvg'),
    converter_from_cli('rsvg-convert'),
    converter_from_cli('inkscape'),
    converter_from_qlmanage()
]
CONVERTERS = [c for c in CONVERTERS if c]
if CONVERTERS:
    CONVERTER_NAME, CONVERT_FN = CONVERTERS[0]
else:
    CONVERTER_NAME, CONVERT_FN = ('html-fallback', html_fallback)


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------


def main():
    manifest = []
    print(f'Using converter: {CONVERTER_NAME}')
    for spec in ASSET_SPECS:
        svg_root, defs = new_svg()
        spec['builder'](svg_root, defs)
        svg_text = "<?xml version='1.0' encoding='UTF-8'?>\n" + tostring(svg_root, encoding='unicode')
        svg_path = SVG_DIR / (Path(spec['file']).stem + '.svg')
        svg_path.write_text(svg_text)
        png_path = PNG_DIR / spec['file']
        if png_path.exists():
            png_path.unlink()
        try:
            CONVERT_FN(svg_text, png_path)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f'Failed converting {spec["file"]}: {e}')
        manifest.append({
            'file': spec['file'],
            'category': spec['category'],
            'name': spec['name'],
            'path': str(png_path.relative_to(ROOT))
        })
        print(f'✓ Built {spec["file"]}')
    manifest_path = PNG_DIR / 'manifest.json'
    manifest_path.write_text(json.dumps({
        'converter': CONVERTER_NAME,
        'assets': manifest
    }, indent=2))
    print(f'Wrote manifest to {manifest_path}')


if __name__ == '__main__':
    main()
