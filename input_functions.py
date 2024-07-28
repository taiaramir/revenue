import streamlit as st

def get_plan_inputs():
    st.header("Plans")
    
    st.markdown("""
    The Plans page allows you to configure monthly fees for users, workspaces, and platforms across different plan tiers. 
    You can also set additional parameters for each plan, which are used in our revenue calculation formulas. 
    These settings provide a comprehensive view of your pricing strategy and its potential impact on revenue.
    """)
    
    plan_types = ["Basic", "Pro", "Enterprise"]
    tabs = st.tabs(plan_types)
    
    if 'plans_data' not in st.session_state:
        st.session_state.plans_data = {}

    for i, tab in enumerate(tabs):
        with tab:
            plan_type = plan_types[i]
            st.subheader(f"{plan_type} Plan")
            
            if plan_type not in st.session_state.plans_data:
                st.session_state.plans_data[plan_type] = {
                    "name": plan_type,
                    "Platform Fee": 100.0,
                    "User Fee": 50.0,
                    "Workspace Fee": 0.0,
                    "Implementation Fee": 500.0,
                    "Growth": 150.0,
                    "Churn": 30.0,
                }
            else:
                # Handle the transition from "Seat Fee" to "User Fee"
                if "Seat Fee" in st.session_state.plans_data[plan_type]:
                    st.session_state.plans_data[plan_type]["User Fee"] = st.session_state.plans_data[plan_type].pop("Seat Fee")
                # Ensure Workspace Fee is a number
                if isinstance(st.session_state.plans_data[plan_type]["Workspace Fee"], str):
                    st.session_state.plans_data[plan_type]["Workspace Fee"] = 0.0
            
            col1, space, col2 = st.columns([1, 0.1, 1])
            
            with col1:
                st.markdown("<h5 style='color: #888888; font-size: 14px;'>Pricing</h5>", unsafe_allow_html=True)
                st.session_state.plans_data[plan_type]["Platform Fee"] = st.number_input(
                    "Platform Fee", 
                    min_value=0.0, 
                    value=float(st.session_state.plans_data[plan_type]["Platform Fee"]), 
                    step=1.0, 
                    key=f"Platform Fee_{plan_type}"
                )
                
                st.session_state.plans_data[plan_type]["User Fee"] = st.number_input(
                    "User Fee", 
                    min_value=0.0, 
                    value=float(st.session_state.plans_data[plan_type]["User Fee"]), 
                    step=1.0, 
                    key=f"User Fee_{plan_type}"
                )
                
                st.session_state.plans_data[plan_type]["Workspace Fee"] = st.number_input(
                    "Workspace Fee", 
                    min_value=0.0, 
                    value=float(st.session_state.plans_data[plan_type]["Workspace Fee"]), 
                    step=1.0, 
                    key=f"Workspace Fee_{plan_type}"
                )
                
                st.session_state.plans_data[plan_type]["Implementation Fee"] = st.number_input(
                    "Implementation Fee", 
                    min_value=0.0, 
                    value=float(st.session_state.plans_data[plan_type]["Implementation Fee"]), 
                    step=1.0, 
                    key=f"Implementation Fee_{plan_type}"
                )

            with col2:
                st.markdown("<h5 style='color: #888888; font-size: 14px;'>Variables</h5>", unsafe_allow_html=True)
                st.session_state.plans_data[plan_type]["Growth"] = st.number_input(
                    "Growth (%)", 
                    min_value=0.0, 
                    value=float(st.session_state.plans_data[plan_type]["Growth"]), 
                    step=0.1, 
                    format="%.1f",
                    key=f"Growth_{plan_type}"
                )
                
                st.session_state.plans_data[plan_type]["Churn"] = st.number_input(
                    "Churn (%)", 
                    min_value=0.0, 
                    value=float(st.session_state.plans_data[plan_type]["Churn"]), 
                    step=0.1, 
                    format="%.1f",
                    key=f"Churn_{plan_type}"
                )

    return st.session_state.plans_data

def get_user_inputs():
    st.header("Users")

    if 'user_lines' not in st.session_state:
        st.session_state.user_lines = [{
            "name": "Line item #1",
            "plan": "Basic",
            "total_companies": 1000,
            "companies_target": 10.0,
            "companies": 100,
            "total_employees": 10000,
            "users_target": 5.0,
            "users": 500,
            "workspaces": 50,  # New field
            "year_started": 1
        }]

    users_data = []

    for i, user_line in enumerate(st.session_state.user_lines):
        st.markdown("---")  # Line divider
        
        name = st.text_input("Name/Segment", value=user_line.get("name", f"Line item #{i+1}"), key=f"name_{i}")
        plan = st.selectbox("Plan", ["Basic", "Pro", "Enterprise"], key=f"plan_{i}", index=["Basic", "Pro", "Enterprise"].index(user_line["plan"]))
        
        col1, col2 = st.columns(2)
        
        with col1:
            total_companies = st.number_input("Total companies", min_value=0, step=1, key=f"total_companies_{i}", value=user_line.get("total_companies", 0))
            companies_target = st.number_input("Companies % target", min_value=0.0, max_value=100.0, step=0.1, key=f"companies_target_{i}", value=float(user_line.get("companies_target", 0.0)))
            calculated_companies = int(total_companies * companies_target / 100)
            companies = st.number_input("Companies", min_value=0, step=1, key=f"companies_{i}", value=calculated_companies)
        
        with col2:
            total_employees = st.number_input("Total employees", min_value=0, step=1, key=f"total_employees_{i}", value=user_line.get("total_employees", 0))
            users_target = st.number_input("Users % target", min_value=0.0, max_value=100.0, step=0.1, key=f"users_target_{i}", value=float(user_line.get("users_target", 0.0)))
            calculated_users = int(total_employees * users_target / 100)
            users = st.number_input("Users", min_value=0, step=1, key=f"users_{i}", value=calculated_users)
        
        workspaces = st.number_input("Workspaces", min_value=0, step=1, key=f"workspaces_{i}", value=user_line.get("workspaces", 0))
        year_started = st.number_input("Year started", min_value=1, step=1, key=f"year_started_{i}", value=user_line.get("year_started", 1))

        if st.button("Remove", key=f"remove_{i}"):
            st.session_state.user_lines.pop(i)
            st.experimental_rerun()

        users_data.append({
            "Order": i, 
            "Name": name,
            "Plan": plan,
            "Total companies": total_companies,
            "Companies % target": companies_target,
            "Companies": companies,
            "Total employees": total_employees,
            "Users % target": users_target,
            "Users": users,
            "Workspaces": workspaces,
            "Year Started": year_started
        })

        # Update session state
        st.session_state.user_lines[i] = {
            "name": name,
            "plan": plan,
            "total_companies": total_companies,
            "companies_target": companies_target,
            "companies": companies,
            "total_employees": total_employees,
            "users_target": users_target,
            "users": users,
            "workspaces": workspaces,
            "year_started": year_started
        }

    # Add button with green color
    if st.button("Add", type="primary"):
        new_line_number = len(st.session_state.user_lines) + 1
        st.session_state.user_lines.append({
            "name": f"Line item #{new_line_number}",
            "plan": "Basic",
            "total_companies": 1000,
            "companies_target": 10.0,
            "companies": 100,
            "total_employees": 10000,
            "users_target": 5.0,
            "users": 500,
            "workspaces": 50,
            "year_started": 1
        })
        st.experimental_rerun()

    return users_data