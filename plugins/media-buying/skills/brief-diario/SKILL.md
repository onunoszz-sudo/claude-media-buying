---
name: brief-diario
description: Brief da manhã de uma ou mais contas de anúncios - lê Meta Ads, Google Ads e a fonte de verdade das vendas e devolve no máximo 5 coisas que precisam do usuário hoje, a mais cara primeiro, mais o número do dia (verba, receita, MER contra a meta). Use quando o usuário disser "brief do dia", "bom dia, o que precisa de mim", "como estão as contas", "resumo da manhã", "o que olhar hoje no tráfego".
---

# Brief diário

Em vez de abrir três painéis, uma resposta curta: o que precisa de decisão hoje, em ordem
de quanto custa ignorar. Leva 10 minutos do usuário. Não muda nada na conta.

## Quais contas
Se o usuário não disser, procure todas as pastas `**/contas/*/numeros.md` e pergunte se é
para rodar todas ou só algumas. Rodando várias, um bloco por conta, começando pela conta
com o problema mais caro.

## Dados (por conta)
1. **Meta:** ontem e últimos 7 dias, pelo conector oficial se estiver nesta sessão; senão,
   o export mais recente que o usuário mandar.
2. **Google Ads:** o relatório mais recente disponível (CSV, leitura no navegador ou MCP).
   **Diga a data do dado.** Dado com mais de 7 dias é avisado como velho.
3. **Fonte de verdade das vendas** (de `numeros.md`): Hotmart, Cardápio Web, planilha ou
   CRM. Se não estiver acessível, use o pixel e escreva "receita do pixel, não confirmada".

## O que procurar
- **Meta:** anúncio 50%+ acima do CPA alvo por 3 dias; anúncio gastando sem conversão
  além de 2x o CPA alvo; anúncio pronto para ESCALAR; sinais de fadiga (frequência subindo
  com CTR caindo).
- **Google:** termos de pesquisa gastando sem conversão; campanha lucrativa limitada por
  orçamento; salto de CPC ou de gasto; anúncio ou palavra reprovada; URL final quebrada.
- **Funil:** queda brusca de conversão da página, do quiz ou do checkout; para lead-crm,
  leads de ontem sem primeiro contato.
- **Criativo:** os melhores anúncios estão ficando velhos e ainda não há variação briefada.
- **Rastreamento:** pixel e fonte de verdade divergindo mais de 20% (ação: rodar
  `conferencia-de-rastreamento`).

## Saída
Menos de 200 palavras por conta, sem travessão.

```
<CONTA> · <data>
Número do dia: verba ontem R$ X · receita R$ Y (fonte) · MER Z (alvo A) · 7 dias: MER W

Precisa de você hoje:
1. [Meta] <o que está errado em uma linha> · <números> · Ação: <uma ação>
2. ...
(no máximo 5, o mais caro primeiro; se nada precisar, dizer isso)

Proteger: <uma coisa que está funcionando e não deve ser mexida>
```

Termine perguntando quais ações numeradas o usuário aprova. Para as aprovadas que exigem
mais análise, chame a skill certa (`revisao-meta`, `diagnostico-anuncio`,
`termos-de-pesquisa`, `saude-google-ads`).

## Guardrails
- Só leitura. Nenhuma mudança sem "sim" para cada ação.
- Conta pequena: não chamar vencedor ou perdedor com menos conversões que o mínimo de
  `regras.md`; diga "ainda em OBSERVAR".
- Nunca inventar número. Dado que não veio aparece como FALTANDO.
- Se for rodar como tarefa agendada, o brief não pode tomar nenhuma ação: só entregar o texto.
