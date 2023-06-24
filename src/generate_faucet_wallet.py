import json
from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet


JSON_RPC_URL = "https://s.altnet.rippletest.net:51234"
client = JsonRpcClient(JSON_RPC_URL)

# wallet 생성
wallet = generate_faucet_wallet(client, debug=True)

# wallet 정보를 JSON 파일로 저장
wallet_info = wallet.__dict__

print(wallet_info)

with open("destination.json", "w", encoding="UTF-8") as f:
    json.dump(wallet_info, f)
