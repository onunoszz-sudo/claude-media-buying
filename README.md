# claude-media-buying

*English: [README.en.md](README.en.md)*

Pacote de skills para operar Meta Ads e Google Ads com o Claude, no modelo **o Claude propõe,
você aprova**. Dois plugins no mesmo repositório:

| Plugin | Idioma | Para quê |
|---|---|---|
| `media-buying` | português | contas no Brasil e LATAM (low-ticket, delivery, lead → CRM, hotel) |
| `media-buying-en` | inglês | agências e clientes americanos, relatórios em inglês, carteira de hotéis |

Tipos de conta cobertos: **venda direta** (ROAS/MER sobre a venda real), **low-ticket** (CPA da
venda e ticket efetivo com bump/upsell), **lead → CRM** (CPL, custo por MQL e orçamento) e
**hotel** (custo de venda contra a comissão da OTA, líquido de cancelamento).

## Skills (v0.5)
| Português | Inglês | Quando usar | Frequência |
|---|---|---|---|
| `numeros-da-conta` | `account-numbers` | conta nova, mudança de preço/margem/comissão | onboarding, revisão trimestral |
| `brief-diario` | `daily-brief` | "o que precisa de mim hoje" | toda manhã |
| `revisao-meta` | `meta-review` | MATAR / OBSERVAR / ESCALAR, estágio que vaza, fadiga | diária, funda na segunda |
| `diagnostico-anuncio` | `ad-diagnosis` | anúncio surpreendeu, vendas caíram de repente | quando acontecer |
| `termos-de-pesquisa` | `search-terms` | negativas do Google Ads | terça |
| `saude-google-ads` | `google-ads-health` | check-up das campanhas do Google | terça |
| `pacing-de-verba` | `budget-pacing` | gasto do mês contra o orçamento contratado | todo dia / sexta |
| `relatorio-semanal` | `weekly-report` | relatório interno e versão cliente | segunda |
| `log-de-aprendizados` | `learnings-log` | regras da conta com evidência | segunda |
| `qa-de-lancamento` | `launch-qa` | conta contra o plano escrito, antes de subir e 72 h depois (só lê) | todo lançamento |
| `rodada-de-teste` | `test-round` | quantos anúncios a verba julga, hipótese e decisão por anúncio | quinta, a cada rodada |
| `multiplicador-de-vencedor` | `winner-multiplier` | por que ganhou, variações de uma variável, roteiro em blocos, resgate de hook, RSA | quinta, quando há vencedor |
| `mapa-de-angulos` | `angle-map` | grade ângulo x pessoa x formato a partir das palavras reais dos clientes, casas vazias e ganchos com checagem de política | terça, antes de cada rodada |
| `conferencia-de-rastreamento` | `tracking-check` | pixel x venda real dia a dia: casamento, compra sem valor, contagem dobrada, venda sumindo; diz se dá para julgar anúncio (só lê) | 1x por mês e depois de mudar checkout/funil |

Próximas: auditoria de funil, speed-to-lead, feed de hotel (Hotel Center).

**Novidades da v0.5:** venda real por anúncio (origem da venda na plataforma de pagamento) e
"custo extra" na `revisao-meta`; escada de verba (subir, segurar, descer um degrau); regra de
"piora geral não é fadiga"; os 3 piores por custo extra no `relatorio-semanal`; diário de
mudanças da conta (`diario.md`); anúncio reprovado vira linha no `marca.md`; `mapa-de-angulos`.

## Contexto de cada conta
Toda skill lê a pasta da conta no seu projeto: `contas/<slug>/` (PT) ou `accounts/<slug>/` (EN).
Rode `numeros-da-conta` / `account-numbers` para criar os 6 arquivos a partir dos modelos:
números, marca, ofertas, vencedores, regras e aprendizados, mais o `diario.md` de mudanças. A `qa-de-lancamento` acrescenta o
`plano-de-lancamento.md` e a `rodada-de-teste`, o `testes.md`.
**Os dados das contas ficam no seu projeto, nunca neste repositório.**

## Scripts (só biblioteca padrão do Python 3)
- `calc_numeros.py`: breakeven, alvos, CPA/CPL e o modo hotel, com a conta aberta. `--lang pt|en`.
- `calc_pacing.py`: pacing do portfólio a partir de um CSV, com status, diário recomendado e passos
  de até 20%. `--lang pt|en`.
- `calc_rodada.py`: quantos anúncios cabem numa rodada de teste (verba x dias ÷ linha de MATAR).
  `--lang pt|en`.

Os scripts são idênticos nos dois plugins. Edite no plugin em português e copie para o inglês.

## Conectores e automação
Guia completo em [connectors/README.md](connectors/README.md): conector oficial da Meta
(personalizado no Claude, lê e escreve) e servidor oficial do Google Ads (local, só leitura), os
dois gratuitos, mais as tarefas agendadas de só leitura.

## Rotina semanal sugerida
- **Todo dia:** `brief-diario` + pacing; aprovar ou pular as ações.
- **Segunda:** `revisao-meta`, `relatorio-semanal`, `log-de-aprendizados`.
- **Terça:** `saude-google-ads`, `termos-de-pesquisa` e `mapa-de-angulos`.
- **Quarta:** consertar o pós-clique (`diagnostico-anuncio`).
- **Quinta:** `rodada-de-teste` e `multiplicador-de-vencedor`; `qa-de-lancamento` antes de subir
  e de novo 72 h depois.
- **Sexta:** `pacing-de-verba` e passos de verba para a semana seguinte.

## Guardrails (valem para todas as skills)
1. Nada muda nas contas sem um "sim" para aquela ação específica.
2. Primeira semana: só leitura.
3. Pausar, nunca apagar.
4. Verba: no máximo +20% por passo, um passo a cada 48 h por campanha ou conjunto.
5. Amostra pequena fica em OBSERVAR.
6. Nunca inventar número ou promessa: dado ausente aparece como FALTANDO.
7. O pixel não é fonte de verdade de venda.
8. O Claude não lê nem copia token, chave ou senha.

## Instalação (5 minutos)
Precisa do **Claude Code** (no terminal, no app desktop ou na extensão do VS Code), com um plano
pago do Claude.

1. Abra o Claude Code e digite, uma linha de cada vez:
   ```
   /plugin marketplace add onunoszz-sudo/claude-media-buying
   /plugin install media-buying@claude-media-buying
   ```
   Para a versão em inglês, troque a segunda linha por
   `/plugin install media-buying-en@claude-media-buying` (pode instalar as duas).
2. Feche e abra o Claude Code de novo. As skills passam a aparecer no menu `/`.
3. Crie uma pasta para o seu trabalho de tráfego, abra o Claude Code nela e peça
   **"números da conta"** para a primeira conta. Ele cria `contas/<nome-da-conta>/` com os arquivos
   que todas as outras skills leem.
4. Conecte os dados (opcional, mas é o que deixa tudo automático): siga
   [connectors/README.md](connectors/README.md) para o conector oficial da Meta e o do Google Ads.
   Sem conector, as skills funcionam com o export do Gerenciador de Anúncios colado na conversa.

**Atualizar para uma versão nova:** `/plugin marketplace update claude-media-buying`.

Sem `/plugin` disponível, copie as pastas de `plugins/<plugin>/skills/` para `~/.claude/skills/`.

## Créditos
Método adaptado, com texto próprio, de quatro materiais públicos: *The Claude Media Buying Team* e
*The Claude Code Paid Ads Team* (Paul Ryan Jones, ORIRI Marketing), *The Meta + Google Ads Agent* e
*12 Claude Agents for Meta Ads* (Dusan Radovanovic, Hook & Scale).
Nenhum texto, prompt ou arquivo desses materiais foi copiado.
