---
name: saude-google-ads
description: Check-up semanal das campanhas do Google Ads (Pesquisa, Demand Gen, Performance Max, YouTube) contra os números da conta - lucrativas limitadas por orçamento, abaixo do breakeven, saltos de CPC, URL final errada, lances e metas de conversão - e devolve 5 ações em passo a passo, separando o que o agente pode fazer do que só o responsável consegue. Use quando o usuário disser "saúde do Google Ads", "check-up das campanhas", "revisão do Google", "por que o Google está gastando mais", ou mandar o relatório de campanhas.
---

# Saúde do Google Ads

O Google vaza dinheiro em lugares silenciosos: campanha boa travada por orçamento, campanha
ruim que ninguém olha por dentro, anúncio mandando para a página errada, meta de conversão
contando a coisa errada. Esta skill faz o check-up e entrega as ações em passos exatos.

## Antes de começar
1. Leia `numeros.md`, `regras.md` e `aprendizados.md` da conta. Em `regras.md` está a
   tabela do que o agente pode fazer no Google Ads e do que só o responsável faz (por
   exemplo, ações que pedem verificação de identidade/passkey).
2. Dados, em ordem de preferência: MCP do Google Ads (se estiver nesta sessão), leitura da
   interface no navegador, ou relatório CSV de campanhas do período **e** do período
   anterior (para comparar). Diga a data do dado.

### Consultas prontas para o MCP do Google Ads (ferramenta `search`)
> Ferramenta `search` do servidor oficial: passe as partes separadas, não a consulta inteira. `resource` = o que vem depois do FROM, `fields` = a lista do SELECT, `conditions` = cada trecho do WHERE (ex.: `"segments.date DURING LAST_30_DAYS"`), `orderings` e `limit`. Na dúvida sobre um campo, use `metadata_get_resource_metadata`.

Rode para o período e para o período anterior (ex.: `LAST_14_DAYS` e um intervalo
`BETWEEN 'AAAA-MM-DD' AND 'AAAA-MM-DD'`). Custo e orçamento em micros (÷ 1.000.000).
```sql
-- campanhas: resultado, orçamento e verba perdida por orçamento
SELECT campaign.id, campaign.name, campaign.advertising_channel_type, campaign.status,
       campaign.bidding_strategy_type, campaign_budget.amount_micros,
       metrics.cost_micros, metrics.impressions, metrics.clicks, metrics.average_cpc,
       metrics.conversions, metrics.conversions_value,
       metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share
FROM campaign
WHERE segments.date DURING LAST_14_DAYS AND campaign.status = 'ENABLED'

-- metas de conversão: o que está contando como conversão
SELECT conversion_action.name, conversion_action.category, conversion_action.primary_for_goal,
       conversion_action.status
FROM conversion_action

-- URLs finais dos anúncios ativos
SELECT campaign.name, ad_group.name, ad_group_ad.ad.id, ad_group_ad.ad.final_urls
FROM ad_group_ad
WHERE ad_group_ad.status = 'ENABLED' AND campaign.status = 'ENABLED'

-- anúncios reprovados ou limitados
SELECT campaign.name, ad_group_ad.ad.id, ad_group_ad.policy_summary.approval_status
FROM ad_group_ad
WHERE ad_group_ad.policy_summary.approval_status != 'APPROVED' AND ad_group_ad.status = 'ENABLED'
```
O servidor oficial só lê. A expansão de URL final do Performance Max e os parceiros de pesquisa
conferem-se na interface.

## O que checar, por campanha
| Checagem | Sinal | Por que importa |
|---|---|---|
| ROAS/CPA contra `numeros.md` | abaixo do breakeven, entre breakeven e alvo, acima do alvo | decide cortar, manter ou crescer |
| Limitada por orçamento | lucrativa e "Limitada pelo orçamento" | dinheiro deixado na mesa |
| CPC | subiu 30%+ contra o período anterior | concorrência, qualidade ou lance |
| Meta de conversão | a campanha otimiza para a conversão certa? (lead real, compra, não visita) | otimizar para a coisa errada treina o algoritmo errado |
| URL final | todos os anúncios apontam para a página certa? Performance Max com expansão de URL final ligada? | tráfego indo para página que não converte |
| Termos de pesquisa | gasto sem conversão | rodar `termos-de-pesquisa` |
| Parceiros de pesquisa / Display em campanha de Pesquisa | ligados sem resultado | verba fora da busca |
| Performance Max | quanto vem de busca pela marca; força dos recursos | pode estar levando crédito de venda que viria de graça |
| Status | anúncio/palavra reprovada, campanha pausada por limite ou pagamento | entrega parada sem ninguém ver |

Para lead-crm, o resultado real da campanha é o que virou MQL/orçamento/venda no CRM ou na
planilha de vendas, não o lead da plataforma. Peça esse dado e cruze por campanha quando
houver UTM/gclid; se não houver atribuição, diga isso como a primeira ação.

## Saída
Sem travessão.

1. **Três linhas:** o que está bom, o que está vazando, o que fazer esta semana.
2. **Tabela:** campanha, tipo, gasto, conversões, valor, CPA/ROAS, variação contra o
   período anterior, status contra a meta, alerta.
3. **5 ações, a mais valiosa primeiro**, cada uma com:
   - o que fazer e o ganho esperado (com o número em que se apoia);
   - **quem faz:** "o agente pode fazer (com seu sim)" ou "só você (pede verificação)",
     conforme `regras.md`;
   - passo a passo exato na interface, em português e com o nome do menu em inglês quando a
     interface costuma abrir em inglês.
4. **Aprendizado candidato** para o `log-de-aprendizados`.

## Guardrails
- Nada muda sem "sim" para cada ação.
- Orçamento: no máximo +20% por passo, 48 h entre passos; respeitar pisos de orçamento já
  conhecidos em `regras.md`.
- Pausar, nunca remover campanha.
- Antes de reativar campanha pausada, conferir URL final de cada anúncio.
- Nunca inventar número; dado velho ou ausente é avisado.
