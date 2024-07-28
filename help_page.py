import streamlit as st

def display_math_explanation():
    st.header("Revenue Calculation Explanation")
    
    st.markdown("""
    This page explains the calculations used in the revenue projection table.

    1. **Companies and Users Growth**: 
       - We start with the initial number of companies and users you provided.
       - Each year, we apply the growth rate to increase these numbers.
       - We also apply the churn rate to simulate companies and users that leave.
       - Example: If you start with 100 companies, have a 20% growth rate and 5% churn rate, next year you'll have:
         100 + (100 * 20%) - (100 * 5%) = 115 companies

    2. **Platform Revenue**:
       - Calculated as: Number of Companies × Platform Fee × 12 months
       - Example: If you have 115 companies and a Platform Fee of $100/month:
         115 × $100 × 12 = $138,000 annual Platform Revenue

    3. **Implementation Revenue**:
       - Only charged for new companies each year
       - Calculated as: (New Companies this year - Companies last year) × Implementation Fee
       - Example: If you gained 15 new companies and the Implementation Fee is $500:
         15 × $500 = $7,500 Implementation Revenue

    4. **Users Revenue**:
       - Calculated as: Number of Users × User Fee × 12 months
       - Example: If you have 1000 users and a User Fee of $50/month:
         1000 × $50 × 12 = $600,000 annual Users Revenue

    5. **Workspaces Revenue**:
       - Calculated as: Number of Workspaces × Workspace Fee × 12 months
       - Example: If you have 50 workspaces and a Workspace Fee of $200/month:
         50 × $200 × 12 = $120,000 annual Workspaces Revenue

    6. **Total Revenue**:
       - Sum of Platform Revenue, Implementation Revenue, Users Revenue, and Workspaces Revenue
       - Example: $138,000 + $7,500 + $600,000 + $120,000 = $865,500 Total Revenue

    Note: These calculations are performed for each line item and each year in the projection.
    """)