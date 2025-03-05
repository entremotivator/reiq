import streamlit as st
from PIL import Image

# Set page configurations
st.set_page_config(
    page_title="AI Real Estate Investment Report",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to improve the app's appearance
st.markdown("""
    <style>
    .reportview-container {
        background: #f0f2f6
    }
    .sidebar .sidebar-content {
        background: #262730
    }
    .Widget>label {
        color: #262730;
        font-family: sans-serif;
    }
    .stButton>button {
        color: #4F8BF9;
        border-radius: 50px;
        height: 3em;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# Add logo to the sidebar
logo = Image.open("prop.png")
st.sidebar.image(logo, use_column_width=True)

# Sidebar navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Home", "Input", "Report"])

# Main content area
st.title("AI Real Estate Investment Report")
st.write("Welcome to your intelligent real estate investment assistant!")

# Navigation logic
if selection == "Home":
    st.header("About This Tool")
    st.write("""
    This AI-powered tool helps you make informed decisions about real estate investments.
    Use the sidebar to navigate between inputting property details and generating reports.
    """)
    
    st.subheader("How to Use")
    st.write("""
    1. Go to the 'Input' page to enter property details.
    2. Navigate to the 'Report' page to view your personalized investment analysis.
    3. Explore different scenarios by adjusting your inputs.
    """)
    
    # Add a call-to-action button
    if st.button("Get Started"):
        st.session_state.selection = "Input"
        st.experimental_rerun()

elif selection == "Input":
    import pages.input as input_page
    input_page.run()

elif selection == "Report":
    import pages.report as report_page
    report_page.run()

# Footer
st.sidebar.markdown("---")
st.sidebar.info("© 2025 AI Real Estate Investment Report")
