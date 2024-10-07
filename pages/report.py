import streamlit as st
import pandas as pd

# Function to calculate real estate investment metrics
def calculate_metrics(price, noi, cash_invested, annual_cash_flow, gross_rental_income, operating_expenses, total_debt_service, square_footage, occupied_units, total_units):
    cap_rate = noi / price
    cash_on_cash_return = annual_cash_flow / cash_invested if cash_invested > 0 else 0
    dscr = noi / total_debt_service if total_debt_service > 0 else 0
    gross_rental_yield = gross_rental_income / price if price > 0 else 0
    price_per_sqft = price / square_footage if square_footage > 0 else 0
    oer = operating_expenses / gross_rental_income if gross_rental_income > 0 else 0
    roi = (annual_cash_flow / cash_invested) * 100 if cash_invested > 0 else 0
    occupancy_rate = (occupied_units / total_units) * 100 if total_units > 0 else 0
    
    return cap_rate, cash_on_cash_return, dscr, gross_rental_yield, price_per_sqft, oer, roi, occupancy_rate

# Function to get AI analysis using the Ollama model
def get_ai_analysis(metrics, property_details):
    prompt = f"""
    As a real estate investment expert, analyze the following property and provide insights:

    Property Details:
    {property_details}

    Financial Metrics:
    {metrics}

    Please provide:
    1. An overall assessment of the investment opportunity
    2. Specific strengths of this property investment
    3. Potential risks or areas of concern
    4. Recommendations for improving the investment's performance
    5. Comparison to typical market standards
    """
    
    response = ollama.generate(model="llama2", prompt=prompt)
    return response['response']

def run():
    st.title("Investment Report")

    # Check if property data is saved in session state
    if 'property_data' not in st.session_state:
        st.error("Please fill out the property details in the Input page first.")
        return

    # Extract data from session state
    data = st.session_state.property_data
    cap_rate, cash_on_cash_return, dscr, gross_rental_yield, price_per_sqft, oer, roi, occupancy_rate = calculate_metrics(
        data["price"], data["noi"], data["cash_invested"], data["annual_cash_flow"], 
        data["gross_rental_income"], data["operating_expenses"], data["total_debt_service"], 
        data["square_footage"], data["occupied_units"], data["total_units"]
    )

    # Display the report
    st.header("Investment Report")
    st.subheader("Property Overview")
    st.write(f"Address: {data['address']}")
    st.write(f"Price: ${data['price']:,.2f}")
    st.write(f"Square Footage: {data['square_footage']:,}")
    st.write(f"Bedrooms: {data['bedrooms']}")
    st.write(f"Bathrooms: {data['bathrooms']}")
    st.write(f"Year Built: {data['year_built']}")

    st.subheader("Financial Metrics")
    st.write(f"Cap Rate: {cap_rate:.2%}")
    st.write(f"Cash-on-Cash Return: {cash_on_cash_return:.2%}")
    st.write(f"Net Operating Income (NOI): ${data['noi']:,.2f}")
    st.write(f"Debt Service Coverage Ratio (DSCR): {dscr:.2f}")
    st.write(f"Gross Rental Yield: {gross_rental_yield:.2%}")
    st.write(f"Price per Square Foot: ${price_per_sqft:.2f}")
    st.write(f"Operating Expense Ratio (OER): {oer:.2%}")
    st.write(f"Return on Investment (ROI): {roi:.2%}")
    st.write(f"Occupancy Rate: {occupancy_rate:.2%}")

    # Advanced AI analysis using Ollama's Llama model
    st.subheader("Advanced AI Investment Analysis")
    
    property_details = f"""
    Address: {data['address']}
    Price: ${data['price']:,.2f}
    Square Footage: {data['square_footage']:,}
    Bedrooms: {data['bedrooms']}
    Bathrooms: {data['bathrooms']}
    Year Built: {data['year_built']}
    """

    metrics = f"""
    Cap Rate: {cap_rate:.2%}
    Cash-on-Cash Return: {cash_on_cash_return:.2%}
    Net Operating Income (NOI): ${data['noi']:,.2f}
    Debt Service Coverage Ratio (DSCR): {dscr:.2f}
    Gross Rental Yield: {gross_rental_yield:.2%}
    Price per Square Foot: ${price_per_sqft:.2f}
    Operating Expense Ratio (OER): {oer:.2%}
    Return on Investment (ROI): {roi:.2%}
    Occupancy Rate: {occupancy_rate:.2%}
    """

    ai_analysis = get_ai_analysis(metrics, property_details)
    st.write(ai_analysis)

    st.write("Note: This AI analysis is based on the provided data and may require further market research.")

