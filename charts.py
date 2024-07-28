import streamlit as st
import plotly.graph_objects as go
from color_palettes import USER_GROWTH_COLORS, REVENUE_GROWTH_COLORS, REVENUE_BREAKDOWN_COLORS

def display_user_growth_chart(revenue_data, years):
    # Filter the data for 'Users' rows
    users_data = [item for item in revenue_data if item['Revenue Type'] == 'Users']
    
    # Create a dictionary to store user counts for each line item
    line_items = {}
    for item in users_data:
        if item['Line Item'] not in line_items:
            line_items[item['Line Item']] = [0] * years
        line_items[item['Line Item']][item['Year'] - 1] = item['Amount']
    
    # Create the line chart
    fig = go.Figure()
    
    # Use the imported color palette
    colors = USER_GROWTH_COLORS
    
    for i, (line_item, users) in enumerate(line_items.items()):
        fig.add_trace(go.Scatter(
            x=list(range(1, years + 1)),
            y=users,
            mode='lines+markers',
            name=line_item,
            line=dict(color=colors[i % len(colors)], width=2),
            marker=dict(color=colors[i % len(colors)], size=8)
        ))
    
    fig.update_layout(
        title='User Growth Over Time',
        xaxis_title='Year',
        yaxis_title='Number of Users',
        legend_title='Line Items',
        hovermode='x unified',
        height=500
    )
    
    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

def display_revenue_growth_chart(revenue_data, years):
    # Filter the data for 'Total Revenue' rows and get unique line items
    total_revenue_data = {}
    for item in revenue_data:
        if item['Revenue Type'] == 'Total Revenue':
            line_item = item['Line Item']
            year = item['Year']
            if line_item not in total_revenue_data:
                total_revenue_data[line_item] = [0] * years
            total_revenue_data[line_item][year - 1] = item['Amount']
    
    # Create the line chart
    fig = go.Figure()
    
    # Use the imported color palette
    colors = REVENUE_GROWTH_COLORS
    
    for i, (line_item, revenue) in enumerate(total_revenue_data.items()):
        fig.add_trace(go.Scatter(
            x=list(range(1, years + 1)),
            y=revenue,
            mode='lines+markers',
            name=line_item,
            line=dict(color=colors[i % len(colors)], width=2),
            marker=dict(color=colors[i % len(colors)], size=8)
        ))
    
    fig.update_layout(
        title='Total Revenue Growth Over Time',
        xaxis_title='Year',
        yaxis_title='Total Revenue ($)',
        legend_title='Line Items',
        hovermode='x unified',
        height=500
    )
    
    # Format y-axis labels as currency
    fig.update_layout(yaxis=dict(tickformat='$,.0f'))
    
    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

def display_revenue_breakdown_chart(revenue_data, years, users_data):
    # Filter the data for the latest year and relevant revenue types
    latest_year = max(item['Year'] for item in revenue_data)
    relevant_types = ['Platform Revenue', 'Implementation Revenue', 'Users Revenue', 'Workspaces Revenue']
    
    filtered_data = [
        item for item in revenue_data 
        if item['Year'] == latest_year and any(rt in item['Revenue Type'] for rt in relevant_types)
    ]
    
    # Create a dictionary to store the order of line items
    line_item_order = {user['Name']: user['Order'] for user in users_data}
    
    # Prepare data for the chart
    line_items = list(set(item['Line Item'] for item in filtered_data))
    # Sort line items based on the order in users_data
    line_items.sort(key=lambda x: line_item_order.get(x, float('inf')))
    
    revenue_types = relevant_types
    
    data = {rt: [] for rt in revenue_types}
    for line_item in line_items:
        for rt in revenue_types:
            revenue = next((item['Amount'] for item in filtered_data if item['Line Item'] == line_item and rt in item['Revenue Type']), 0)
            data[rt].append(revenue)
    
    # Create the stacked bar chart
    fig = go.Figure()
    
    colors = REVENUE_BREAKDOWN_COLORS
    
    for i, (rt, values) in enumerate(data.items()):
        fig.add_trace(go.Bar(
            name=rt,
            x=line_items,
            y=values,
            marker_color=colors[i % len(colors)]
        ))
    
    fig.update_layout(
        title=f'Revenue Breakdown by Line Item (Year {latest_year})',
        xaxis_title='Line Items',
        yaxis_title='Revenue ($)',
        barmode='stack',
        height=500,
        legend_title='Revenue Types',
        hovermode='x unified'
    )
    
    # Format y-axis labels as currency
    fig.update_layout(yaxis=dict(tickformat='$,.0f'))
    
    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)