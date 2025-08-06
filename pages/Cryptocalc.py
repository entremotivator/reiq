import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import time

# Page configuration
st.set_page_config(
    page_title="Bitcoin Price Tracker Pro",
    page_icon="₿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #f7931a;
        font-size: 3rem;
        margin-bottom: 2rem;
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
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">₿ Bitcoin Price Tracker Pro</h1>', unsafe_allow_html=True)
st.markdown("### 📊 Real-time Bitcoin prices with advanced analytics")

# Initialize session state
if 'price_history' not in st.session_state:
    st.session_state.price_history = []
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = False

# Sidebar configuration
st.sidebar.title("⚙️ Settings")
st.sidebar.markdown("---")

# API Information
with st.sidebar.expander("📡 API Information"):
    st.info("**CoinDesk API**\n- Free public API\n- No API key required\n- Real-time data\n- Multiple currencies")

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
    st.sidebar.success("History cleared!")

# Currency selection
st.sidebar.markdown("---")
st.sidebar.subheader("💱 Display Preferences")
show_currencies = st.sidebar.multiselect(
    "Select currencies to display:",
    options=["USD", "GBP", "EUR"],
    default=["USD", "GBP", "EUR"]
)

# Number format preference
number_format = st.sidebar.selectbox(
    "Number format:",
    options=["With commas", "Clean"],
    index=0
)

def format_price(price_str, currency, format_type):
    """Format price based on user preference"""
    # Remove commas and convert to float
    clean_price = float(price_str.replace(',', ''))
    
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
            
            # Extract data
            updated_time = data["time"]["updated"]
            prices = {
                "USD": data["bpi"]["USD"]["rate"],
                "GBP": data["bpi"]["GBP"]["rate"],
                "EUR": data["bpi"]["EUR"]["rate"]
            }
            
            # Store in history
            timestamp = datetime.now()
            usd_price_float = float(data["bpi"]["USD"]["rate"].replace(',', ''))
            
            st.session_state.price_history.append({
                "timestamp": timestamp,
                "price": usd_price_float,
                "updated": updated_time
            })
            
            # Keep only last 50 records
            if len(st.session_state.price_history) > 50:
                st.session_state.price_history = st.session_state.price_history[-50:]
            
            return prices, updated_time, True
            
    except requests.exceptions.RequestException as e:
        st.error(f"🚫 Network error: {str(e)}")
        return None, None, False
    except Exception as e:
        st.error(f"🚫 Error fetching data: {str(e)}")
        return None, None, False

# Auto-refresh logic
if auto_refresh:
    placeholder = st.empty()
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = 0
    
    current_time = time.time()
    if current_time - st.session_state.last_refresh > 30:  # 30 seconds
        fetch_data = True
        st.session_state.last_refresh = current_time

# Fetch data
if fetch_data or (auto_refresh and 'prices' not in st.session_state):
    prices, updated_time, success = fetch_bitcoin_price()
    
    if success:
        st.session_state.prices = prices
        st.session_state.updated_time = updated_time
        st.session_state.last_update = datetime.now()

# Display current prices
if 'prices' in st.session_state:
    prices = st.session_state.prices
    updated_time = st.session_state.updated_time
    
    # Success message and last updated
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
    
    # Current prices display
    st.subheader("💰 Current Prices")
    
    # Create columns based on selected currencies
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
    
    # Price history and analytics
    if len(st.session_state.price_history) > 1:
        st.markdown("---")
        st.subheader("📈 Price Analytics")
        
        # Create two columns for analytics
        col1, col2 = st.columns(2)
        
        with col1:
            # Price trend
            latest_price = st.session_state.price_history[-1]["price"]
            previous_price = st.session_state.price_history[-2]["price"]
            price_change = latest_price - previous_price
            price_change_pct = (price_change / previous_price) * 100
            
            trend_emoji = "📈" if price_change > 0 else "📉" if price_change < 0 else "➡️"
            trend_color = "green" if price_change > 0 else "red" if price_change < 0 else "gray"
            
            st.metric(
                label="Change from last fetch",
                value=f"${price_change:+,.2f}",
                delta=f"{price_change_pct:+.2f}%"
            )
        
        with col2:
            # Session statistics
            prices_list = [record["price"] for record in st.session_state.price_history]
            session_high = max(prices_list)
            session_low = min(prices_list)
            
            st.metric(
                label="Session High/Low",
                value=f"${session_high:,.2f}",
                delta=f"Low: ${session_low:,.2f}",
                delta_color="off"
            )
        
        # Price chart
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
            
            fig.update_traces(
                hovertemplate="<b>%{y:$,.2f}</b><br>%{x}<extra></extra>"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Data table
            with st.expander("📋 View Raw Data"):
                display_df = df.copy()
                display_df["price"] = display_df["price"].apply(lambda x: f"${x:,.2f}")
                display_df["timestamp"] = display_df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
                display_df = display_df.rename(columns={
                    "timestamp": "Time",
                    "price": "Price (USD)",
                    "updated": "API Updated"
                })
                st.dataframe(display_df.iloc[::-1], use_container_width=True, hide_index=True)

else:
    # Initial state
    st.info("👆 Click the **Refresh Now** button in the sidebar to get the latest Bitcoin prices.")
    
    # Sample chart placeholder
    st.subheader("📊 Sample Chart")
    sample_data = pd.DataFrame({
        'time': pd.date_range('2024-01-01', periods=10, freq='H'),
        'price': [45000, 45200, 44800, 45100, 45300, 44900, 45400, 45000, 45250, 45150]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=sample_data['time'],
        y=sample_data['price'],
        mode='lines+markers',
        name='Bitcoin Price (USD)',
        line=dict(color='#f7931a', width=2),
        marker=dict(size=6, color='#f7931a')
    ))
    
    fig.update_layout(
        title="Sample Bitcoin Price Chart",
        xaxis_title="Time",
        yaxis_title="Price (USD)",
        height=300,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    <p>💡 <strong>Bitcoin Price Tracker Pro</strong> | Data provided by <a href="https://www.coindesk.com/coindesk-api" target="_blank">CoinDesk API</a></p>
    <p>⚡ Features: Real-time prices, Auto-refresh, Price history, Interactive charts, Multi-currency support</p>
    </div>
    """,
    unsafe_allow_html=True
)
