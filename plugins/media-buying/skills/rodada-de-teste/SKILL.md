---
name: rodada-de-teste
description: Planeja a próxima rodada de teste de criativos de uma conta - quantos anúncios cabem na verba (pela linha de MATAR), quais ângulos e hooks entram, estrutura ABO ou CBO, e para cada anúncio a hipótese, a métrica que decide, a janela de leitura e a decisão combinada antes - e registra tudo em testes.md. Use quando o usuário disser "próxima rodada de teste", "planeja os criativos novos", "quantos anúncios testo", "teste de ângulos", "subir criativos novos", "plano de teste".
---

# Rodada de teste

Teste sem decisão escrita antes vira discussão depois, e rodada maior que a verba deixa
anúncio sem gasto suficiente para ser julgado. Esta skill dimensiona a rodada pela verba e
escreve, antes de subir, o que cada anúncio precisa mostrar e o que acontece em cada caso.

## Antes de começar
1. Ache a pasta da conta (`**/contas/<slug>/`). Leia `numeros.md` (linha de MATAR, CPA alvo),
   `regras.md`, `marca.md`, `vencedores.md`, `aprendizados.md` e `testes.md` se existir.
   Sem `numeros.md`, pare e rode `numeros-da-conta`.
2. Pergunte ou leia: verba diária disponível para o teste, data de início, janela de leitura
   (padrão 7 dias) e os criativos prontos ou as ideias (ângulos e hooks) que o usuário tem.
3. Veja o que está em teste agora (`testes.md` e a conta): não sobreponha dois testes que mexem
   na mesma coisa (criativo novo + página nova + preço novo ao mesmo tempo atrapalham a leitura).
   Se houver conflito, diga e proponha a ordem.

## 1. Tamanho pela verba
Rode `scripts/calc_rodada.py --verba-diaria V --dias D --linha-matar K [--conjuntos C] [--moeda X]`.
A conta: verba diária x dias da janela ÷ linha de MATAR, para baixo. Mostre a conta.
- Se não couber um ângulo completo (padrão 3 hooks), teste **1 hook por ângulo** e deixe as
  variações de hook para o vencedor (`multiplicador-de-vencedor`).
- Se não couber nenhum anúncio, diga o que precisa mudar (janela ou verba) e pare.
- Cabem mais ideias que anúncios: escolha pelos `aprendizados.md` e pelo que nunca foi testado;
  o resto vai para a fila em `testes.md`.

## 2. Estrutura
- **ABO (orçamento no conjunto)** quando o objetivo é dar a mesma chance a cada ângulo: um
  conjunto por ângulo, verba igual. Dentro de um conjunto com vários anúncios, a Meta concentra
  a entrega em um.
- **CBO (orçamento na campanha)** quando o objetivo é deixar a Meta achar o vencedor entre
  anúncios já aprovados; aceite que alguns não vão gastar.
- Público e posicionamentos iguais entre os conjuntos do teste: a única diferença é o criativo.
- Escreva o plano no `plano-de-lancamento.md` da conta e rode `qa-de-lancamento` antes de
  subir.

## 3. Cada anúncio
| Campo | Como escrever |
|---|---|
| Nome | `gatilho / ângulo / H#` (vira o `utm_content`); ex.: `medo-dor / periné-preparado / H1` |
| Hipótese | "Se mostrar X para quem sente Y, a pessoa clica/compra porque Z", ligada a uma evidência (aprendizado, comentário, review, anúncio que já rodou) |
| Métrica que decide | uma só, do estágio que o teste mexe: hook novo decide por hook rate; ângulo novo decide por custo por checkout ou CPA |
| Janela | data de leitura e gasto mínimo (a linha de MATAR) |
| Decisão combinada | "se até DATA gastar a linha sem venda: pausar; se CPA até o alvo com o mínimo de vendas: vencedor, vai para o `multiplicador-de-vencedor`; no meio: mais uma janela" |

Use os limiares de `numeros.md` e `regras.md`. Número que não existe lá não entra na decisão:
escreva FALTANDO e pergunte.

## Saída
Sem travessão.

1. **Uma linha:** quantos anúncios, em quantos conjuntos, de quando a quando, quanto custa.
2. **A conta do tamanho** (saída do script).
3. **Tabela da rodada:** nome, ângulo, hook, criativo (arquivo), hipótese, métrica, janela,
   decisão.
4. **Estrutura para o Gerenciador:** campanha, conjuntos, verba, público, posicionamentos.
5. **Fila:** ideias que não couberam, na ordem em que entram.
6. **Conflitos** com testes em andamento, se houver.

Grave a rodada em `testes.md` na pasta da conta (uma seção por rodada, com data), para a
`revisao-meta` ler a decisão combinada e o `log-de-aprendizados` registrar o resultado.

## Guardrails
- A rodada não sobe sem o "sim" do usuário; subir e ativar é ação separada.
- Nunca mais anúncios que a verba julga.
- Decisão escrita antes não muda depois de ver o resultado, a não ser com motivo registrado.
- Criativo que esbarra no `marca.md` não entra, a não ser que o dono da conta tenha aceito
  aquela promessa e isso esteja registrado lá.
- Nunca inventar número.
