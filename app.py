import streamlit as st

# Set page configurations
st.set_page_config(page_title="AI Real Estate Investment Report", page_icon="prop.png", layout="wide")

# Add logo to the sidebar
st.sidebar.image("prop.png", use_column_width=True)

# Page navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Input", "Report"])

if selection == "Input":
    import pages.input  # Import the input page
    pages.input.run()    # Call the run function in the input page

elif selection == "Report":
    import pages.report   # Import the report page
    pages.report.run()    # Call the run function in the report page
