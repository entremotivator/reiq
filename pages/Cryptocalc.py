import streamlit as st
import requests

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Crypto to Property Calculator", layout="centered")

# ---- SIDEBAR ----
with st.sidebar:
    st.title("🔐 App Access")
    app_key = st.text_input("Enter App Key", type="password")

# ---- MAIN APP ----
st.title("🏡 Crypto to Property Calculator")
st.write("Convert your crypto to real estate buying power in USD or local currency")

if not app_key:
    st.warning("Please enter your App Key in the sidebar to use the calculator.")
    st.stop()

# ---- OPTIONS ----
cryptos = {
    "Bitcoin (BTC)": "bitcoin",
    "Ethereum (ETH)": "ethereum",
    "Solana (SOL)": "solana",
    "Tether (USDT)": "tether"
}

currencies = ["USD", "EUR", "GBP", "CAD", "AUD", "JPY", "NGN", "INR"]

# ---- USER INPUTS ----
selected_crypto = st.selectbox("🔁 Select your Cryptocurrency", list(cryptos.keys()))
crypto_amount = st.number_input("💰 Amount of Crypto", min_value=0.0, format="%.6f")
target_currency = st.selectbox("🌍 Convert to Currency", currencies)
property_cost = st.number_input(f"🏠 Property Cost in {target_currency}", min_value=0.0, step=1000.0)

# ---- API CALLS ----
@st.cache_data
def get_crypto_price(crypto_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data[crypto_id]['usd']

@st.cache_data
def get_usd_to_currency_rate(currency_code):
    url = f"https://api.exchangerate.host/latest?base=USD&symbols={currency_code}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data['rates'][currency_code]

# ---- CONVERSION LOGIC ----
if st.button("🔄 Convert"):
    crypto_id = cryptos[selected_crypto]
    with st.spinner("Fetching live prices..."):
        try:
            crypto_usd = get_crypto_price(crypto_id)
            usd_total = crypto_usd * crypto_amount

            if target_currency != "USD":
                rate = get_usd_to_currency_rate(target_currency)
                converted = usd_total * rate
            else:
                rate = 1.0
                converted = usd_total

            st.success(f"💹 {crypto_amount} {selected_crypto.split()[0]} = {converted:,.2f} {target_currency}")

            if converted >= property_cost:
                st.markdown(f"✅ You can afford the property worth **{property_cost:,.2f} {target_currency}** 🎉")
                st.balloons()
            else:
                shortfall = property_cost - converted
                st.markdown(f"❌ You need **{shortfall:,.2f} {target_currency}** more to buy this property.")

        except Exception as e:
            st.error("Error fetching live data. Please try again later.")
            st.code(str(e))
