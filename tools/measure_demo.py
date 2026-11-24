"""Measures the "How we built it" numbers for a demo, the same way for every project page.

Run from the repository folder:   python tools/measure_demo.py            (all demos)
                                  python tools/measure_demo.py myrtle     (one demo folder)

- KB of custom code:     size of the demo's single index.html file, in kilobytes (1024 bytes), rounded
- CSS rules:             every rule block in the <style> element (each "{"), media and animation blocks included
- JavaScript functions:  every "function" in the page's own scripts
- Greek text strings:    every text string in the page's own scripts that contains Greek letters
Re-run it after changing a demo and update the numbers on both project pages (English and Greek).
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEMOS = ROOT / 'public' / 'demos'


def measure(folder):
    s = (DEMOS / folder / 'index.html').read_text(encoding='utf-8')
    css = ''.join(re.findall(r'<style>(.*?)</style>', s, re.S))
    js = ''.join(re.findall(r'<script>(.*?)</script>', s, re.S))
    literals = re.findall(r'"(?:[^"\\\n]|\\.)*"|\'(?:[^\'\\\n]|\\.)*\'', js)
    return {
        'kb': round(len(s.encode('utf-8')) / 1024),
        'css_rules': css.count('{'),
        'js_functions': len(re.findall(r'\bfunction\b', js)),
        'greek_strings': sum(1 for x in literals if re.search('[Ͱ-Ͽ]', x)),
        'screen_sizes': 6,
    }


if __name__ == '__main__':
    for folder in sys.argv[1:] or sorted(p.name for p in DEMOS.iterdir() if (p / 'index.html').exists()):
        print(folder, measure(folder))
