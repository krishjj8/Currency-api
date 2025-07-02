from fastapi import FastAPI, HTTPException
import requests
import os
from dotenv import load_dotenv

# ✅ Load environment variables from .env file
load_dotenv(dotenv_path=".env")

# ✅ Read API key from environment
API_KEY = os.getenv("EXCHANGE_API_KEY")
print("🔑 Loaded API KEY:", API_KEY)  # Only for debugging — remove in production

# ✅ Base URL for the external API
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}"

# ✅ Initialize FastAPI app
app = FastAPI(title="Currency Exchange API")

# ✅ Route to get latest exchange rates
@app.get("/latest/{base}")
def get_latest(base: str):
    url = f"{BASE_URL}/latest/{base.upper()}"
    resp = requests.get(url)
    print("🌐 GET:", url)  # Debug
    if resp.status_code != 200:
        print("❌ API Error:", resp.status_code, resp.text)  # Debug
        raise HTTPException(status_code=502, detail="External API error")
    return resp.json()

# ✅ Route to convert currency
@app.get("/convert/{base}/{target}/{amount}")
def convert_currency(base: str, target: str, amount: float):
    data = get_latest(base)
    rates = data.get("conversion_rates", {})
    rate = rates.get(target.upper())
    if rate is None:
        raise HTTPException(404, detail="Target currency not supported")
    return {
        "base": base.upper(),
        "target": target.upper(),
        "rate": rate,
        "amount": amount,
        "converted": round(amount * rate, 2)
    }
