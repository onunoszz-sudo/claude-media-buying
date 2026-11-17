---
name: multiplicador-de-vencedor
description: Pega um anúncio vencedor (ou quase) e multiplica - explica por que ele ganhou estágio por estágio, separa o que não se mexe, planeja variações de uma variável por vez com o original como controle, reescreve o roteiro em blocos (hook, história, fechamento) com grade de combinação, resgata o hook quando só ele está fraco, e gera títulos e descrições de RSA para o Google. Use quando o usuário disser "multiplica esse vencedor", "variações do anúncio que vende", "hooks novos", "o hook está fraco", "resgatar o anúncio", "roteiro em blocos", "anúncio cansando, o que faço", "títulos de RSA a partir do vencedor".
---

# Multiplicador de vencedor

Um vencedor é o ativo mais barato da conta: já provou que o ângulo funciona. Em vez de
procurar o próximo do zero, esta skill descobre o que nele funciona, protege isso e troca uma
coisa de cada vez. Também serve para resgatar um anúncio quando só o começo está fraco.

## Antes de começar
1. Ache a pasta da conta (`**/contas/<slug>/`). Leia `numeros.md`, `marca.md`,
   `vencedores.md`, `aprendizados.md` e `testes.md`.
2. Dados do anúncio, pelo conector oficial do Meta Ads ou export: gasto, impressões,
   reproduções de 3 s (ou 2 s contínuos), 25/50/75/100% do vídeo, ThruPlay, cliques no link,
   visitas, checkouts, compras, frequência; os mesmos números da **média da conta** no mesmo
   formato. Texto e título do anúncio.
3. **O conteúdo do criativo:** roteiro, transcrição ou o arquivo de vídeo. Sem saber o que o
   anúncio diz e mostra, não há como explicar por que ganhou: peça antes de seguir.
4. Confirme que é vencedor pelos critérios de `numeros.md`. Se ainda não é (poucas vendas),
   diga "quase vencedor" e trate as variações como teste, não como escala.

## 1. Por que ganhou
Leia o anúncio estágio por estágio contra a média da conta (mesmo formato):
| Estágio | Conta | Leitura |
|---|---|---|
| Hook | 3 s ÷ impressões | os primeiros segundos param o scroll? |
| Retenção | 25%, 50%, ThruPlay ÷ 3 s | a história segura? onde a curva cai? |
| Clique | CTR do link | o fechamento dá vontade de saber mais? |
| Pós-clique | visita ÷ clique, checkout ÷ visita, compra ÷ checkout | quem clica é o público certo? |

Depois liste, com evidência, **as 3 coisas que o anúncio faz** (ex.: abre com a dor de hoje,
mostra o produto antes de 5 s, termina com convite ao teste). Isso é o que não se mexe.

## 2. Variações de uma variável
Cada variação muda **uma** coisa; o original fica no ar como controle. Ordem, da mais barata
para a mais cara:
1. **Hook** (primeiros 3 a 5 s: frase, texto na tela, primeira imagem). Com avatar de IA ou
   corte de vídeo existente, é só gerar ou cortar o começo.
2. **Texto do anúncio e título** (não mexe no vídeo).
3. **Fechamento** (chamada final, o que acontece depois do clique).
4. **Formato** (o mesmo roteiro em estático, carrossel ou vídeo mais curto).
5. **Quem fala ou onde** (outro cenário, outra pessoa): só depois que 1 a 4 estiverem testados.

Cada variação ganha nome `gatilho / ângulo / H#` e uma decisão combinada, no formato da
`rodada-de-teste` (que dimensiona quantas cabem na verba).

## 3. Roteiro em blocos
Reescreva o vencedor em blocos que se encaixam:
- **Hooks (H1, H2, H3):** 3 a 5 s cada, aberturas diferentes (pergunta, afirmação que
  surpreende, cena do problema, número verdadeiro, fala de quem sente), cada uma com o texto na
  tela, porque muita gente assiste sem som.
- **História (S1):** o corpo do vencedor, sem mudar.
- **Fechamentos (C1, C2):** a chamada atual e uma alternativa.

Grade de combinação: H1+S1+C1, H2+S1+C1, H3+S1+C1 primeiro (só o hook muda); fechamentos
depois. Com vídeo de avatar de IA, cada hook é uma geração curta colada ao corpo existente;
com gravação, os blocos são filmados separados para o editor combinar.

## 4. Resgate de hook
Quando **só** o hook está fraco (3 s ÷ impressões abaixo da média da conta e retenção, clique
e pós-clique na média ou acima), não refaça o anúncio: escreva 3 hooks novos para o mesmo
corpo e teste como na seção 2. Se mais de um estágio está fraco, o problema não é o hook: use
`diagnostico-anuncio`.

## 5. Para o Google (RSA)
Do vencedor, tire até 15 títulos (até 30 caracteres) e 4 descrições (até 90): a dor, a promessa
aceita no `marca.md`, a prova, o convite. Conte os caracteres. Um título por ideia, sem
repetir palavra-chave em todos.

## Saída
Sem travessão, no idioma do anúncio para os textos que vão ao ar.

1. **Por que ganhou:** tabela por estágio contra a média, e as 3 coisas que não se mexem.
2. **Variações:** tabela com nome, o que muda, o que fica, hipótese, decisão combinada.
3. **Roteiro em blocos:** H1 a H3 (fala + texto na tela + imagem), S1, C1 e C2, e a grade.
4. **Títulos e descrições de RSA**, se a conta usa Google.
5. **O que pedir ao produtor:** arquivos, gerações de avatar ou cortes necessários.

Grave as variações em `testes.md` e o motivo da vitória em `vencedores.md`.

## Guardrails
- Nada sobe sem "sim"; criar e ativar anúncio é ação separada.
- Uma variável por variação; o original continua como controle.
- Nada de promessa, número, credencial ou depoimento que o `marca.md` proíbe; o que o dono da
  conta aceitou e está registrado lá pode ser usado.
- Número no hook só se for verdadeiro e tiver fonte.
- Nunca inventar métrica; o que faltar aparece como FALTANDO.
