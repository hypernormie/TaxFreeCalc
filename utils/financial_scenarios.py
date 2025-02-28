import numpy as np

def calculate_home_purchase_potential(total_tax):
    """Calculate potential home purchase scenarios with real examples"""
    down_payment = total_tax
    max_mortgage = down_payment * 4  # Typical 4x leverage

    scenarios = {
        'starter_home': {
            'down_payment': down_payment,
            'max_home_value': down_payment + (max_mortgage * 0.8),
            'monthly_payment': (max_mortgage * 0.8 * 0.06) / 12,
            'time_saved': '2-3 years',  # Time saved in down payment accumulation
            'description': 'Perfect for first-time homebuyers',
            'example_properties': [
                'Two-bedroom condo in suburban area',
                'Townhouse in growing community',
                'Small detached home in smaller cities'
            ]
        },
        'family_home': {
            'down_payment': down_payment,
            'max_home_value': down_payment + max_mortgage,
            'monthly_payment': (max_mortgage * 0.06) / 12,
            'time_saved': '4-5 years',
            'description': 'Ideal for growing families',
            'example_properties': [
                'Three-bedroom detached house',
                'Large townhouse with garage',
                'Semi-detached home in established neighborhood'
            ]
        }
    }
    return scenarios

def calculate_investment_growth(total_tax, years=30):
    """Calculate long-term investment growth potential"""
    monthly_contribution = total_tax / 12
    years_range = list(range(1, years + 1))

    scenarios = {
        'conservative': {
            'rate': 0.06,  # 6% annual return
            'strategy': 'Low-risk index funds and bonds',
            'growth': [],
            'retirement_potential': 'Retire 5 years earlier',
            'description': 'Steady, reliable growth with lower risk'
        },
        'balanced': {
            'rate': 0.08,  # 8% annual return
            'strategy': 'Diversified portfolio',
            'growth': [],
            'retirement_potential': 'Retire 8 years earlier',
            'description': 'Mix of growth and stability'
        },
        'aggressive': {
            'rate': 0.10,  # 10% annual return
            'strategy': 'Growth-focused stocks',
            'growth': [],
            'retirement_potential': 'Retire 10+ years earlier',
            'description': 'Maximum growth potential with higher risk'
        }
    }

    # Calculate compound growth for each scenario
    for scenario in scenarios.values():
        principal = total_tax
        annual_contribution = total_tax  # Assuming same tax savings each year
        accumulated = []

        for year in years_range:
            # Compound interest formula with annual contributions
            amount = principal * (1 + scenario['rate']) ** year
            contribution_growth = annual_contribution * ((1 + scenario['rate']) ** year - 1) / scenario['rate']
            total = amount + contribution_growth

            accumulated.append({
                'year': year,
                'value': round(total, 2),
                'contributions': round(annual_contribution * year, 2),
                'earnings': round(total - (annual_contribution * year), 2)
            })

        scenario['growth'] = accumulated

    return scenarios, years_range

def calculate_alternative_uses(total_tax):
    """Calculate alternative uses and their long-term impact"""
    monthly_tax = total_tax / 12

    return {
        'education': {
            'title': 'Education & Skills',
            'description': f"${total_tax:,.2f} could fund:",
            'examples': [
                'Complete MBA or Master\'s degree',
                'Professional certifications and skills training',
                'Starting a small business'
            ],
            'impact': 'Potential 20-30% income increase'
        },
        'business': {
            'title': 'Business Ventures',
            'description': f"${total_tax:,.2f} could start:",
            'examples': [
                'Small consulting practice',
                'Online business',
                'Franchise opportunity'
            ],
            'impact': 'Build equity and create jobs'
        },
        'lifestyle': {
            'title': 'Life Quality',
            'description': f"${monthly_tax:,.2f} extra monthly could provide:",
            'examples': [
                'Quality healthcare and wellness programs',
                'Better work-life balance through reduced hours',
                'Enhanced retirement savings'
            ],
            'impact': 'Improved quality of life and health'
        }
    }

def calculate_debt_payment(total_tax):
    """Calculate detailed debt payment scenarios with practical examples"""
    debt_types = {
        'credit_card': {
            'rate': 0.1999,
            'priority': 'High',
            'description': 'High-interest debt that should be prioritized',
            'monthly_savings': (total_tax * 0.1999) / 12,
            'example_impact': 'Eliminate $20,000 credit card debt and save $4,000 yearly in interest'
        },
        'student_loan': {
            'rate': 0.0599,
            'priority': 'Medium',
            'description': 'Consider alongside tax benefits',
            'monthly_savings': (total_tax * 0.0599) / 12,
            'example_impact': 'Pay off student loans years earlier and reduce total interest paid'
        },
        'car_loan': {
            'rate': 0.0699,
            'priority': 'Medium',
            'description': 'Consider if refinancing is beneficial',
            'monthly_savings': (total_tax * 0.0699) / 12,
            'example_impact': 'Fully own your vehicle sooner and redirect payments to savings'
        },
        'mortgage': {
            'rate': 0.0559,
            'priority': 'Low',
            'description': 'Consider alongside investment opportunities',
            'monthly_savings': (total_tax * 0.0559) / 12,
            'example_impact': 'Reduce mortgage term and save thousands in interest'
        }
    }

    for debt_type in debt_types.values():
        debt_type['five_year_savings'] = debt_type['monthly_savings'] * 12 * 5

    return debt_types

def calculate_retirement_impact(total_tax, current_age=35):
    """Calculate retirement planning scenarios with real-world examples"""
    retirement_ages = [55, 60, 65]
    monthly_withdrawal = total_tax / 240  # Assuming 20 years of retirement

    scenarios = {}
    for retirement_age in retirement_ages:
        years_to_grow = retirement_age - current_age
        if years_to_grow > 0:
            conservative_value = total_tax * (1.06 ** years_to_grow)
            balanced_value = total_tax * (1.08 ** years_to_grow)
            aggressive_value = total_tax * (1.10 ** years_to_grow)

            scenarios[retirement_age] = {
                'years_to_retirement': years_to_grow,
                'conservative_value': round(conservative_value, 2),
                'balanced_value': round(balanced_value, 2),
                'aggressive_value': round(aggressive_value, 2),
                'monthly_income_potential': round(monthly_withdrawal, 2),
                'lifestyle_examples': [
                    f'Annual vacation budget: ${monthly_withdrawal * 2:,.2f}',
                    f'Monthly housing budget: ${monthly_withdrawal * 0.4:,.2f}',
                    f'Healthcare savings: ${monthly_withdrawal * 0.15:,.2f}',
                    f'Entertainment & dining: ${monthly_withdrawal * 0.2:,.2f}'
                ]
            }

    return scenarios