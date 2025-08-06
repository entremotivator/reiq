import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import time
import json

# Page configuration
st.set_page_config(
    page_title="Bitcoin Real Estate Calculator Pro",
    page_icon="🏠₿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #f7931a 0%, #4a90e2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .price-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: white;
    }
    .metric-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem;
        border-left: 4px solid #f7931a;
    }
    .real-estate-card {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: white;
    }
    .calculator-section {
        background-color: #f8f9fa;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        border: 2px solid #e9ecef;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🏠₿ Bitcoin Real Estate Calculator Pro</h1>', unsafe_allow_html=True)
st.markdown("### 📊 Real-time Bitcoin prices with real estate investment calculator")

# Initialize session state
if 'price_history' not in st.session_state:
    st.session_state.price_history = []
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = False
if 'real_estate_history' not in st.session_state:
    st.session_state.real_estate_history = []

# Sidebar configuration
st.sidebar.title("⚙️ Settings & API Keys")
st.sidebar.markdown("---")

# API Key Inputs
st.sidebar.subheader("🔑 API Configuration")

# CoinDesk API (free, no key needed)
st.sidebar.success("✅ CoinDesk API: Active (Free)")

# Optional APIs for enhanced features
with st.sidebar.expander("🚀 Enhanced Features (Optional APIs)"):
    st.markdown("**Add API keys for premium features:**")
    
    # CoinGecko API for more crypto data
    coingecko_key = st.text_input(
        "CoinGecko API Key:",
        type="password",
        help="Get free API key from coingecko.com/en/api"
    )
    
    # Real Estate API (RentSpider, RealtyMole, etc.)
    real_estate_key = st.text_input(
        "RealtyMole API Key:",
        type="password",
        help="For live real estate data (realtymole.com)"
    )
    
    # News API for Bitcoin news
    news_api_key = st.text_input(
        "News API Key:",
        type="password",
        help="For Bitcoin news feed (newsapi.org)"
    )

st.sidebar.markdown("---")

# Auto-refresh toggle
auto_refresh = st.sidebar.checkbox("🔄 Auto-refresh (30s)", value=st.session_state.auto_refresh)
st.session_state.auto_refresh = auto_refresh

# Manual refresh button
col1, col2 = st.sidebar.columns(2)
with col1:
    fetch_data = st.button("🔄 Refresh Now", use_container_width=True)
with col2:
    clear_history = st.button("🗑️ Clear History", use_container_width=True)

if clear_history:
    st.session_state.price_history = []
    st.session_state.real_estate_history = []
    st.sidebar.success("History cleared!")

# Display preferences
st.sidebar.markdown("---")
st.sidebar.subheader("💱 Display Preferences")
show_currencies = st.sidebar.multiselect(
    "Select currencies:",
    options=["USD", "GBP", "EUR"],
    default=["USD", "GBP", "EUR"]
)

number_format = st.sidebar.selectbox(
    "Number format:",
    options=["With commas", "Clean"],
    index=0
)

# Real Estate Calculator Settings
st.sidebar.markdown("---")
st.sidebar.subheader("🏠 Real Estate Settings")
default_location = st.sidebar.selectbox(
    "Default location:",
    options=["New York, NY", "Los Angeles, CA", "Miami, FL", "Austin, TX", "Seattle, WA", "Denver, CO", "Custom"],
    index=0
)

if default_location == "Custom":
    custom_location = st.sidebar.text_input("Enter custom location:", "San Francisco, CA")
    default_location = custom_location

property_types = st.sidebar.multiselect(
    "Property types to show:",
    options=["Single Family Home", "Condo", "Townhouse", "Multi-Family", "Land"],
    default=["Single Family Home", "Condo"]
)

def format_price(price_str, currency, format_type):
    """Format price based on user preference"""
    if isinstance(price_str, str):
        clean_price = float(price_str.replace(',', ''))
    else:
        clean_price = float(price_str)
    
    if format_type == "With commas":
        formatted = f"{clean_price:,.2f}"
    else:
        formatted = f"{clean_price:.2f}"
    
    currency_symbols = {"USD": "$", "GBP": "£", "EUR": "€"}
    return f"{currency_symbols.get(currency, '')}{formatted}"

def fetch_bitcoin_price():
    """Fetch Bitcoin price from CoinDesk API"""
    try:
        with st.spinner("Fetching latest Bitcoin prices..."):
            url = "https://api.coindesk.com/v1/bpi/currentprice.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            updated_time = data["time"]["updated"]
            prices = {
                "USD": data["bpi"]["USD"]["rate"],
                "GBP": data["bpi"]["GBP"]["rate"],
                "EUR": data["bpi"]["EUR"]["rate"]
            }
            
            timestamp = datetime.now()
            usd_price_float = float(data["bpi"]["USD"]["rate"].replace(',', ''))
            
            st.session_state.price_history.append({
                "timestamp": timestamp,
                "price": usd_price_float,
                "updated": updated_time
            })
            
            if len(st.session_state.price_history) > 100:
                st.session_state.price_history = st.session_state.price_history[-100:]
            
            return prices, updated_time, True
            
    except Exception as e:
        st.error(f"🚫 Error fetching Bitcoin data: {str(e)}")
        return None, None, False

def fetch_enhanced_crypto_data(api_key):
    """Fetch additional crypto data with API key"""
    if not api_key:
        return None
    
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true"
        headers = {"x-cg-demo-api-key": api_key} if api_key else {}
        response = requests.get(url, headers=headers, timeout=10)
        return response.json() if response.status_code == 200 else None
    except:
        return None

# Auto-refresh logic
if auto_refresh:
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = 0
    
    current_time = time.time()
    if current_time - st.session_state.last_refresh > 30:
        fetch_data = True
        st.session_state.last_refresh = current_time

# Fetch data
if fetch_data or (auto_refresh and 'prices' not in st.session_state):
    prices, updated_time, success = fetch_bitcoin_price()
    
    if success:
        st.session_state.prices = prices
        st.session_state.updated_time = updated_time
        st.session_state.last_update = datetime.now()
        
        # Fetch enhanced data if API key provided
        if coingecko_key:
            enhanced_data = fetch_enhanced_crypto_data(coingecko_key)
            if enhanced_data:
                st.session_state.enhanced_data = enhanced_data

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Bitcoin Prices", "🏠 Real Estate Calculator", "📈 Investment Analysis", "📰 Market Insights"])

with tab1:
    # Display current prices
    if 'prices' in st.session_state:
        prices = st.session_state.prices
        updated_time = st.session_state.updated_time
        
        st.success("✅ Bitcoin prices fetched successfully!")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"**📅 Last Updated:** {updated_time}")
        with col2:
            if 'last_update' in st.session_state:
                time_diff = datetime.now() - st.session_state.last_update
                minutes_ago = int(time_diff.total_seconds() / 60)
                if minutes_ago < 1:
                    st.markdown("**🕐 Just now**")
                else:
                    st.markdown(f"**🕐 {minutes_ago} min{'s' if minutes_ago != 1 else ''} ago**")
        
        st.markdown("---")
        
        # Enhanced data display
        if 'enhanced_data' in st.session_state:
            enhanced = st.session_state.enhanced_data['bitcoin']
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("💰 Price (USD)", f"${enhanced['usd']:,.2f}")
            with col2:
                change_24h = enhanced.get('usd_24h_change', 0)
                st.metric("📈 24h Change", f"{change_24h:+.2f}%")
            with col3:
                market_cap = enhanced.get('usd_market_cap', 0)
                st.metric("🌐 Market Cap", f"${market_cap/1e9:.1f}B")
            with col4:
                volume = enhanced.get('usd_24h_vol', 0)
                st.metric("💱 24h Volume", f"${volume/1e9:.1f}B")
        
        # Current prices display
        st.subheader("💰 Current Prices")
        
        if show_currencies:
            cols = st.columns(len(show_currencies))
            
            currency_info = {
                "USD": {"flag": "🇺🇸", "name": "US Dollar"},
                "GBP": {"flag": "🇬🇧", "name": "British Pound"},
                "EUR": {"flag": "🇪🇺", "name": "Euro"}
            }
            
            for i, currency in enumerate(show_currencies):
                with cols[i]:
                    info = currency_info[currency]
                    formatted_price = format_price(prices[currency], currency, number_format)
                    
                    st.metric(
                        label=f"{info['flag']} {currency}",
                        value=formatted_price,
                        help=f"{info['name']} - {currency}"
                    )
        
        # Price history chart
        if len(st.session_state.price_history) >= 2:
            st.subheader("📊 Price History")
            
            df = pd.DataFrame(st.session_state.price_history)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df["timestamp"],
                y=df["price"],
                mode='lines+markers',
                name='Bitcoin Price (USD)',
                line=dict(color='#f7931a', width=2),
                marker=dict(size=6, color='#f7931a')
            ))
            
            fig.update_layout(
                title="Bitcoin Price Trend (This Session)",
                xaxis_title="Time",
                yaxis_title="Price (USD)",
                height=400,
                showlegend=False,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("👆 Click the **Refresh Now** button in the sidebar to get the latest Bitcoin prices.")

with tab2:
    st.markdown('<div class="calculator-section">', unsafe_allow_html=True)
    st.subheader("🏠₿ Bitcoin to Real Estate Calculator")
    
    # Get current Bitcoin price
    current_btc_price = 0
    if 'prices' in st.session_state:
        current_btc_price = float(st.session_state.prices['USD'].replace(',', ''))
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Bitcoin → Real Estate")
        btc_amount = st.number_input(
            "Bitcoin Amount:",
            min_value=0.001,
            max_value=1000.0,
            value=1.0,
            step=0.1,
            format="%.3f"
        )
        
        if current_btc_price > 0:
            usd_value = btc_amount * current_btc_price
            st.metric("💰 USD Value", f"${usd_value:,.2f}")
            
            # Property suggestions based on Bitcoin value
            st.markdown("**🏠 Property Options:**")
            
            if usd_value >= 1000000:
                st.success("🏰 Luxury Properties: Downtown penthouses, waterfront estates")
            elif usd_value >= 500000:
                st.success("🏡 Premium Properties: Luxury condos, large family homes")
            elif usd_value >= 250000:
                st.info("🏠 Standard Properties: Condos, townhouses, starter homes")
            elif usd_value >= 100000:
                st.info("🏘️ Entry-level Properties: Small condos, fixer-uppers")
            else:
                st.warning("💡 Consider: Down payment on properties, land investment")
            
            # Down payment calculator
            st.markdown("**📊 Down Payment Analysis:**")
            down_payment_pct = st.slider("Down Payment %:", 5, 50, 20)
            max_property_value = usd_value / (down_payment_pct / 100)
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("🏠 Max Property Value", f"${max_property_value:,.0f}")
            with col_b:
                monthly_payment = (max_property_value - usd_value) * 0.005  # Rough 6% APR estimate
                st.metric("💳 Est. Monthly Payment", f"${monthly_payment:,.0f}")
    
    with col2:
        st.markdown("#### Real Estate → Bitcoin")
        property_value = st.number_input(
            "Property Value (USD):",
            min_value=1000,
            max_value=10000000,
            value=500000,
            step=10000
        )
        
        if current_btc_price > 0:
            btc_equivalent = property_value / current_btc_price
            st.metric("₿ Bitcoin Equivalent", f"{btc_equivalent:.3f} BTC")
            
            # Historical comparison
            st.markdown("**📈 Historical Perspective:**")
            historical_prices = {
                "2020": 10000,
                "2021": 35000,
                "2022": 20000,
                "2023": 30000
            }
            
            for year, price in historical_prices.items():
                btc_then = property_value / price
                st.write(f"**{year}:** {btc_then:.2f} BTC (@ ${price:,})")
            
            # Investment scenarios
            st.markdown("**💡 Investment Scenarios:**")
            scenarios = {
                "Conservative (+10%/year)": 1.1,
                "Moderate (+25%/year)": 1.25,
                "Aggressive (+50%/year)": 1.5
            }
            
            for scenario, multiplier in scenarios.items():
                future_btc_value = btc_equivalent * current_btc_price * multiplier
                st.write(f"**{scenario}:** ${future_btc_value:,.0f} (1 year)")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Location-based analysis
    st.markdown("---")
    st.subheader(f"📍 Real Estate Analysis: {default_location}")
    
    # Sample property data (in real app, this would come from real estate API)
    sample_properties = {
        "New York, NY": {"avg_price": 1200000, "price_per_sqft": 1500, "avg_sqft": 800},
        "Los Angeles, CA": {"avg_price": 900000, "price_per_sqft": 750, "avg_sqft": 1200},
        "Miami, FL": {"avg_price": 600000, "price_per_sqft": 500, "avg_sqft": 1200},
        "Austin, TX": {"avg_price": 450000, "price_per_sqft": 300, "avg_sqft": 1500},
        "Seattle, WA": {"avg_price": 800000, "price_per_sqft": 600, "avg_sqft": 1333},
        "Denver, CO": {"avg_price": 550000, "price_per_sqft": 400, "avg_sqft": 1375}
    }
    
    if default_location in sample_properties:
        prop_data = sample_properties[default_location]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🏠 Average Price", f"${prop_data['avg_price']:,}")
        with col2:
            st.metric("📏 Price/Sq Ft", f"${prop_data['price_per_sqft']}")
        with col3:
            st.metric("📐 Average Size", f"{prop_data['avg_sqft']:,} sq ft")
        
        if current_btc_price > 0:
            btc_needed = prop_data['avg_price'] / current_btc_price
            st.info(f"**₿ You would need {btc_needed:.2f} Bitcoin to buy an average property in {default_location}**")

with tab3:
    st.subheader("📈 Investment Analysis & Projections")
    
    if 'prices' in st.session_state:
        current_btc_price = float(st.session_state.prices['USD'].replace(',', ''))
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔮 Future Value Projections")
            initial_investment = st.number_input("Initial Investment (USD):", min_value=100, value=10000, step=100)
            time_horizon = st.selectbox("Time Horizon:", ["1 Year", "2 Years", "5 Years", "10 Years"])
            
            growth_scenarios = {
                "Conservative (5%/year)": 0.05,
                "Moderate (15%/year)": 0.15,
                "Optimistic (30%/year)": 0.30,
                "Bull Market (100%/year)": 1.0
            }
            
            years = int(time_horizon.split()[0])
            
            st.markdown("**Projected Values:**")
            for scenario, rate in growth_scenarios.items():
                future_value = initial_investment * ((1 + rate) ** years)
                btc_amount = initial_investment / current_btc_price
                future_btc_value = btc_amount * current_btc_price * ((1 + rate) ** years)
                
                st.write(f"**{scenario}:** ${future_value:,.0f}")
        
        with col2:
            st.markdown("#### 🏠 Property Appreciation vs Bitcoin")
            
            # Real estate vs Bitcoin comparison
            real_estate_growth = 0.04  # 4% average annual appreciation
            bitcoin_growth = st.slider("Bitcoin Annual Growth %:", -20, 100, 25) / 100
            
            years_range = list(range(1, 11))
            re_values = [initial_investment * ((1 + real_estate_growth) ** year) for year in years_range]
            btc_values = [initial_investment * ((1 + bitcoin_growth) ** year) for year in years_range]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=years_range,
                y=re_values,
                mode='lines+markers',
                name='Real Estate (4%/year)',
                line=dict(color='#4CAF50', width=2)
            ))
            fig.add_trace(go.Scatter(
                x=years_range,
                y=btc_values,
                mode='lines+markers',
                name=f'Bitcoin ({bitcoin_growth*100:.0f}%/year)',
                line=dict(color='#f7931a', width=2)
            ))
            
            fig.update_layout(
                title="Investment Growth Comparison",
                xaxis_title="Years",
                yaxis_title="Investment Value ($)",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Portfolio allocation suggestions
        st.markdown("---")
        st.subheader("📊 Portfolio Allocation Suggestions")
        
        risk_tolerance = st.selectbox(
            "Risk Tolerance:",
            ["Conservative", "Moderate", "Aggressive", "Very Aggressive"]
        )
        
        allocations = {
            "Conservative": {"Bitcoin": 5, "Real Estate": 30, "Stocks": 40, "Bonds": 25},
            "Moderate": {"Bitcoin": 10, "Real Estate": 25, "Stocks": 50, "Bonds": 15},
            "Aggressive": {"Bitcoin": 20, "Real Estate": 30, "Stocks": 45, "Bonds": 5},
            "Very Aggressive": {"Bitcoin": 30, "Real Estate": 35, "Stocks": 35, "Bonds": 0}
        }
        
        allocation = allocations[risk_tolerance]
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_pie = px.pie(
                values=list(allocation.values()),
                names=list(allocation.keys()),
                title=f"{risk_tolerance} Portfolio Allocation",
                color_discrete_map={
                    "Bitcoin": "#f7931a",
                    "Real Estate": "#4CAF50",
                    "Stocks": "#2196F3",
                    "Bonds": "#FF9800"
                }
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            total_investment = st.number_input("Total Portfolio Value:", min_value=1000, value=100000, step=1000)
            
            st.markdown("**Suggested Allocation:**")
            for asset, percentage in allocation.items():
                amount = total_investment * (percentage / 100)
                if asset == "Bitcoin":
                    btc_amount = amount / current_btc_price
                    st.write(f"**{asset}:** ${amount:,.0f} ({btc_amount:.3f} BTC)")
                else:
                    st.write(f"**{asset}:** ${amount:,.0f}")

with tab4:
    st.subheader("📰 Market Insights & News")
    
    if news_api_key:
        # In a real app, fetch news from News API
        st.info("🔄 Loading latest Bitcoin and real estate news...")
        # Placeholder for news content
    else:
        st.info("💡 Add a News API key in the sidebar to see latest market news and insights.")
    
    # Market indicators (placeholder data)
    st.markdown("---")
    st.subheader("📊 Market Indicators")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📈 Bitcoin Metrics")
        st.metric("Fear & Greed Index", "45", "Neutral")
        st.metric("Hash Rate", "400 EH/s", "+5%")
        st.metric("Active Addresses", "950k", "+2%")
    
    with col2:
        st.markdown("#### 🏠 Real Estate Metrics")
        st.metric("Median Home Price", "$420k", "+3.2%")
        st.metric("Mortgage Rates", "6.8%", "+0.1%")
        st.metric("Housing Supply", "3.2 months", "-5%")
    
    with col3:
        st.markdown("#### 🌍 Economic Indicators")
        st.metric("Inflation Rate", "3.1%", "-0.2%")
        st.metric("Gold Price", "$2,045", "+1.5%")
        st.metric("DXY Index", "103.2", "-0.5%")
    
    # Educational content
    st.markdown("---")
    st.subheader("🎓 Educational Resources")
    
    with st.expander("💡 Bitcoin vs Real Estate Investment Guide"):
        st.markdown("""
        **Bitcoin Advantages:**
        - High growth potential
        - Liquidity (24/7 trading)
        - No maintenance costs
        - Portability and divisibility
        - Hedge against inflation
        
        **Real Estate Advantages:**
        - Tangible asset with utility
        - Stable, predictable returns
        - Rental income potential
        - Tax advantages
        - Less volatility
        
        **Risk Considerations:**
        - Bitcoin: High volatility, regulatory risks, technical complexity
        - Real Estate: Illiquidity, maintenance costs, location dependency, market cycles
        """)
    
    with st.expander("📊 How to Use This Calculator"):
        st.markdown("""
        1. **Get Current Prices**: Click 'Refresh Now' to fetch latest Bitcoin prices
        2. **Calculate Conversions**: Use Tab 2 to convert between Bitcoin and real estate values
        3. **Plan Investments**: Use Tab 3 to project future values and plan portfolio allocation
        4. **Stay Informed**: Monitor market indicators and news in Tab 4
        5. **Set Up Alerts**: Enable auto-refresh to track price movements
        """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    <p>🏠₿ <strong>Bitcoin Real Estate Calculator Pro</strong> | 
    Data: <a href="https://www.coindesk.com/coindesk-api" target="_blank">CoinDesk API</a> • 
    Enhanced with CoinGecko • RealtyMole • NewsAPI</p>
    <p>⚡ Features: Real-time prices • Real estate calculator • Investment analysis • Market insights • Portfolio planning</p>
    <p>⚠️ <em>This tool is for educational purposes only. Not financial advice. Always do your own research.</em></p>
    </div>
    """,
    unsafe_allow_html=True
)
