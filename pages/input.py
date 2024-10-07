import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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

    # Calculating financial metrics
    annual_cash_flow = gross_rental_income - operating_expenses  # Assuming cash flow calculation
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

def generate_report(metrics, property_details):
    """Generate a comprehensive report based on the financial metrics and property details."""
    report = f"""
    ## Property Investment Analysis Report

    **Property Address:** {property_details["address"]}  
    **Price:** ${property_details["price"]:.2f}  
    **Square Footage:** {property_details["square_footage"]} sqft  
    **Bedrooms:** {property_details["bedrooms"]}  
    **Bathrooms:** {property_details["bathrooms"]}  
    **Year Built:** {property_details["year_built"]}  

    ### Financial Metrics
    - Annual Cash Flow: ${metrics['annual_cash_flow']:.2f}
    - Cash on Cash Return: {metrics['cash_on_cash_return']:.2f}%
    - Capitalization Rate (Cap Rate): {metrics['cap_rate']:.2f}%
    - Debt Service Coverage Ratio (DSCR): {metrics['dscr']:.2f}
    - Gross Rental Yield: {metrics['gross_rental_yield']:.2f}%
    - Price per Square Foot: ${metrics['price_per_sqft']:.2f}
    - Operating Expense Ratio (OER): {metrics['oer']:.2f}%
    - Return on Investment (ROI): {metrics['roi']:.2f}%
    - Occupancy Rate: {metrics['occupancy_rate']:.2f}%

    ### Property Summary
    - **Investment Type:** Residential
    - **Location Quality:** Good (assumed; can be based on user input)
    - **Potential Appreciation:** 5% (assumed; can be based on user input)
    - **Market Trends:** Stable (assumed; can be based on user input)
    """
    return report

def export_report_as_pdf(report, filename="Investment_Report.pdf"):
    """Export the report as a PDF file using reportlab."""
    pdf = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Title
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(30, height - 40, "Property Investment Analysis Report")
    
    # Set font for the report body
    pdf.setFont("Helvetica", 12)
    
    # Draw the report content
    y_position = height - 80
    for line in report.split('\n'):
        pdf.drawString(30, y_position, line.strip())
        y_position -= 15  # Move down for the next line

    pdf.save()

def export_report_as_csv(property_details, metrics, filename="Investment_Report.csv"):
    """Export the report as a CSV file."""
    data = {
        "Property Address": property_details["address"],
        "Price": property_details["price"],
        "Square Footage": property_details["square_footage"],
        "Bedrooms": property_details["bedrooms"],
        "Bathrooms": property_details["bathrooms"],
        "Year Built": property_details["year_built"],
        "Annual Cash Flow": metrics['annual_cash_flow'],
        "Cash on Cash Return (%)": metrics['cash_on_cash_return'],
        "Cap Rate (%)": metrics['cap_rate'],
        "DSCR": metrics['dscr'],
        "Gross Rental Yield (%)": metrics['gross_rental_yield'],
        "Price per Square Foot": metrics['price_per_sqft'],
        "Operating Expense Ratio (%)": metrics['oer'],
        "ROI (%)": metrics['roi'],
        "Occupancy Rate (%)": metrics['occupancy_rate'],
    }

    df = pd.DataFrame([data])
    df.to_csv(filename, index=False)

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
    noi = st.number_input("Net Operating Income (NOI)", min_value=0.0, value=30000.00)
    cash_invested = st.number_input("Total Cash Invested", min_value=0.0, value=70000.00)
    gross_rental_income = st.number_input("Gross Rental Income", min_value=0.0, value=42000.00)
    operating_expenses = st.number_input("Operating Expenses", min_value=0.0, value=12000.00)
    total_debt_service = st.number_input("Total Debt Service", min_value=0.0, value=24000.00)
    occupied_units = st.number_input("Occupied Units", min_value=0, value=3)
    total_units = st.number_input("Total Units", min_value=1, value=4)

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
            "gross_rental_income": gross_rental_income,
            "operating_expenses": operating_expenses,
            "total_debt_service": total_debt_service,
            "occupied_units": occupied_units,
            "total_units": total_units,
        }
        st.success("Property details saved! Navigate to the Report page to generate your report.")

    # Generate and display the report
    if "property_data" in st.session_state:
        property_data = st.session_state.property_data
        metrics = calculate_metrics(property_data)

        if st.button("Generate Investment Report"):
            report = generate_report(metrics, property_data)
            st.success("Investment report generated!")
            st.markdown(report)

            # Export options
            export_pdf = st.button("Export Report as PDF")
            export_csv = st.button("Export Report as CSV")

            if export_pdf:
                export_report_as_pdf(report)
                st.success("Report exported as PDF.")

            if export_csv:
                export_report_as_csv(property_data, metrics)
                st.success("Report exported as CSV.")

# Run the Streamlit application
if __name__ == "__main__":
    run()
