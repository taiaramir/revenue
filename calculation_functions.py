import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from color_palettes import USER_GROWTH_COLORS, REVENUE_GROWTH_COLORS, REVENUE_BREAKDOWN_COLORS

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

def calculate_revenue(plans, users, years):
    revenue_data = []
    
    for order, user_line in enumerate(users):
        plan = user_line['Plan']
        initial_customers = user_line['Customers']
        initial_users = user_line['Users']
        line_item_name = user_line['Name']
        year_started = user_line['Year Started']
        
        plan_data = plans[plan]
        growth_rate = plan_data['Growth']
        churn_rate = plan_data['Churn']
        
        customers = initial_customers
        users_count = initial_users
        previous_customers = 0
        
        for year in range(1, years + 1):
            if year < year_started:
                # Add zero revenue for years before the start year
                revenue_data.extend([
                    {
                        'Line Item': line_item_name,
                        'Revenue Type': 'Customers',
                        'Year': year,
                        'Amount': 0,
                        'Order': order,
                        'Sub Order': 0
                    },
                    {
                        'Line Item': line_item_name,
                        'Revenue Type': 'Users',
                        'Year': year,
                        'Amount': 0,
                        'Order': order,
                        'Sub Order': 1
                    },
                    {
                        'Line Item': line_item_name,
                        'Revenue Type': f"Platform Revenue (${plan_data['Platform Fee']})",
                        'Year': year,
                        'Amount': 0,
                        'Order': order,
                        'Sub Order': 2
                    },
                    {
                        'Line Item': line_item_name,
                        'Revenue Type': f"Implementation Revenue (${plan_data['Implementation Fee']})",
                        'Year': year,
                        'Amount': 0,
                        'Order': order,
                        'Sub Order': 3
                    },
                    {
                        'Line Item': line_item_name,
                        'Revenue Type': f"Users Revenue (${plan_data['Seat Fee']})",
                        'Year': year,
                        'Amount': 0,
                        'Order': order,
                        'Sub Order': 4
                    },
                    {
                        'Line Item': line_item_name,
                        'Revenue Type': 'Total Revenue',
                        'Year': year,
                        'Amount': 0,
                        'Order': order,
                        'Sub Order': 5
                    }
                ])
                continue

            if year > year_started:
                # Calculate new and churned customers
                new_customers = int(customers * growth_rate)
                churned_customers = int(customers * churn_rate)
                customers = customers + new_customers - churned_customers
                
                new_users = int(users_count * growth_rate)
                churned_users = int(users_count * churn_rate)
                users_count = users_count + new_users - churned_users
            else:
                new_customers = customers  # All customers are new in the first year
            
            platform_revenue = customers * plan_data['Platform Fee'] * 12
            implementation_revenue = (customers - previous_customers) * plan_data['Implementation Fee']
            users_revenue = users_count * plan_data['Seat Fee'] * 12
            total_revenue = platform_revenue + implementation_revenue + users_revenue
            
            revenue_data.extend([
                {
                    'Line Item': line_item_name,
                    'Revenue Type': 'Customers',
                    'Year': year,
                    'Amount': customers,
                    'Order': order,
                    'Sub Order': 0
                },
                {
                    'Line Item': line_item_name,
                    'Revenue Type': 'Users',
                    'Year': year,
                    'Amount': users_count,
                    'Order': order,
                    'Sub Order': 1
                },
                {
                    'Line Item': line_item_name,
                    'Revenue Type': f"Platform Revenue (${plan_data['Platform Fee']})",
                    'Year': year,
                    'Amount': platform_revenue,
                    'Order': order,
                    'Sub Order': 2
                },
                {
                    'Line Item': line_item_name,
                    'Revenue Type': f"Implementation Revenue (${plan_data['Implementation Fee']})",
                    'Year': year,
                    'Amount': implementation_revenue,
                    'Order': order,
                    'Sub Order': 3
                },
                {
                    'Line Item': line_item_name,
                    'Revenue Type': f"Users Revenue (${plan_data['Seat Fee']})",
                    'Year': year,
                    'Amount': users_revenue,
                    'Order': order,
                    'Sub Order': 4
                },
                {
                    'Line Item': line_item_name,
                    'Revenue Type': 'Total Revenue',
                    'Year': year,
                    'Amount': total_revenue,
                    'Order': order,
                    'Sub Order': 5
                }
            ])
            
            previous_customers = customers  # Update previous_customers for the next iteration

    return revenue_data

def display_revenue_table(revenue_data, years):
    st.header(f"Revenue Projection ({years} Year{'s' if years > 1 else ''})")
    
    df = pd.DataFrame(revenue_data)
    
    # Sort the dataframe by the 'Order' and 'Sub Order' columns to maintain the original order
    df = df.sort_values(['Order', 'Sub Order'])
    
    # Pivot the dataframe to have years as columns
    df_pivoted = df.pivot_table(
        values='Amount', 
        index=['Line Item', 'Revenue Type', 'Order', 'Sub Order'],
        columns='Year', 
        aggfunc='sum'
    ).reset_index()
    
    # Rename columns
    df_pivoted.columns = ['Line Item', 'Revenue Type', 'Order', 'Sub Order'] + [f'Year {i}' for i in range(1, years + 1)]
    
    # Sort to maintain Line Item order and put Total Revenue at the end of each group
    df_pivoted = df_pivoted.sort_values(['Order', 'Sub Order'])
    
    # Remove the 'Order' and 'Sub Order' columns as they're no longer needed
    df_pivoted = df_pivoted.drop(['Order', 'Sub Order'], axis=1)
    
    # Calculate grand total
    grand_total = df_pivoted[df_pivoted['Revenue Type'] == 'Total Revenue'].sum().drop(['Line Item', 'Revenue Type'])
    
    # Add grand total row
    grand_total_df = pd.DataFrame({
        'Line Item': ['Grand Total'],
        'Revenue Type': [''],
        **{f'Year {i}': [grand_total[f'Year {i}']] for i in range(1, years + 1)}
    })
    
    df_final = pd.concat([df_pivoted, grand_total_df], ignore_index=True)

    # Format values
    for year in range(1, years + 1):
        df_final[f'Year {year}'] = df_final.apply(
            lambda row: f"{int(row[f'Year {year}']):,}" if row['Revenue Type'] in ['Customers', 'Users'] 
                   else f"${int(row[f'Year {year}']):,}" if row['Revenue Type'] != '' or row['Line Item'] == 'Grand Total'
                   else row[f'Year {year}'],
            axis=1
        )

    
    # Apply styling to the dataframe
    def style_dataframe(df):
        styles = [
            dict(selector="th", props=[("font-weight", "bold"), ("text-align", "left"), ("font-size", "13px")]),
            dict(selector="td", props=[("text-align", "left"), ("font-size", "13px"), ("white-space", "nowrap")])
        ]
        
        colors = ['#e6f3ff', '#cce7ff', '#b3dbff', '#99cfff', '#80c3ff']  # Light blue shades
        
        def color_rows(row):
            if row.name == len(df) - 1:  # Grand Total row
                return ['background-color: #4da6ff'] * (years + 2)
            else:
                line_item_index = df['Line Item'].unique().tolist().index(row['Line Item'])
                return [f'background-color: {colors[line_item_index % len(colors)]}'] * (years + 2)
        
        return (df.style
                .set_table_styles(styles)
                .set_properties(**{'color': 'black', 'border': '1px solid white'})
                .apply(lambda x: ['font-weight: bold' if x.name == len(df) - 1 or x['Revenue Type'] == 'Total Revenue' else '' for _ in x], axis=1)
                .apply(color_rows, axis=1)
               )

    styled_df = style_dataframe(df_final)
    
    # Create a container with horizontal scrolling for the table
    st.markdown("""
    <style>
    .table-container {
        width: 100%;
        overflow-x: auto;
    }
    .table-container table {
        width: 100%;
        border-collapse: collapse;
    }
    .table-container th, .table-container td {
        padding: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    st.write(styled_df.to_html(escape=False, index=False), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    import plotly.graph_objects as go
import streamlit as st
from color_palettes import REVENUE_BREAKDOWN_COLORS

#Charts and Graphs

import plotly.graph_objects as go
import streamlit as st
from color_palettes import REVENUE_BREAKDOWN_COLORS

def display_revenue_breakdown_chart(revenue_data, years):
    # Filter the data for the latest year and relevant revenue types
    latest_year = max(item['Year'] for item in revenue_data)
    relevant_types = ['Platform Revenue', 'Implementation Revenue', 'Users Revenue']
    
    filtered_data = [
        item for item in revenue_data 
        if item['Year'] == latest_year and any(rt in item['Revenue Type'] for rt in relevant_types)
    ]
    
    # Prepare data for the chart
    line_items = list(set(item['Line Item'] for item in filtered_data))
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