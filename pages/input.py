import streamlit as st

def run():
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

    # Store inputs in session state
    if st.button("Save Details"):
        st.session_state.property_data = {
            "address": address,
            "price": price,
            "square_footage": square_footage,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "year_built": year_built,
            "noi": noi,
            "cash_invested": cash_invested,
            "annual_cash_flow": annual_cash_flow,
            "gross_rental_income": gross_rental_income,
            "operating_expenses": operating_expenses,
            "total_debt_service": total_debt_service,
            "occupied_units": occupied_units,
            "total_units": total_units,
        }
        st.success("Property details saved! Navigate to the Report page to generate your report.")
