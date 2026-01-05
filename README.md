# Bingo generator

Projeto simples para gerar cartelas de bingo (página imprimível) e uma página interativa de sorteio.

## O que faz
- Gera várias cartelas 4×4 usando um conjunto de ícones e salva uma página HTML imprimível em `html/bingo-cards.html`.
- Há também uma página interativa em `html/bingo.html` que permite sortear ícones com animação.

## Estrutura principal
- `generate_bingo_cards.py`: script Python que monta as cartelas e escreve `html/bingo-cards.html`.
- `html/bingo-cards.html`: saída imprimível (A4, 6 cartelas por página).
- `html/bingo.html`: página interativa com sorteio animado.
- `html/figures/icons/` e `html/figures/banners/`: imagens usadas (ícones e banners/figuras).
- `vectors/`: recursos vetoriais do projeto.

## Requisitos
- Python 3.x (usa apenas a stdlib: `random`, `html`, `typing`).

## Uso rápido
1. Gere as cartelas executando:

```bash
python3 generate_bingo_cards.py
```

2. Abra a pasta `html/` no navegador para ver/ imprimir:

```bash
python3 -m http.server --directory html 8000
# depois abra http://localhost:8000/bingo-cards.html ou /bingo.html
```

## Pontos de configuração / como trocar o tema
- Ícones: o script define uma lista `icons` dentro de `generate_bingo_cards.py`. Para usar outro tema, substitua os arquivos em `html/figures/icons/` e atualize a lista `icons` (ou modifique o script para ler automaticamente o diretório).
- Grupos de ícones: o script agrupa ícones em `icon_groups` (variáveis `num_groups` e `group_size`). Ajuste essas variáveis se seu tema tiver outra organização.
- Ícone fixo especial: a constante `ISAQUE` é usada para forçar a presença de um ícone específico em posições particulares — remova/edite se não quiser esse comportamento.
- Quantidade de cartelas: troque o argumento de `generate_unique_bingos(40)` para gerar mais/menos cartelas.
- Cartelas por página: o trecho que cria `pages` usa blocos de 6; altere o passo do slice `for i in range(0, len(cards), 6)` para mudar quantas cartelas por página.
- Tamanho da grade: o código atual gera matrizes 4×4 (valor usado em `cells`, loops e CSS). Para 5×5 você precisará ajustar a lógica de geração e os estilos CSS (largura/altura dos `.bingo-table` e `.icon`).
- Página interativa: atualize a lista `icons` dentro de `html/bingo.html` e substitua as imagens em `html/figures/banners/` para adaptar a interface de sorteio ao novo tema.
