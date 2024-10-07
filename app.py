import streamlit as st
import pandas as pd
import numpy as np
import ollama

# Set page configurations (logo in sidebar and favicon)
st.set_page_config(
    page_title="AI Real Estate Investment Report",
    page_icon="/Users/donmenicohudson/Downloads/aipropiq/prop.png",  # Use your 'prop.png' as the favicon
    layout="wide"
)

# Add logo to the sidebar
st.sidebar.image("/Users/donmenicohudson/Downloads/aipropiq/prop.png", use_column_width=True)

# Function to calculate real estate investment metrics
def calculate_metrics(price, noi, cash_invested, annual_cash_flow, gross_rental_income, operating_expenses, total_debt_service, square_footage, occupied_units, total_units):
    cap_rate = noi / price
    cash_on_cash_return = annual_cash_flow / cash_invested
    dscr = noi / total_debt_service
    gross_rental_yield = gross_rental_income / price
    price_per_sqft = price / square_footage
    oer = operating_expenses / gross_rental_income
    roi = (annual_cash_flow / cash_invested) * 100
    occupancy_rate = (occupied_units / total_units) * 100
    
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

# Main function to run the Streamlit app
def main():
    st.title("Enhanced AI Real Estate Investment Report Creator")

    # Property details input
    st.header("Property Details")
    address = st.text_input("Property Address")
    price = st.number_input("Property Price", min_value=0.0)
    square_footage = st.number_input("Square Footage", min_value=0)
    bedrooms = st.number_input("Number of Bedrooms", min_value=0)
    bathrooms = st.number_input("Number of Bathrooms", min_value=0.0, step=0.5)
    year_built = st.number_input("Year Built", min_value=1800, max_value=2100)

    # Financial details input
    st.header("Financial Details")
    noi = st.number_input("Net Operating Income (NOI)", min_value=0.0)
    cash_invested = st.number_input("Total Cash Invested", min_value=0.0)
    annual_cash_flow = st.number_input("Annual Cash Flow", min_value=0.0)
    gross_rental_income = st.number_input("Gross Rental Income", min_value=0.0)
    operating_expenses = st.number_input("Operating Expenses", min_value=0.0)
    total_debt_service = st.number_input("Total Debt Service", min_value=0.0)
    occupied_units = st.number_input("Occupied Units", min_value=0)
    total_units = st.number_input("Total Units", min_value=1)

    # Generate report button
    if st.button("Generate Report"):
        cap_rate, cash_on_cash_return, dscr, gross_rental_yield, price_per_sqft, oer, roi, occupancy_rate = calculate_metrics(
            price, noi, cash_invested, annual_cash_flow, gross_rental_income, operating_expenses, total_debt_service, square_footage, occupied_units, total_units
        )

        # Display the report
        st.header("Investment Report")
        st.subheader("Property Overview")
        st.write(f"Address: {address}")
        st.write(f"Price: ${price:,.2f}")
        st.write(f"Square Footage: {square_footage:,}")
        st.write(f"Bedrooms: {bedrooms}")
        st.write(f"Bathrooms: {bathrooms}")
        st.write(f"Year Built: {year_built}")

        st.subheader("Financial Metrics")
        st.write(f"Cap Rate: {cap_rate:.2%}")
        st.write(f"Cash-on-Cash Return: {cash_on_cash_return:.2%}")
        st.write(f"Net Operating Income (NOI): ${noi:,.2f}")
        st.write(f"Debt Service Coverage Ratio (DSCR): {dscr:.2f}")
        st.write(f"Gross Rental Yield: {gross_rental_yield:.2%}")
        st.write(f"Price per Square Foot: ${price_per_sqft:.2f}")
        st.write(f"Operating Expense Ratio (OER): {oer:.2%}")
        st.write(f"Return on Investment (ROI): {roi:.2%}")
        st.write(f"Occupancy Rate: {occupancy_rate:.2%}")

        # Basic AI analysis based on key metrics
        st.subheader("Basic AI Investment Analysis")
        if cap_rate > 0.08:
            st.write("The cap rate is above average, indicating a potentially good investment opportunity.")
        else:
            st.write("The cap rate is below average. Consider investigating further to ensure the property meets your investment criteria.")

        if cash_on_cash_return > 0.10:
            st.write("The cash-on-cash return is strong, suggesting good immediate cash flow performance.")
        else:
            st.write("The cash-on-cash return is lower than ideal. Evaluate ways to improve cash flow or negotiate a better purchase price.")

        if dscr > 1.25:
            st.write("The debt service coverage ratio is healthy, indicating the property can comfortably cover its debt obligations.")
        else:
            st.write("The debt service coverage ratio is concerning. Consider strategies to increase income or reduce debt.")

        # Advanced AI analysis using Ollama's Llama model
        st.subheader("Advanced AI Investment Analysis")
        
        property_details = f"""
        Address: {address}
        Price: ${price:,.2f}
        Square Footage: {square_footage:,}
        Bedrooms: {bedrooms}
        Bathrooms: {bathrooms}
        Year Built: {year_built}
        """

        metrics = f"""
        Cap Rate: {cap_rate:.2%}
        Cash-on-Cash Return: {cash_on_cash_return:.2%}
        Net Operating Income (NOI): ${noi:,.2f}
        Debt Service Coverage Ratio (DSCR): {dscr:.2f}
        Gross Rental Yield: {gross_rental_yield:.2%}
        Price per Square Foot: ${price_per_sqft:.2f}
        Operating Expense Ratio (OER): {oer:.2%}
        Return on Investment (ROI): {roi:.2%}
        Occupancy Rate: {occupancy_rate:.2%}
        """

        ai_analysis = get_ai_analysis(metrics, property_details)
        st.write(ai_analysis)

        st.write("Note: This AI analysis is based on the provided data and general market knowledge. Always consult with a financial advisor or real estate professional for personalized advice.")

# Run the app
if __name__ == "__main__":
    main()
