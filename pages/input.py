import streamlit as st

def calculate_metrics(property_data):
    """Calculate various financial metrics based on the provided property data."""
    price = property_data["price"]
    noi = property_data["noi"]
    cash_invested = property_data["cash_invested"]
    gross_rental_income = property_data["gross_rental_income"]
    operating_expenses = property_data["operating_expenses"]
    total_debt_service = property_data["total_debt_service"]
    occupied_units = property_data["occupied_units"]
    total_units = property_data["total_units"]

    # Financial metrics calculations
    annual_cash_flow = gross_rental_income - operating_expenses
    cash_on_cash_return = (annual_cash_flow / cash_invested) * 100 if cash_invested > 0 else 0
    cap_rate = (noi / price) * 100 if price > 0 else 0
    dscr = (noi / total_debt_service) if total_debt_service > 0 else 0
    gross_rental_yield = (gross_rental_income / price) * 100 if price > 0 else 0
    price_per_sqft = price / property_data["square_footage"] if property_data["square_footage"] > 0 else 0
    oer = (operating_expenses / gross_rental_income) * 100 if gross_rental_income > 0 else 0
    roi = (annual_cash_flow / cash_invested) * 100 if cash_invested > 0 else 0
    occupancy_rate = (occupied_units / total_units) * 100 if total_units > 0 else 0

    return {
        "annual_cash_flow": annual_cash_flow,
        "cash_on_cash_return": cash_on_cash_return,
        "cap_rate": cap_rate,
        "dscr": dscr,
        "gross_rental_yield": gross_rental_yield,
        "price_per_sqft": price_per_sqft,
        "oer": oer,
        "roi": roi,
        "occupancy_rate": occupancy_rate,
    }

def generate_html_report(metrics, property_details):
    """Generate the HTML content for the investment report."""
    html_content = f"""
    <html>
    <head>
        <title>Property Investment Analysis Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            h1 {{ text-align: center; }}
            h2 {{ margin-top: 20px; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ border: 1px solid black; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            p {{ line-height: 1.6; }}
            .financial-details {{ margin-top: 20px; }}
        </style>
    </head>
    <body>
        <h1>Property Investment Analysis Report</h1>
        
        <h2>Property Details</h2>
        <p><strong>Property Address:</strong> {property_details['address']}</p>
        <p><strong>Price:</strong> ${property_details['price']:.2f}</p>
        <p><strong>Square Footage:</strong> {property_details['square_footage']} sqft</p>
        <p><strong>Bedrooms:</strong> {property_details['bedrooms']}</p>
        <p><strong>Bathrooms:</strong> {property_details['bathrooms']}</p>
        <p><strong>Year Built:</strong> {property_details['year_built']}</p>
        
        <h2>Financial Details</h2>
        <div class="financial-details">
            <p><strong>Net Operating Income (NOI):</strong> ${metrics['annual_cash_flow'] + property_details['operating_expenses']:.2f}</p>
            <p><strong>Cash Invested:</strong> ${property_details['cash_invested']:.2f}</p>
            <p><strong>Gross Rental Income:</strong> ${property_details['gross_rental_income']:.2f}</p>
            <p><strong>Operating Expenses:</strong> ${property_details['operating_expenses']:.2f}</p>
            <p><strong>Total Debt Service:</strong> ${property_details['total_debt_service']:.2f}</p>
            <p><strong>Occupied Units:</strong> {property_details['occupied_units']}</p>
            <p><strong>Total Units:</strong> {property_details['total_units']}</p>
        </div>
        
        <h2>Calculated Financial Metrics</h2>
        <table>
            <tr><th>Metric</th><th>Value</th></tr>
            <tr><td>Annual Cash Flow</td><td>${metrics['annual_cash_flow']:.2f}</td></tr>
            <tr><td>Cash on Cash Return</td><td>{metrics['cash_on_cash_return']:.2f}%</td></tr>
            <tr><td>Cap Rate</td><td>{metrics['cap_rate']:.2f}%</td></tr>
            <tr><td>DSCR</td><td>{metrics['dscr']:.2f}</td></tr>
            <tr><td>Gross Rental Yield</td><td>{metrics['gross_rental_yield']:.2f}%</td></tr>
            <tr><td>Price per Square Foot</td><td>${metrics['price_per_sqft']:.2f}</td></tr>
            <tr><td>Operating Expense Ratio</td><td>{metrics['oer']:.2f}%</td></tr>
            <tr><td>ROI</td><td>{metrics['roi']:.2f}%</td></tr>
            <tr><td>Occupancy Rate</td><td>{metrics['occupancy_rate']:.2f}%</td></tr>
        </table>
        
        <h2>Conclusion</h2>
        <p>This report provides a comprehensive analysis of the property investment, including essential metrics that will help in making informed decisions.</p>
    </body>
    </html>
    """
    return html_content

def run():
    st.title("Enhanced AI Real Estate Investment Report Creator")

    # Property details input
    st.header("Property Details")
    address = st.text_input("Property Address", "1234 Example St, Anytown, USA")
    price = st.number_input("Property Price", min_value=0.0, value=350000.00)
    square_footage = st.number_input("Square Footage", min_value=0, value=1500)
    bedrooms = st.number_input("Number of Bedrooms", min_value=0, value=3)
    bathrooms = st.number_input("Number of Bathrooms", min_value=0.0, step=0.5, value=2.0)
    year_built = st.number_input("Year Built", min_value=1800, max_value=2100, value=1990)

    # Financial details input
    st.header("Financial Details")
    noi = st.number_input("Net Operating Income (NOI)", min_value=0.0, value=20000.06)
    cash_invested = st.number_input("Cash Invested", min_value=0.0, value=70000.00)
    gross_rental_income = st.number_input("Gross Rental Income", min_value=0.0, value=36000.00)
    operating_expenses = st.number_input("Operating Expenses", min_value=0.0, value=10000.00)
    total_debt_service = st.number_input("Total Debt Service", min_value=0.0, value=15000.00)
    occupied_units = st.number_input("Occupied Units", min_value=0, value=1)
    total_units = st.number_input("Total Units", min_value=1, value=1)

    # Gather property data
    property_data = {
        "address": address,
        "price": price,
        "square_footage": square_footage,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "year_built": year_built,
        "noi": noi,
        "cash_invested": cash_invested,
        "gross_rental_income": gross_rental_income,
        "operating_expenses": operating_expenses,
        "total_debt_service": total_debt_service,
        "occupied_units": occupied_units,
        "total_units": total_units,
    }

    metrics = calculate_metrics(property_data)

    if st.button("Generate Report"):
        html_content = generate_html_report(metrics, property_data)
        st.download_button(
            label="Download PDF",
            data=html_content,
            file_name="Investment_Report.html",
            mime="text/html",
        )
        st.success("Report generated successfully!")

run()
