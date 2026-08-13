import requests
import json

base_url = "http://localhost:8085"

# 1. Login as app member (form params, not JSON)
login_resp = requests.post(f"{base_url}/sso/login", data={"username": "test", "password": "123456"})
print("=== Login ===")
print(f"  status: {login_resp.status_code}")
login_data = login_resp.json()
print(f"  code: {login_data.get('code')}")
token = login_data.get("data", {}).get("token", "")
print(f"  token: {token[:30]}..." if token else "  token: None")

if token:
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Check coupon list visible to user
    list_resp = requests.get(f"{base_url}/member/coupon/list", headers=headers, params={"useStatus": 0})
    print()
    print("=== My Coupons (useStatus=0) ===")
    print(f"  status: {list_resp.status_code}")
    print(f"  body: {json.dumps(list_resp.json(), ensure_ascii=False, indent=2)}")

    # 3. Check coupons available for product 33 (小米电视4A)
    prod_resp = requests.get(f"{base_url}/member/coupon/listByProduct/33", headers=headers)
    print()
    print("=== Coupons for Product 33 ===")
    print(f"  status: {prod_resp.status_code}")
    print(f"  body: {json.dumps(prod_resp.json(), ensure_ascii=False, indent=2)}")
