# BMC — Publicador de Carrossel Instagram

## Instalar (só na primeira vez)

```
pip install playwright pillow
playwright install chromium
```

---

## Como usar a cada novo carrossel

**Passo 1** — Salve o HTML gerado pelo Claude como `carrossel.html` nesta pasta

**Passo 2** — Edite `legenda.txt` com a legenda do post

**Passo 3** — No terminal, rode:
```
python postar.py
```

**Passo 4** — Digite seu usuário e senha quando pedido

Pronto. O script abre o Instagram, faz o upload e publica sozinho.

---

## O que cada arquivo faz

| Arquivo | O que é |
|---|---|
| `carrossel.html` | HTML do carrossel — você troca a cada post |
| `legenda.txt` | Legenda do post — você edita a cada post |
| `postar.py` | Script que faz tudo — não precisa mexer |
| `slides_png/` | Pasta criada automaticamente com as imagens |

---

## Se travar em algum passo

O script pausa e avisa. Você age manualmente no browser e pressiona Enter para continuar.
