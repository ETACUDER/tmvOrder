"""
OAuth flow for Google Business Profile API to fetch food menus.
Run: python3 get_menu.py
"""
import json
import http.server
import urllib.parse
import webbrowser
import urllib.request
import ssl

# OAuth config — uses the same GCP project as the Maps API key
PROJECT_ID = "628338757341"
# We need to create OAuth credentials. Using OOB/loopback flow.
import os
CLIENT_ID = os.environ.get("YOUTUBE_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("YOUTUBE_CLIENT_SECRET", "")

SCOPES = "https://www.googleapis.com/auth/business.manage"
REDIRECT_URI = "http://localhost:8085"

token_result = {}

class OAuthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        if "code" in params:
            token_result["code"] = params["code"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Auth successful! Close this tab.</h1>")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"No code received")
    def log_message(self, *args):
        pass

def exchange_code(code, client_id, client_secret):
    data = urllib.parse.urlencode({
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data)
    ctx = ssl.create_default_context()
    resp = urllib.request.urlopen(req, context=ctx)
    return json.loads(resp.read())

def api_get(url, token):
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    ctx = ssl.create_default_context()
    try:
        resp = urllib.request.urlopen(req, context=ctx)
        return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"  HTTP {e.code}: {body[:1000]}")
        return {"error": e.code, "body": body}

def main():
    print("=" * 50)
    print("Google Business Profile - Food Menu Fetcher")
    print("=" * 50)
    print()
    client_id = CLIENT_ID
    client_secret = CLIENT_SECRET

    # Start local server
    server = http.server.HTTPServer(("localhost", 8085), OAuthHandler)

    # Open browser for auth
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={client_id}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"response_type=code&"
        f"scope={SCOPES}&"
        f"access_type=offline"
    )
    print(f"\nOpening browser for auth...")
    webbrowser.open(auth_url)

    # Wait for callback
    server.handle_request()

    if "code" not in token_result:
        print("Failed to get auth code")
        return

    print("Got auth code, exchanging for token...")
    tokens = exchange_code(token_result["code"], client_id, client_secret)
    access_token = tokens["access_token"]
    print("Got access token!")

    # List accounts
    print("\nFetching accounts...")
    accounts = api_get("https://mybusinessaccountmanagement.googleapis.com/v1/accounts", access_token)
    print(json.dumps(accounts, indent=2))

    if "accounts" not in accounts:
        print("No accounts found")
        return

    for acc in accounts["accounts"]:
        acc_name = acc["name"]
        print(f"\nAccount: {acc.get('accountName', acc_name)}")

        # List locations
        locations = api_get(
            f"https://mybusinessbusinessinformation.googleapis.com/v1/{acc_name}/locations?readMask=name,title",
            access_token
        )
        print(json.dumps(locations, indent=2))

        if "locations" not in locations:
            continue

        for loc in locations["locations"]:
            loc_name = loc["name"]
            print(f"\n  Location: {loc.get('title', loc_name)}")

            # Get food menus
            try:
                menus = api_get(
                    f"https://mybusiness.googleapis.com/v4/{acc_name}/{loc_name}/foodMenus",
                    access_token
                )

                # Save to file
                out_path = "/Volumes/CRESCENT/dev/exp/JVH/tmvOrder/food_menus.json"
                with open(out_path, "w") as f:
                    json.dump(menus, f, indent=2)
                print(f"\n  Menu saved to {out_path}")
                print(json.dumps(menus, indent=2)[:5000])
            except Exception as e:
                print(f"  Error fetching menu: {e}")

if __name__ == "__main__":
    main()
