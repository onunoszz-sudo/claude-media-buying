"""Inicia o servidor MCP oficial do Google Ads com as variaveis lidas de um .env local.

O cliente MCP (Claude Code / app do Claude) chama este script. Assim o developer token e
o caminho da credencial ficam so no .env, fora de qualquer arquivo de configuracao que
possa ser copiado ou sincronizado.

.env padrao: %USERPROFILE%\\.config\\google-ads-mcp\\.env (ou GOOGLE_ADS_MCP_ENV)
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

VERSAO = os.environ.get("GOOGLE_ADS_MCP_VERSION", "0.0.5")
ENV = Path(os.environ.get("GOOGLE_ADS_MCP_ENV", Path.home() / ".config" / "google-ads-mcp" / ".env"))
# Developer token e opcional: desde 2026 o nivel de acesso (Test/Explorer/Basic) fica no projeto do
# Google Cloud (Console > Google Ads API > Access levels). So e preciso para tokens antigos.
OBRIGATORIAS = ["GOOGLE_APPLICATION_CREDENTIALS", "GOOGLE_PROJECT_ID"]


def carregar_env(caminho):
    if not caminho.exists():
        sys.exit(f"google-ads-mcp: .env nao encontrado em {caminho}")
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, valor = linha.split("=", 1)
        valor = valor.strip().strip('"').strip("'")
        if valor and not valor.startswith("COLE_AQUI"):
            os.environ.setdefault(chave.strip(), os.path.expandvars(os.path.expanduser(valor)))


def main():
    carregar_env(ENV)
    faltando = [k for k in OBRIGATORIAS if not os.environ.get(k)]
    if faltando:
        sys.exit("google-ads-mcp: faltam no .env: " + ", ".join(faltando))
    if not Path(os.environ["GOOGLE_APPLICATION_CREDENTIALS"]).exists():
        sys.exit("google-ads-mcp: arquivo de credencial nao existe; rode gerar_credencial.py")
    uvx = shutil.which("uvx")
    if not uvx:
        sys.exit("google-ads-mcp: uvx nao encontrado no PATH (instale o uv)")
    sys.exit(subprocess.call([uvx, "--from", f"google-ads-mcp=={VERSAO}", "google-ads-mcp"]))


if __name__ == "__main__":
    main()
