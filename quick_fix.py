#!/usr/bin/env python3
"""Минимальное исправление 404 ошибок"""

import os
from pathlib import Path

# Создание директорий
dirs = ['static/css', 'static/js', 'static/img', 'static/fonts']
for d in dirs:
    Path(d).mkdir(parents=True, exist_ok=True)

# Пустые CSS файлы
Path('static/css/swiper-bundle.min.css').write_text('/* Swiper CSS placeholder */')
Path('static/css/style.css').write_text('''
body { font-family: Arial, sans-serif; margin: 0; }
.container { max-width: 1200px; margin: 0 auto; padding: 0 15px; }
img { background: #f0f0f0; border: 1px solid #ddd; }
''')
Path('static/css/media.css').write_text('/* Media queries */')

# Пустой JS
Path('static/js/main.js').write_text('console.log("Site loaded");')

# SVG заглушки
svg_template = '<svg width="100" height="50" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="#f0f0f0"/><text x="50%" y="50%" text-anchor="middle" dy=".3em" font-size="12" fill="#666">{}</text></svg>'

files = [
    ('static/img/logo.svg', 'LOGO'),
    ('static/img/logofooterldpi.svg', 'FOOTER'),
    ('static/img/about1ldpi.svg', 'ICON1'),
    ('static/img/about2ldpi.svg', 'ICON2'),
    ('static/img/about3ldpi.svg', 'ICON3'),
    ('static/img/about4ldpi.svg', 'ICON4'),
    ('static/img/a.svg', '↓'),
    ('static/img/fonldpi.svg', 'BG'),
]

for filepath, text in files:
    Path(filepath).write_text(svg_template.format(text))

# PNG как SVG
Path('static/img/fon.svg').write_text(svg_template.format('BG'))
Path('static/img/a-icon.svg').write_text(svg_template.format('↓'))

# Пустые шрифты
fonts = ['Gilroy-Regular.ttf', 'Gilroy-Medium.ttf', 'Gilroy-Semibold.ttf', 'Gilroy-Bold.ttf', 'Gilroy-Light.ttf']
for font in fonts:
    Path(f'static/fonts/{font}').touch()

print("✅ Все файлы созданы! Перезапустите сервер.")