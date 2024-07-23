import streamlit as st
from input_functions import get_plan_inputs, get_user_inputs
from calculation_functions import calculate_revenue, display_revenue_table, display_user_growth_chart, display_revenue_growth_chart, display_revenue_breakdown_chart

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
        display_revenue_breakdown_chart(revenue_data, years)

if __name__ == "__main__":
    main()