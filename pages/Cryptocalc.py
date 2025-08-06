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
st.write("Convert your crypto into real estate buying power in USD or local currency — no API key needed!")

if not app_key:
    st.warning("Please enter your App Key in the sidebar to use the calculator.")
    st.stop()

# ---- CRYPTO & CURRENCY OPTIONS ----
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

# ---- FETCH PRICE FUNCTIONS (FREE APIs) ----
@st.cache_data(ttl=300)
def get_crypto_price_usd(crypto_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd"
    res = requests.get(url)
    res.raise_for_status()
    return res.json()[crypto_id]["usd"]

@st.cache_data(ttl=300)
def get_usd_to_currency_rate(currency_code):
    if currency_code == "USD":
        return 1.0
    url = f"https://api.exchangerate.host/latest?base=USD&symbols={currency_code}"
    res = requests.get(url)
    res.raise_for_status()
    return res.json()["rates"][currency_code]

# ---- CONVERSION ----
if st.button("🔄 Convert"):
    with st.spinner("Calculating conversion..."):
        try:
            crypto_id = cryptos[selected_crypto]
            price_usd = get_crypto_price_usd(crypto_id)
            total_usd = price_usd * crypto_amount
            exchange_rate = get_usd_to_currency_rate(target_currency)
            converted_value = total_usd * exchange_rate

            st.success(f"💹 {crypto_amount} {selected_crypto.split()[0]} = {converted_value:,.2f} {target_currency}")

            # Affordability check
            if converted_value >= property_cost:
                st.markdown(f"✅ You can afford the property worth **{property_cost:,.2f} {target_currency}** 🎉")
                st.balloons()
            else:
                shortfall = property_cost - converted_value
                st.markdown(f"❌ You need **{shortfall:,.2f} {target_currency}** more to buy this property.")

        except Exception as e:
            st.error("Something went wrong. Please try again later.")
            st.exception(e)
