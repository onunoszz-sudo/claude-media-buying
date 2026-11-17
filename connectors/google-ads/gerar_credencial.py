"""Gera a credencial OAuth (Application Default Credentials) para o servidor MCP do Google Ads.

Roda o fluxo "app para computador" do Google com PKCE e porta local, so com biblioteca
padrao. O navegador abre, voce autoriza com a conta Google que tem acesso a MCC, e o
arquivo de credencial e gravado direto em disco. Nenhum segredo e impresso na tela.

Uso:
  python gerar_credencial.py
  python gerar_credencial.py --client-json C:\\caminho\\client_secret.json --saida C:\\caminho\\adc.json

Padroes: le e grava em %USERPROFILE%\\.config\\google-ads-mcp\\
"""
import argparse
import base64
import hashlib
import http.server
import json
import os
import secrets
import sys
import threading
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path

PASTA = Path.home() / ".config" / "google-ads-mcp"
ESCOPOS = "https://www.googleapis.com/auth/adwords"


def ler_cliente(caminho):
    if not caminho.exists():
        sys.exit(f"ERRO: nao achei {caminho}. Baixe o JSON do ID do cliente OAuth (tipo "
                 "'App para computador') no Google Cloud e salve com esse nome.")
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    bloco = dados.get("installed") or dados.get("web")
    if not bloco:
        sys.exit("ERRO: o JSON nao e de um cliente OAuth. Crie um 'App para computador'.")
    return bloco


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--client-json", type=Path, default=PASTA / "client_secret.json")
    p.add_argument("--saida", type=Path, default=PASTA / "adc.json")
    a = p.parse_args()

    cliente = ler_cliente(a.client_json)
    verificador = secrets.token_urlsafe(64)
    desafio = base64.urlsafe_b64encode(hashlib.sha256(verificador.encode()).digest()).rstrip(b"=").decode()
    estado = secrets.token_urlsafe(16)
    recebido = {}

    class Receptor(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            recebido.update({k: v[0] for k, v in q.items()})
            ok = "code" in q and q.get("state", [""])[0] == estado
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            msg = "Autorizado. Pode fechar esta aba e voltar ao terminal." if ok else "Falhou. Volte ao terminal."
            self.wfile.write(f"<p style='font-family:sans-serif'>{msg}</p>".encode())

        def log_message(self, *args):
            pass

    servidor = http.server.HTTPServer(("127.0.0.1", 0), Receptor)
    redirect = f"http://127.0.0.1:{servidor.server_port}/"
    url = cliente.get("auth_uri", "https://accounts.google.com/o/oauth2/auth") + "?" + urllib.parse.urlencode({
        "client_id": cliente["client_id"],
        "redirect_uri": redirect,
        "response_type": "code",
        "scope": ESCOPOS,
        "access_type": "offline",
        "prompt": "consent",
        "state": estado,
        "code_challenge": desafio,
        "code_challenge_method": "S256",
    })

    t = threading.Thread(target=servidor.handle_request, daemon=True)
    t.start()
    print("Abrindo o navegador para autorizar o acesso ao Google Ads...")
    print("Se nao abrir, copie este endereco no navegador:\n" + url + "\n")
    webbrowser.open(url)
    t.join(timeout=300)
    servidor.server_close()

    if recebido.get("state") != estado or "code" not in recebido:
        sys.exit(f"ERRO: autorizacao nao concluida ({recebido.get('error', 'sem resposta em 5 min')}).")

    corpo = urllib.parse.urlencode({
        "code": recebido["code"],
        "client_id": cliente["client_id"],
        "client_secret": cliente.get("client_secret", ""),
        "redirect_uri": redirect,
        "grant_type": "authorization_code",
        "code_verifier": verificador,
    }).encode()
    req = urllib.request.Request(cliente.get("token_uri", "https://oauth2.googleapis.com/token"), data=corpo)
    try:
        resposta = json.loads(urllib.request.urlopen(req, timeout=30).read())
    except urllib.error.HTTPError as e:
        sys.exit(f"ERRO na troca do codigo: HTTP {e.code}. Confira se o cliente e 'App para computador'.")
    if "refresh_token" not in resposta:
        sys.exit("ERRO: o Google nao devolveu refresh_token. Remova o acesso do app em "
                 "myaccount.google.com/permissions e rode de novo.")

    a.saida.parent.mkdir(parents=True, exist_ok=True)
    a.saida.write_text(json.dumps({
        "type": "authorized_user",
        "client_id": cliente["client_id"],
        "client_secret": cliente.get("client_secret", ""),
        "refresh_token": resposta["refresh_token"],
    }, indent=2), encoding="utf-8")
    try:
        os.chmod(a.saida, 0o600)
    except OSError:
        pass
    print(f"Credencial gravada em: {a.saida}")
    print("Proximo passo: conferir o .env na mesma pasta e reiniciar o Claude.")


if __name__ == "__main__":
    main()
