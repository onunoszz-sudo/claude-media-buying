# Números: <nome da conta>

> Gerado por `numeros-da-conta` em AAAA-MM-DD. Revisar a cada trimestre ou quando preço,
> margem ou oferta mudarem.

- **Tipo de funil:** venda-direta | low-ticket | lead-crm
- **Fonte de verdade das vendas:** <Hotmart | Cardápio Web | planilha X | CRM Y> (o pixel
  da plataforma nunca é a fonte de verdade)
- **Moeda das vendas / moeda da verba:** <BRL / BRL>

## Entradas (com origem de cada número)
| Entrada | Valor | De onde veio |
|---|---|---|
| Ticket médio (ou front, bump, upsell e taxas) | | |
| Margem de contribuição | | |
| Lucro desejado depois dos anúncios | | |
| Taxas do funil (só lead-crm: lead → MQL → orçamento → venda) | | |
| Verba mensal e divisão entre plataformas | | |

## Números de decisão
<colar a saída de `calc_numeros.py`>

## Limiares de rótulo (padrão; ajustar em regras.md depois de 2 semanas)
- **MATAR:** gastou 2x o CPA alvo sem conversão, ou CPA 50%+ acima do alvo por 3 dias.
- **OBSERVAR:** menos de 72 h no ar, em aprendizado, menos de <N> conversões, ou entre
  breakeven e alvo.
- **ESCALAR:** acima do alvo por 3+ dias com <N>+ conversões, CPA e frequência estáveis.
- **Janela de julgamento:** <30 dias; 7 a 14 em conta pequena>.

## Contas e acessos
- Meta: <conta de anúncios / ID> · leitura por <conector oficial | export CSV>
- Google Ads: <ID> · leitura por <CSV semanal | navegador | MCP>
