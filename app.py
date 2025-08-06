import streamlit as st
import pandas as pd
from PIL import Image
import random
import datetime

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
    .stDataFrame {
        border: 1px solid #4F8BF9;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Add logo to the sidebar
logo = Image.open("prop.png")
st.sidebar.image(logo, use_column_width=True)

# Sidebar navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Home", "Input", "Report", "Manage Properties"])

# Initialize session state for properties
if 'properties' not in st.session_state:
    st.session_state.properties = []

# Generate 10 demo properties
def generate_demo_properties():
    properties = []
    for i in range(1, 11):
        property = {
            "id": i,
            "address": f"{random.randint(100, 999)} {random.choice(['Main', 'Oak', 'Pine', 'Maple'])} St, City {i}",
            "type": random.choice(["Single Family", "Multi-Family", "Condo", "Townhouse"]),
            "price": random.randint(100000, 1000000),
            "bedrooms": random.randint(1, 5),
            "bathrooms": random.randint(1, 4),
            "square_feet": random.randint(800, 3000),
            "year_built": random.randint(1950, 2022),
            "date_added": datetime.datetime.now().strftime("%Y-%m-%d")
        }
        properties.append(property)
    return properties

# Main content area
st.title("AI Real Estate Investment Report")
st.write("Welcome to your intelligent real estate investment assistant!")

# Navigation logic
if selection == "Home":
    st.header("About This Tool")
    st.write("""
    This AI-powered tool helps you make informed decisions about real estate investments.
    Use the sidebar to navigate between inputting property details, generating reports, and managing your property portfolio.
    """)
    
    st.subheader("Key Features")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("🏠 **Property Input**")
        st.write("Easily input and save property details.")
    with col2:
        st.markdown("📊 **Investment Analysis**")
        st.write("Generate comprehensive investment reports.")
    with col3:
        st.markdown("📁 **Portfolio Management**")
        st.write("View and manage all your inputted properties.")
    
    st.subheader("How to Use")
    st.write("""
    1. Go to the 'Input' page to enter property details.
    2. Navigate to the 'Report' page to view your personalized investment analysis.
    3. Use the 'Manage Properties' page to see all your saved properties.
    4. Explore different scenarios by adjusting your inputs and comparing properties.
    """)
    
    # Add a call-to-action button
    if st.button("Get Started"):
        st.session_state.selection = "Input"
        st.rerun()

elif selection == "Input":
    import pages.input as input_page
    input_page.run()

elif selection == "Report":
    import pages.report as report_page
    report_page.run()

elif selection == "Manage Properties":
    st.header("Manage Your Properties")
    
    # Add demo properties if the list is empty
    if not st.session_state.properties:
        st.session_state.properties = generate_demo_properties()
    
    # Display properties in a dataframe
    df = pd.DataFrame(st.session_state.properties)
    st.dataframe(df)
    
    # Add functionality to remove a property
    property_to_remove = st.selectbox("Select a property to remove:", df['address'])
    if st.button("Remove Selected Property"):
        st.session_state.properties = [p for p in st.session_state.properties if p['address'] != property_to_remove]
        st.success(f"Property at {property_to_remove} has been removed.")
        st.experimental_rerun()
    
    # Add functionality to add a new property
    st.subheader("Add a New Property")
    with st.form("add_property_form"):
        new_address = st.text_input("Address")
        new_type = st.selectbox("Property Type", ["Single Family", "Multi-Family", "Condo", "Townhouse"])
        new_price = st.number_input("Price", min_value=0, step=1000)
        new_bedrooms = st.number_input("Bedrooms", min_value=0, step=1)
        new_bathrooms = st.number_input("Bathrooms", min_value=0, step=0.5)
        new_square_feet = st.number_input("Square Feet", min_value=0, step=10)
        new_year_built = st.number_input("Year Built", min_value=1800, max_value=datetime.datetime.now().year, step=1)
        
        if st.form_submit_button("Add Property"):
            new_property = {
                "id": len(st.session_state.properties) + 1,
                "address": new_address,
                "type": new_type,
                "price": new_price,
                "bedrooms": new_bedrooms,
                "bathrooms": new_bathrooms,
                "square_feet": new_square_feet,
                "year_built": new_year_built,
                "date_added": datetime.datetime.now().strftime("%Y-%m-%d")
            }
            st.session_state.properties.append(new_property)
            st.success(f"Property at {new_address} has been added.")
            st.rerun()

# Footer
st.sidebar.markdown("---")
st.sidebar.info("© 2025 AI PropIQ Investment Report")
