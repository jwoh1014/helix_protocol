from xrpl.models.transactions import Payment
from xrpl.transaction import send_reliable_submission

# 보낼 목적지 주소를 설정합니다.
destination_address = "rU6K7V3Po4snVhBBaU29sesqs2qTQJWDw1"  # 이 주소는 예시입니다.

# 보낼 금액을 설정합니다. (단위: 드랍)
amount = "100000000"  # 100 XRP

# 지급(Payment) 트랜잭션을 생성합니다.
payment = Payment(
    account=wallet.classic_address,
    amount=amount,
    destination=destination_address,
)

# 트랜잭션을 전송하고, 그 결과를 받아옵니다.
response = send_reliable_submission(payment, wallet, client)

# 결과를 출력합니다.
print("Transaction result:", response.result["engine_result"])
print("Transaction hash:", response.result["tx_json"]["hash"])
