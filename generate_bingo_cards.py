import html
import os
import random

from typing import List


icons = [f for f in os.listdir('html/figures/icons') if f.endswith('.png')]

# 4 grupos de 10 ícones
num_groups = 4
group_size = 10
icon_groups = [icons[i * group_size:(i + 1) * group_size] for i in range(num_groups)]

ISAQUE = 'isaque.png'


def generate_card_with_isaque() -> List[List[str]]:
    # posições possíveis 4x4
    cells = [(r, c) for r in range(4) for c in range(4)]
    # pares de posições sem mesma linha ou coluna
    valid_pairs = []
    for i in range(len(cells)):
        for j in range(i + 1, len(cells)):
            (r1, c1), (r2, c2) = cells[i], cells[j]
            if r1 != r2 and c1 != c2:
                valid_pairs.append(((r1, c1), (r2, c2)))

    p1, p2 = random.choice(valid_pairs)

    # matriz 4x4
    card = [[None for _ in range(4)] for _ in range(4)]
    card[p1[0]][p1[1]] = ISAQUE
    card[p2[0]][p2[1]] = ISAQUE

    # completar por coluna a partir de cada grupo
    for col in range(4):
        pool = [ic for ic in icon_groups[col] if ic != ISAQUE]
        already = sum(1 for r in range(4) if card[r][col] == ISAQUE)
        needed = 4 - already
        choices = random.sample(pool, needed)
        k = 0
        for row in range(4):
            if card[row][col] is None:
                card[row][col] = choices[k]
                k += 1

    return card


def card_tuple(card: List[List[str]]):
    return tuple(tuple(row) for row in card)


def generate_unique_bingos(total_bingos: int) -> List[List[List[str]]]:
    seen = set()
    cards: List[List[List[str]]] = []
    attempts = 0
    while len(cards) < total_bingos and attempts < total_bingos * 100:
        c = generate_card_with_isaque()
        t = card_tuple(c)
        if t not in seen:
            seen.add(t)
            cards.append(c)
        attempts += 1
    return cards


def bingo_table_html(card: List[List[str]], index: int) -> str:
    h = f'<table class="bingo-table"><caption>BINGO #{index + 1}</caption>'
    for r in range(4):
        h += '<tr>'
        for c in range(4):
            src = html.escape('figures/icons/' + card[r][c])
            h += f'<td><img src="{src}" alt="" class="icon" /></td>'
        h += '</tr>'
    h += '</table>'
    return h


# gerar 40 bingos
cards = generate_unique_bingos(40)

# montar páginas com 6 bingos por A4
pages = []
for i in range(0, len(cards), 6):
    page_cards = cards[i:i + 6]
    page_html = '<div class="page">' + ''.join(
        f'<div class="bingo-card">{bingo_table_html(card, i + j)}</div>'
        for j, card in enumerate(page_cards)
    ) + '</div>'
    pages.append(page_html)

full_html = '''<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>Cartelas de Bingo do Isaque :) - Ícones</title>
<style>
body { margin: 0; padding: 0; }
.page {
  width: 210mm;
  height: 297mm;
  page-break-after: always;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  align-items: flex-start;
}
.bingo-card {
  width: 350px;
  height: 350px;     /* 280px da matriz + espaço para o título/caption + padding */
  box-sizing: border-box;
  padding: 6px 6px 12px 6px;
  margin: 12px;
  border: 2px dashed #639cb8;
  border-radius: 8px;
  background: #f9fafd;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
}
.bingo-table {
  width: 280px;
  height: 280px;
  border-collapse: collapse;
  table-layout: fixed;
}
.bingo-table caption {
  caption-side: top;
  font-size: 1.3em;
  margin-top: 3px;;
  margin-bottom: 3px;
  color: #37688f;
  font-weight: bold;
  height: 36px;  /* reserva espaço sempre igual para o título */
  line-height: 28px;
}
.bingo-table td {
  width: 70px;
  height: 70px;
  border: 1px solid #85a9ce;
  text-align: center;
  vertical-align: middle;
  font-family: Arial, sans-serif;
  background: #eef5fc;
  padding: 0;
}
.icon {
  max-width: 55px;
  max-height: 55px;
  width: auto;
  height: auto;
  display: inline-block;
  margin: auto;
}
@media print {
  body { margin: 0; }
  .page { page-break-after: always; }
}
</style>
</head>
<body>
'''

full_html += '\n'.join(pages)
full_html += '\n</body>\n</html>'

with open("html/bingo-cards.html", "w", encoding="utf-8") as f:
    f.write(full_html)
