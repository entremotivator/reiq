import streamlit as st

# Set page configurations
st.set_page_config(page_title="AI Real Estate Investment Report", page_icon="prop.png", layout="wide")

# Add logo to the sidebar
st.sidebar.image("prop.png", use_column_width=True)

# Page navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Input", "Report"])

# Navigation logic
if selection == "Input":
    # Assuming 'input.py' is located in a folder named 'pages'
    import pages.input as input_page  # Import the input page
    input_page.run()  # Call the run function in the input page

elif selection == "Report":
    # Assuming 'report.py' is located in a folder named 'pages'
    import pages.report as report_page  # Import the report page
    report_page.run()  # Call the run function in the report page
