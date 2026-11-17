---
name: relatorio-semanal
description: Escreve o relatório semanal (de segunda) de uma conta de anúncios, juntando Meta, Google e a fonte de verdade das vendas - em duas versões, a interna (com breakeven, prejuízo e decisões) e a do cliente (foco em ajustes e próximos passos). Use quando o usuário disser "relatório da semana", "relatório de segunda", "resumo semanal", "relatório pro cliente", "como foi a semana nos anúncios".
---

# Relatório semanal

Uma vez por semana, a história da conta em palavras simples: o que aconteceu, por quê, o que
foi feito e o que precisa de decisão. É o relatório que um bom gestor de tráfego mandaria,
sem precisar de reunião.

## Antes de começar
1. Leia os 6 arquivos da conta (`**/contas/<slug>/`). Em `marca.md` está o que pode e o que
   não pode aparecer no material que o cliente vê.
2. Defina as datas: semana fechada (segunda a domingo) contra a semana anterior. Diga as
   datas no topo.
3. Dados: Meta, Google e a fonte de verdade das vendas da semana e da anterior; o que foi
   pausado/escalado na semana; aprendizados novos.
4. **Regra de ouro:** recalcule todo derivado (CPA, ROAS, MER, ticket, CPM) a partir dos
   totais da semana. Nunca copie um derivado pronto de planilha ou de linha de total, que
   pode estar desatualizada.

## Versão interna (para o gestor)
Menos de 400 palavras, sem travessão.
1. **Manchete** em uma frase.
2. **Números:** verba total, receita (fonte de verdade), MER contra alvo e breakeven; para
   lead-crm, leads, MQL, orçamentos, vendas e custo por cada um.
3. **Meta:** verba, conversões, CPA, ROAS; os 3 melhores anúncios e por que ganharam, e os
   **3 piores por custo extra** (gasto − conversões × CPA alvo) com a ação para cada um. Se a
   fonte de verdade tem a origem da venda por anúncio, use as vendas reais.
4. **Google:** verba, conversões, ROAS; melhor e pior campanha; negativas adicionadas.
5. **Pós-clique:** o estágio do funil que mais mudou (página, quiz, checkout, atendimento).
6. **O que foi pausado/escalado** e quanto isso economizou ou rendeu (estimativa, com a conta).
7. **Criativos que precisamos na próxima semana.**
   Inclua o que mudou no funil na semana (deploy, preço, VSL, bump, upsell), tirado do diário
   de mudanças da conta, se existir: mudança sem registro confunde a leitura da semana.
8. **Três decisões para o gestor**, numeradas.

## Versão cliente
Mesmos fatos, outro enquadramento:
- **Sem** breakeven, prejuízo, ROI negativo ou comparações que soem como fracasso. Mostrar o
  que melhorou, o que foi ajustado e o que vem a seguir.
- Números que o cliente reconhece (vendas, pedidos, leads, custo por pedido/lead), com a
  variação contra a semana anterior.
- Um parágrafo "o que fizemos esta semana" e um "próximos passos", com o que depende do
  cliente (fotos, aprovação, atendimento do lead) escrito como pedido claro.
- Respeitar tudo que `marca.md` diz que não pode aparecer.
- Nunca esconder um problema que o cliente precisa resolver (ex.: lead sem atendimento):
  escrever como próximo passo, não como culpa.

## Depois do relatório
Proponha as linhas novas para o `aprendizados.md` (rode `log-de-aprendizados`) e, se algum
vencedor ficou 2 semanas em ESCALAR, sugira incluí-lo em `vencedores.md`.

## Guardrails
- Nunca inventar número; dado que faltou aparece como FALTANDO na versão interna e some
  (sem inventar substituto) da versão cliente.
- Estimativa de economia ou ganho sempre com a conta aberta.
- A versão cliente não é enviada pelo agente: o gestor revisa e envia.
