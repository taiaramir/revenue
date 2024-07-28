def calculate_revenue(plans, users, years):
    revenue_data = []
    
    for order, user_line in enumerate(users):
        plan = user_line['Plan']
        initial_companies = user_line['Companies']
        initial_users = user_line['Users']
        initial_workspaces = user_line['Workspaces']
        line_item_name = user_line['Name']
        year_started = user_line['Year Started']
        
        plan_data = plans[plan]
        growth_rate = plan_data['Growth'] / 100  # Convert percentage to decimal
        churn_rate = plan_data['Churn'] / 100  # Convert percentage to decimal
        
        companies = initial_companies
        users_count = initial_users
        workspaces_count = initial_workspaces
        previous_companies = 0
        
        for year in range(1, years + 1):
            if year < year_started:
                # Skip years before the line item starts
                continue

            if year > year_started:
                # Calculate new and churned companies, users, and workspaces
                new_companies = int(companies * growth_rate)
                churned_companies = int(companies * churn_rate)
                companies = companies + new_companies - churned_companies
                
                new_users = int(users_count * growth_rate)
                churned_users = int(users_count * churn_rate)
                users_count = users_count + new_users - churned_users
                
                new_workspaces = int(workspaces_count * growth_rate)
                churned_workspaces = int(workspaces_count * churn_rate)
                workspaces_count = workspaces_count + new_workspaces - churned_workspaces
            else:
                new_companies = companies  # All companies are new in the first year
            
            platform_revenue = companies * plan_data['Platform Fee'] * 12
            implementation_revenue = (companies - previous_companies) * plan_data['Implementation Fee']
            users_revenue = users_count * plan_data['User Fee'] * 12
            workspaces_revenue = workspaces_count * plan_data['Workspace Fee'] * 12
            total_revenue = platform_revenue + implementation_revenue + users_revenue + workspaces_revenue
            
            revenue_data.extend([
                {
                    'Line Item': line_item_name,
                    'Revenue Type': 'Companies',
                    'Year': year,
                    'Amount': companies,
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
                    'Revenue Type': 'Workspaces',
                    'Year': year,
                    'Amount': workspaces_count,
                    'Order': order,
                    'Sub Order': 2
                },
                {
                    'Line Item': line_item_name,
                    'Revenue Type': f"Platform Revenue (${plan_data['Platform Fee']})",
                    'Year': year,
                    'Amount': platform_revenue,
                    'Order': order,
                    'Sub Order': 3
                },
                {
                    'Line Item': line_item_name,
                    'Revenue Type': f"Implementation Revenue (${plan_data['Implementation Fee']})",
                    'Year': year,
                    'Amount': implementation_revenue,
                    'Order': order,
                    'Sub Order': 4
                },
                {
                    'Line Item': line_item_name,
                    'Revenue Type': f"Users Revenue (${plan_data['User Fee']})",
                    'Year': year,
                    'Amount': users_revenue,
                    'Order': order,
                    'Sub Order': 5
                },
                {
                    'Line Item': line_item_name,
                    'Revenue Type': f"Workspaces Revenue (${plan_data['Workspace Fee']})",
                    'Year': year,
                    'Amount': workspaces_revenue,
                    'Order': order,
                    'Sub Order': 6
                },
                {
                    'Line Item': line_item_name,
                    'Revenue Type': 'Total Revenue',
                    'Year': year,
                    'Amount': total_revenue,
                    'Order': order,
                    'Sub Order': 7
                }
            ])
            
            previous_companies = companies  # Update previous_companies for the next iteration

    return revenue_data