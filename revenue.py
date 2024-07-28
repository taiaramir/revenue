import streamlit as st
from input_functions import get_plan_inputs, get_user_inputs
from revenue_calculation import calculate_revenue
from revenue_display import display_revenue_table
from charts import display_user_growth_chart, display_revenue_growth_chart, display_revenue_breakdown_chart
from color_palettes import PRIMARY_PURPLE
from help_page import display_math_explanation

def main():
    if 'page' not in st.session_state:
        st.session_state.page = "Plans"

    st.sidebar.title("Navigation")
    
    # Main navigation
    main_pages = ["Plans", "Users", "Revenue", "Insights"]
    selected_page = st.sidebar.radio("Go to", main_pages, key="navigation")
    
    # Update the page state based on main navigation
    st.session_state.page = selected_page

    # Add year slider to sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Years")
    years = st.sidebar.slider("Projection Years", min_value=1, max_value=7, value=1, step=1)

    # Add Help section to sidebar
    st.sidebar.markdown("---")
    if st.sidebar.button("Calculation Explanation", key="help_button"):
        st.session_state.page = "Calculation Explanation"

    # Initialize session state for plans and users if not already present
    if 'plans' not in st.session_state:
        st.session_state.plans = get_plan_inputs()
    if 'users' not in st.session_state:
        st.session_state.users = get_user_inputs()

    # Display the appropriate page content
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
        display_revenue_breakdown_chart(revenue_data, years, st.session_state.users)
    elif st.session_state.page == "Calculation Explanation":
        display_math_explanation()

if __name__ == "__main__":
    main()