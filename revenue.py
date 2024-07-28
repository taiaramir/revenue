import streamlit as st
from input_functions import get_plan_inputs, get_user_inputs
from revenue_calculation import calculate_revenue
from revenue_display import display_revenue_table
from charts import display_user_growth_chart, display_revenue_growth_chart, display_revenue_breakdown_chart

from color_palettes import PRIMARY_PURPLE
st.set_page_config(page_title="Revenue Projection", page_icon="📊", layout="wide", initial_sidebar_state="expanded", menu_items=None)

# Custom CSS for tab styling
st.markdown(f"""
<style>
    .stTabs [data-baseweb="tab-list"] {{
        gap: 24px;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        white-space: pre-wrap;
        border-radius: 4px 4px 0px 0px;
        gap: 12px;
        padding-top: 10px;
        padding-bottom: 10px;
        padding-left: 20px;
        padding-right: 20px;
        border-bottom: 2px solid transparent;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: transparent !important;
        border-bottom-color: {PRIMARY_PURPLE[700]} !important;
        border-top: none !important;
        border-left: none !important;
        border-right: none !important;
    }}
    .stTabs [aria-selected="true"] [data-testid="stMarkdownContainer"] p {{
        color: {PRIMARY_PURPLE[700]} !important;
    }}
    .stTabs [role="tablist"] button [data-testid="stMarkdownContainer"] p {{
        font-size: 14px;
        font-weight: 500;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        background-color: transparent !important;
        border-bottom-color: {PRIMARY_PURPLE[700]} !important;
        border-top: none !important;
        border-left: none !important;
        border-right: none !important;
    }}
    .stTabs [data-baseweb="tab"]:hover [data-testid="stMarkdownContainer"] p {{
        color: {PRIMARY_PURPLE[700]} !important;
    }}
    .stTabs [data-baseweb="tab-highlight"] {{
        display: none;
    }}
</style>
""", unsafe_allow_html=True)

# ... rest of your main() function

def main():
    if 'page' not in st.session_state:
        st.session_state.page = "Plans"

    st.sidebar.title("Navigation")
    st.session_state.page = st.sidebar.radio("Go to", ["Plans", "Users", "Revenue", "Insights"], key="navigation")

    # Add year slider to sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Years")
    years = st.sidebar.slider("Projection Years", min_value=1, max_value=7, value=1, step=1)

    # Initialize session state for plans and users if not already present
    if 'plans' not in st.session_state:
        st.session_state.plans = get_plan_inputs()
    if 'users' not in st.session_state:
        st.session_state.users = get_user_inputs()

    if st.session_state.page == "Plans":
        st.session_state.plans = get_plan_inputs()
    elif st.session_state.page == "Users":
        st.session_state.users = get_user_inputs()
    elif st.session_state.page == "Revenue":
        revenue_data = calculate_revenue(st.session_state.plans, st.session_state.users, years)
        display_revenue_table(revenue_data, years)
    elif st.session_state.page == "Insights":
        st.header("Insights")
        revenue_data = calculate_revenue(st.session_state.plans, st.session_state.users, years)
        
        st.subheader("User Growth Over Time")
        display_user_growth_chart(revenue_data, years)
        
        st.subheader("Revenue Growth Over Time")
        display_revenue_growth_chart(revenue_data, years)

        st.subheader("Revenue Breakdown by Line Item")
        display_revenue_breakdown_chart(revenue_data, years, st.session_state.users)  # Pass users_data here

if __name__ == "__main__":
    main()