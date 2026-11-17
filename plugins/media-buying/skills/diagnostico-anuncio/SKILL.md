---
name: diagnostico-anuncio
description: Diagnostica um anúncio ou campanha que está indo mal (ou bem demais) lendo-o como um funil próprio, do primeiro segundo até a venda, incluindo o pós-clique (quiz, VSL, checkout, lead no CRM), e escreve o rebrief só do estágio fraco. Também investiga "dia ruim" quando as vendas caem de repente. Use quando o usuário disser "por que esse anúncio não funciona", "diagnostica esse criativo", "onde está vazando", "as vendas caíram ontem", "dia ruim", "rebrief".
---

# Diagnóstico de anúncio

Um anúncio raramente está ruim inteiro. Na maioria das vezes um estágio vaza e o resto está
saudável. Refazer o anúncio todo joga fora o que funcionava. Esta skill acha o estágio e
reescreve só ele. Se todos os estágios estiverem fracos, confirma que é um fracasso de verdade.

## Antes de começar
Leia `numeros.md`, `regras.md`, `marca.md` e `aprendizados.md` da conta
(`**/contas/<slug>/`). Peça os dados do anúncio e a média da conta no mesmo formato. Se o
anúncio teve pouca verba, diga quanto falta gastar para julgar e pare aí.

## O funil completo
Monte a cadeia de estágios do tipo de funil da conta e preencha com o que houver. O que não
houver vira FALTANDO, com onde conseguir.

| Estágio | venda-direta | low-ticket (quiz/VSL) | lead-crm |
|---|---|---|---|
| 1. Hook | 3 s ÷ impressões | igual | igual |
| 2. Retenção | ThruPlay ÷ 3 s | igual | igual |
| 3. Clique | CTR (link) | igual | igual |
| 4. Chegada | visualizações da página ÷ cliques | visitas no quiz ÷ cliques | visitas na LP ÷ cliques |
| 5. Meio | produto visto / carrinho | conclusão do quiz, chegada na VSL | envio do formulário |
| 6. Decisão | início de checkout | retenção da VSL, clique no botão, início de checkout | lead → MQL |
| 7. Fechamento | compra | compra + bump + upsell | MQL → orçamento → venda |

- Compare cada estágio com a média da conta. Sem média, use o próprio histórico do anúncio.
- **Chegada baixa** (estágio 4) quase sempre é técnico: página lenta, redirecionamento,
  vídeo que não toca no celular, pixel duplicado. Verifique antes de culpar o criativo.
- Criativo com CTR alto e venda baixa é sinal de problema depois do clique, não do anúncio.

## Veredito
- **Um estágio abaixo da média:** CONSERTAR. Rebrief só desse estágio.
- **Dois estágios:** CONSERTAR o mais cedo no funil primeiro (consertar o hook muda quem
  chega no resto).
- **Todos abaixo:** MATAR de verdade. Escreva a lição: que hipótese o anúncio testou e o
  que o resultado sugere.

## Rebrief por estágio
Dê 3 correções específicas, que dá para briefar hoje, usando só promessas de `marca.md`:

- **Hook:** 3 aberturas novas, cada uma com estrutura diferente (chamada direta do público,
  lacuna de curiosidade, opinião contrária, momento do problema, prova social), escritas
  como o que se **vê**, se **ouve** e se **lê na tela** nos 3 primeiros segundos. Nunca
  abrir com logo.
- **Retenção:** cortar o que vem antes do problema, mostrar o produto/resultado mais cedo,
  ritmo mais rápido, legenda na tela.
- **Clique:** prova mais forte, oferta mais clara, um único CTA de baixa fricção, um loop
  de curiosidade que só fecha do outro lado do clique.
- **Pós-clique:** a correção é na página, quiz, VSL, checkout ou atendimento. Diga qual
  passo, o número, e o teste a fazer. Não é briefing de criativo.

Toda correção sai com uma hipótese: "Se trocarmos X, esperamos Y subir de A para B".

## Modo "dia ruim"
Quando as vendas caem de repente, investigue nesta ordem antes de mexer em qualquer coisa:
1. O rastreamento funcionou? (conversões disparando nas plataformas e na fonte de verdade)
2. O site/checkout teve problema? (taxa de conversão da página, erro de checkout, gateway)
3. Verba ou CPM saltou em alguma plataforma?
4. Um anúncio ou campanha importante parou de entregar? (reprovado, limite de gasto, cartão)
5. Algo de fora: feriado, concorrente, mudança de preço, oferta fora do ar.

Diga a causa mais provável com os números, quanto você tem certeza (baixa, média, alta) e
a única coisa a checar primeiro. Se parecer um dia ruim normal dentro da variação da conta,
diga isso e recomende esperar.

## Guardrails
- Diagnóstico não muda nada na conta. Qualquer ação vira item numerado para aprovação.
- Nunca inventar métrica nem promessa de anúncio.
- Pouca amostra: dizer quanto falta, não dar veredito.
