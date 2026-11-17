# Conectores: Meta Ads e Google Ads (custo zero)

*English version: [README.en.md](README.en.md)*

Com os dois conectores ligados, as skills leem as contas direto, sem export, e as tarefas
agendadas (brief diário, revisão de segunda, pacing de sexta) podem rodar sozinhas. Os dois
caminhos abaixo são oficiais e gratuitos. As opções do diretório de conectores do Claude para
anúncios (Supermetrics, Windsor.ai, Adspirer, Funnel) são pagas.

| | Meta Ads | Google Ads |
|---|---|---|
| Quem publica | Meta (conector oficial, beta desde 2026-04-29) | Google (`googleads/google-ads-mcp`, código aberto) |
| Onde roda | servidor da Meta, conector personalizado no Claude | local, no seu computador, via `uvx` |
| Acesso | **lê e escreve** (cria campanha pausada, muda orçamento, pausa) | **só leitura** |
| O que você precisa | login do Facebook com acesso às contas | developer token, projeto no Google Cloud, credencial OAuth |
| Tempo | 2 minutos | 30 a 45 minutos, mais a espera do token se ele não vier aprovado |

## Regra de segurança que vale para os dois
O Claude propõe e você aprova. As skills nunca chamam uma ferramenta de escrita sem um "sim" para
aquela ação, e o Claude **não lê, não copia e não cola** token, chave ou senha: esses valores vão
direto para arquivos locais que só você edita.

## 1. Meta Ads
1. claude.ai → **Personalizar → Conectores → Agregar → Agregar conector personalizado**.
2. Nome: `Meta Ads` · URL: `https://mcp.facebook.com/ads` → **Continuar → Agregar** (deixe a
   autenticação como detectada).
3. Clique em **Conectar**. Entre com o Facebook que tem acesso às contas, escolha **só** os
   negócios e páginas que o Claude deve ver e aceite os termos da Meta.
4. Num chat novo, confira que o conector **Meta Ads** está ligado e peça: "liste as contas de
   anúncio que você vê e o gasto dos últimos 7 dias de cada uma". Não mude nada nos primeiros dias.

Se aparecer "conta não habilitada": a Meta libera o conector aos poucos. Até lá, use o export CSV
do Gerenciador (nível Anúncio) com as mesmas skills.

O conector recebe as mesmas permissões que o seu login tem na conta. Quem protege a conta são os
guardrails das skills e o seu hábito de nunca aprovar uma ação sem ler.

## 2. Google Ads
### 2.1 Nível de acesso da API (no projeto do Google Cloud)
Desde 2026 o acesso da Google Ads API é gerenciado **no projeto do Google Cloud**, não mais pelo
formulário da Central de API do Google Ads. Aquele formulário agora serve só para a "App
Conversion Tracking and Remarketing API": não use para isto.
1. Depois de criar o projeto e ativar a API (2.2), abra **APIs e serviços → Google Ads API →
   Access levels → Manage**.
2. O projeto começa em **Test**, que só lê contas de teste. Em **Upgrade access level →
   Explorer**, clique em **Apply for access**. O pedido é enviado **no clique**, sem formulário,
   e fica "under review" por alguns minutos.
3. Com Explorer aprovado, o developer token é **opcional**: deixe a linha do `.env` como está,
   a menos que você já tenha um token antigo.

### 2.2 Projeto no Google Cloud (você)
1. console.cloud.google.com → crie um projeto (ex.: `ads-mcp`) e anote o **ID do projeto**.
2. **APIs e serviços → Biblioteca →** ative a **Google Ads API**.
3. **Google Auth Platform (tela de consentimento OAuth):** tipo Externo, nome do app, seu e-mail.
   Para publicar em **Em produção**, o Google exige URL do site e da política de privacidade no
   Branding. Sem elas, deixe em **Teste**, adicione seu e-mail em **Usuários de teste** e rode
   `gerar_credencial.py` de novo a cada 7 dias (a credencial de app em teste expira).
4. **Clientes → Criar cliente → App para computador →** baixe o JSON e salve como
   `%USERPROFILE%\.config\google-ads-mcp\client_secret.json`.

### 2.3 Credencial e token no computador
1. Gere a credencial (abre o navegador; autorize com a conta Google que acessa a MCC):
   ```bash
   python connectors/google-ads/gerar_credencial.py
   ```
   Ela é gravada em `%USERPROFILE%\.config\google-ads-mcp\adc.json`. Nada é impresso na tela.
2. Abra `%USERPROFILE%\.config\google-ads-mcp\.env` (modelo em `google-ads/env.exemplo`) e preencha
   `GOOGLE_PROJECT_ID` e, se usar MCC, `GOOGLE_ADS_LOGIN_CUSTOMER_ID` (só números).
   `GOOGLE_ADS_DEVELOPER_TOKEN` é opcional (ver 2.1).

### 2.4 Ligar no Claude Code
No projeto onde você trabalha, um `.mcp.json` com:
```json
{
  "mcpServers": {
    "google-ads": {
      "command": "python",
      "args": ["<caminho do repo>\\connectors\\google-ads\\iniciar_servidor.py"]
    }
  }
}
```
Reinicie o app e aprove o servidor `google-ads` quando ele perguntar. O lançador confere o `.env`
e a credencial antes de iniciar; se faltar algo, ele para com a mensagem do que falta.
Teste: "quais contas do Google Ads você acessa?" (ferramenta `list_accessible_customers`).

## 3. Automação (depois que os dois responderem)
Com os conectores funcionando, as tarefas agendadas rodam só leitura e salvam o resultado em
arquivo:

| Quando | Tarefa |
|---|---|
| Dias úteis, 8h | `brief-diario` do portfólio |
| Segunda, 9h | `revisao-meta` + `relatorio-semanal` + `log-de-aprendizados` (propostas) |
| Terça, 9h | `saude-google-ads` + `termos-de-pesquisa` |
| Sexta, 9h | `pacing-de-verba` |

Nenhuma tarefa agendada muda a conta: elas entregam a lista de ações, e você aprova numa conversa.

## Problemas comuns
- **"only approved for use with test accounts":** o projeto ainda está em Test. Peça Explorer
  em Google Ads API → Access levels (2.1).
- **`invalid_grant` depois de uma semana:** a tela de consentimento ficou em "Teste". Mude para
  "Em produção" e rode `gerar_credencial.py` de novo.
- **Sem `refresh_token`:** remova o acesso do app em myaccount.google.com/permissions e rode de novo.
- **Servidor não aparece no Claude:** confira o caminho no `.mcp.json`, o `uvx` no PATH e se você
  aprovou o servidor ao abrir o projeto.
