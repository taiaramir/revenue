import streamlit as st
import pandas as pd
import numpy as np

import streamlit as st
import pandas as pd
import numpy as np

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
    
    # Calculate total
    total = df_pivoted[df_pivoted['Revenue Type'] == 'Total Revenue'].sum().drop(['Line Item', 'Revenue Type'])
    
    # Add total row
    total_df = pd.DataFrame({
        'Line Item': ['Total'],
        'Revenue Type': [''],
        **{f'Year {i}': [total[f'Year {i}']] for i in range(1, years + 1)}
    })
    
    # Calculate grand total (cumulative sum)
    grand_total = total.cumsum()
    
    # Add grand total row
    grand_total_df = pd.DataFrame({
        'Line Item': ['Grand Total'],
        'Revenue Type': [''],
        **{f'Year {i}': [grand_total[f'Year {i}']] for i in range(1, years + 1)}
    })
    
    df_final = pd.concat([df_pivoted, total_df, grand_total_df], ignore_index=True)

    # Format values
    for year in range(1, years + 1):
        df_final[f'Year {year}'] = df_final.apply(
            lambda row: format_value(row, year),
            axis=1
        )

    # Apply styling to the dataframe
    styled_df = style_dataframe(df_final, years)
    
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

def format_value(row, year):
    value = row[f'Year {year}']
    if pd.isna(value) or np.isnan(value):
        return ''
    elif row['Revenue Type'] in ['Companies', 'Users', 'Workspaces']:  # Added 'Workspaces' here
        return f"{int(value):,}"
    elif (row['Revenue Type'] not in ['Companies', 'Users', 'Workspaces'] and row['Revenue Type'] != '') or row['Line Item'] in ['Total', 'Grand Total']:
        return f"${int(value):,}"
    else:
        return value

def style_dataframe(df, years):
    styles = [
        dict(selector="th", props=[("font-weight", "bold"), ("text-align", "left"), ("font-size", "13px")]),
        dict(selector="td", props=[("text-align", "left"), ("font-size", "13px"), ("white-space", "nowrap")])
    ]
    
    colors = ['#e6f3ff', '#cce7ff', '#b3dbff', '#99cfff', '#80c3ff']  # Light blue shades
    
    def color_rows(row):
        if row['Line Item'] == 'Grand Total':
            return ['background-color: #3399ff'] * (years + 2)  # Darker blue for Grand Total
        elif row['Line Item'] == 'Total':
            return ['background-color: #4da6ff'] * (years + 2)  # Slightly lighter blue for Total
        elif row['Revenue Type'] == 'Total Revenue':
            return ['background-color: #66b3ff'] * (years + 2)  # Even lighter blue for Total Revenue
        else:
            line_item_index = df['Line Item'].unique().tolist().index(row['Line Item'])
            return [f'background-color: {colors[line_item_index % len(colors)]}'] * (years + 2)
    
    return (df.style
            .set_table_styles(styles)
            .set_properties(**{'color': 'black', 'border': '1px solid white'})
            .apply(lambda x: ['font-weight: bold' if x['Line Item'] in ['Total', 'Grand Total'] or x['Revenue Type'] == 'Total Revenue' else '' for _ in x], axis=1)
            .apply(color_rows, axis=1)
           )