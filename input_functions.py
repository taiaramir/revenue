import streamlit as st

def get_plan_inputs():
    st.header("Plans")
    
    plan_types = ["Basic", "Pro", "Enterprise"]
    tabs = st.tabs(plan_types)
    
    plans_data = {}
    
    for i, tab in enumerate(tabs):
        with tab:
            plan_type = plan_types[i]
            st.subheader(f"{plan_type} Plan")
            
            col1, space, col2 = st.columns([1, 0.1, 1])
            
            with col1:
                st.markdown("<h5 style='color: #888888; font-size: 14px;'>Pricing</h5>", unsafe_allow_html=True)
                platform_fee = st.number_input("Platform Fee/month ($)", 
                                               min_value=0, 
                                               value=100, 
                                               step=1, 
                                               key=f"platform_fee_{plan_type}")
                
                seat_fee = st.number_input("Additional Fee for Seat/user/month ($)", 
                                           min_value=0, 
                                           value=50, 
                                           step=1, 
                                           key=f"seat_fee_{plan_type}")
                
                if plan_type == "Basic":
                    workspace_fee = st.text_input("Additional Fee for Workspace/workspace/month ($)", 
                                                  value="Not available", 
                                                  disabled=True, 
                                                  key=f"workspace_fee_{plan_type}")
                else:
                    workspace_fee = st.number_input("Additional Fee for Workspace/workspace/month ($)", 
                                                    min_value=0, 
                                                    value=100, 
                                                    step=1, 
                                                    key=f"workspace_fee_{plan_type}")
                
                implementation_fee = st.number_input("Implementation Fee/One-Time ($)", 
                                                     min_value=0, 
                                                     value=500, 
                                                     step=1, 
                                                     key=f"implementation_fee_{plan_type}")

            with col2:
                st.markdown("<h5 style='color: #888888; font-size: 14px;'>Variables</h5>", unsafe_allow_html=True)
                growth = st.number_input("Growth (%)", 
                                         min_value=0, 
                                         value=150, 
                                         step=1, 
                                         key=f"growth_{plan_type}")
                
                churn = st.number_input("Churn (%)", 
                                        min_value=0, 
                                        value=30, 
                                        step=1, 
                                        key=f"churn_{plan_type}")
                
                extra_workspaces = st.number_input("Extra Workspaces (%)", 
                                                   min_value=0, 
                                                   value=35, 
                                                   step=1, 
                                                   key=f"extra_workspaces_{plan_type}")
                
                extra_seats = st.number_input("Extra Seats (%)", 
                                              min_value=0, 
                                              value=15, 
                                              step=1, 
                                              key=f"extra_seats_{plan_type}")
            
            plans_data[plan_type] = {
                "name": plan_type,
                "Platform Fee": platform_fee,
                "Seat Fee": seat_fee,
                "Workspace Fee": workspace_fee,
                "Implementation Fee": implementation_fee,
                "Growth": growth / 100,  # Convert percentage to decimal
                "Churn": churn / 100,
                "Extra Workspaces": extra_workspaces / 100,
                "Extra Seats": extra_seats / 100
            }
    
    return plans_data

def get_user_inputs():
    st.header("Users")

    # Use session state to keep track of the user lines
    if 'user_lines' not in st.session_state:
        st.session_state.user_lines = [{"name": "Line item #1", "plan": "Basic", "customers": 0, "users": 0, "year_started": 1}]

    users_data = []

    # Reduce gaps by using custom CSS
    st.markdown("""
    <style>
    .stContainer {
        padding-left: 1rem;
        padding-right: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

    for i, user_line in enumerate(st.session_state.user_lines):
        col_name, col1, col2, col3, col4, col_delete = st.columns([3, 2, 2, 2, 2, 1])
        
        with col_name:
            name = st.text_input("Name", value=user_line.get("name", f"Line item #{i+1}"), key=f"name_{i}")
        
        with col1:
            plan = st.selectbox("Plan", ["Basic", "Pro", "Enterprise"], key=f"plan_{i}", index=["Basic", "Pro", "Enterprise"].index(user_line["plan"]))
        
        with col2:
            customers = st.number_input("Customers", min_value=0, step=1, key=f"customers_{i}", value=user_line["customers"])
        
        with col3:
            users = st.number_input("Users", min_value=0, step=1, key=f"users_{i}", value=user_line["users"])
        
        with col4:
            year_started = st.number_input("Year Started", min_value=1, step=1, key=f"year_started_{i}", value=user_line.get("year_started", 1))
        
        with col_delete:
            if len(st.session_state.user_lines) > 1:
                if st.button("🗑️", key=f"delete_{i}"):
                    st.session_state.user_lines.pop(i)
                    st.experimental_rerun()

        users_data.append({
            "Name": name,
            "Plan": plan,
            "Customers": customers,
            "Users": users,
            "Year Started": year_started
        })

        # Update session state
        st.session_state.user_lines[i] = {"name": name, "plan": plan, "customers": customers, "users": users, "year_started": year_started}

    # Add button with green color
    if st.button("Add", type="primary"):
        new_line_number = len(st.session_state.user_lines) + 1
        st.session_state.user_lines.append({"name": f"Line item #{new_line_number}", "plan": "Basic", "customers": 0, "users": 0, "year_started": 1})
        st.experimental_rerun()

    return users_data