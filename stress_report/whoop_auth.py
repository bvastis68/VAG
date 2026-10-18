"""One-time WHOOP OAuth sign-in. Saves tokens to .env on this machine.

Usage:
    python3 stress_report/whoop_auth.py            # catches the redirect on localhost
    python3 stress_report/whoop_auth.py --manual   # paste the redirect URL into this terminal

Never paste the redirect URL, code, or tokens into a chat.
"""
import argparse
import http.server
import json
import secrets
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser

from envfile import load_env, require, update_env

AUTH_URL = "https://api.prod.whoop.com/oauth/oauth2/auth"
TOKEN_URL = "https://api.prod.whoop.com/oauth/oauth2/token"
SCOPES = "offline read:recovery read:cycles read:workout read:sleep read:profile"
DEFAULT_REDIRECT = "http://localhost:8765/callback"


def post_token(form):
    body = urllib.parse.urlencode(form).encode()
    req = urllib.request.Request(
        TOKEN_URL, data=body, headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as err:
        raise SystemExit(f"WHOOP token request failed: HTTP {err.code} {err.read().decode()[:300]}")


def save_tokens(tok):
    update_env({
        "WHOOP_ACCESS_TOKEN": tok["access_token"],
        "WHOOP_REFRESH_TOKEN": tok.get("refresh_token", ""),
        "WHOOP_TOKEN_EXPIRES_AT": str(int(time.time()) + int(tok.get("expires_in", 3600)) - 60),
    })


def refresh(env):
    """Swap the refresh token for a new access token. WHOOP rotates the refresh token too."""
    require(env, "WHOOP_CLIENT_ID", "WHOOP_CLIENT_SECRET", "WHOOP_REFRESH_TOKEN")
    tok = post_token({
        "grant_type": "refresh_token",
        "refresh_token": env["WHOOP_REFRESH_TOKEN"],
        "client_id": env["WHOOP_CLIENT_ID"],
        "client_secret": env["WHOOP_CLIENT_SECRET"],
        "scope": "offline",
    })
    save_tokens(tok)
    return load_env()


def catch_redirect(redirect_uri):
    parsed = urllib.parse.urlparse(redirect_uri)
    result = {}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            if urllib.parse.urlparse(self.path).path != parsed.path:
                self.send_response(404)
                self.end_headers()
                return
            result.update(urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query))
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h2>WHOOP connected. You can close this tab.</h2>")

        def log_message(self, *args):
            pass

    server = http.server.HTTPServer((parsed.hostname, parsed.port or 80), Handler)
    server.timeout = 300
    while not result:
        server.handle_request()
    server.server_close()
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--manual", action="store_true", help="paste the redirect URL instead of catching it")
    args = ap.parse_args()

    env = load_env()
    require(env, "WHOOP_CLIENT_ID", "WHOOP_CLIENT_SECRET")
    redirect_uri = env.get("WHOOP_REDIRECT_URI") or DEFAULT_REDIRECT
    state = secrets.token_urlsafe(16)

    url = AUTH_URL + "?" + urllib.parse.urlencode({
        "response_type": "code",
        "client_id": env["WHOOP_CLIENT_ID"],
        "redirect_uri": redirect_uri,
        "scope": SCOPES,
        "state": state,
    })
    print("Opening WHOOP sign-in in your browser. If it doesn't open, visit:\n\n" + url + "\n")
    webbrowser.open(url)

    if args.manual:
        pasted = input("After approving, paste the FULL URL from the browser address bar here: ").strip()
        params = urllib.parse.parse_qs(urllib.parse.urlparse(pasted).query)
    else:
        print(f"Waiting for WHOOP to redirect to {redirect_uri} ...")
        params = catch_redirect(redirect_uri)

    if "error" in params:
        raise SystemExit(f"WHOOP returned an error: {params['error'][0]} {params.get('error_description', [''])[0]}")
    if params.get("state", [None])[0] != state:
        raise SystemExit("State mismatch. Aborting (possible stale or forged redirect). Run again.")

    tok = post_token({
        "grant_type": "authorization_code",
        "code": params["code"][0],
        "client_id": env["WHOOP_CLIENT_ID"],
        "client_secret": env["WHOOP_CLIENT_SECRET"],
        "redirect_uri": redirect_uri,
    })
    save_tokens(tok)
    if not tok.get("refresh_token"):
        print("Warning: no refresh token returned. Check the 'offline' scope is enabled on your WHOOP app.")
    print("Done. Tokens saved to .env (owner-only permissions). Next: python3 stress_report/whoop_pull.py")


if __name__ == "__main__":
    sys.exit(main())
