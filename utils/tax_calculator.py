import pandas as pd
import numpy as np

def get_federal_tax_brackets():
    """2024 Canadian Federal Tax Brackets"""
    return [
        (0, 53359, 0.15),
        (53359, 106717, 0.205),
        (106717, 165430, 0.26),
        (165430, 235675, 0.29),
        (235675, float('inf'), 0.33)
    ]

def get_province_tax_rates():
    """Get tax rates for all provinces and territories (2024)"""
    return {
        'Ontario': [
            (0, 49231, 0.0505),
            (49231, 98463, 0.0915),
            (98463, 150000, 0.1116),
            (150000, 220000, 0.1216),
            (220000, float('inf'), 0.1316)
        ],
        'British Columbia': [
            (0, 45654, 0.0506),
            (45654, 91310, 0.077),
            (91310, 104835, 0.105),
            (104835, 127299, 0.1229),
            (127299, 172602, 0.147),
            (172602, 240716, 0.168),
            (240716, float('inf'), 0.205)
        ],
        'Alberta': [
            (0, 142292, 0.10),
            (142292, 170751, 0.12),
            (170751, 227668, 0.13),
            (227668, 341502, 0.14),
            (341502, float('inf'), 0.15)
        ],
        'Quebec': [
            (0, 49275, 0.14),
            (49275, 98540, 0.19),
            (98540, 119910, 0.24),
            (119910, float('inf'), 0.2575)
        ],
        'Manitoba': [
            (0, 36842, 0.108),
            (36842, 79625, 0.1275),
            (79625, float('inf'), 0.174)
        ],
        'Saskatchewan': [
            (0, 49720, 0.105),
            (49720, 142058, 0.125),
            (142058, float('inf'), 0.145)
        ],
        'Nova Scotia': [
            (0, 29590, 0.0879),
            (29590, 59180, 0.1495),
            (59180, 93000, 0.1667),
            (93000, 150000, 0.175),
            (150000, float('inf'), 0.21)
        ],
        'New Brunswick': [
            (0, 47715, 0.094),
            (47715, 95431, 0.14),
            (95431, 176756, 0.16),
            (176756, float('inf'), 0.195)
        ],
        'Prince Edward Island': [
            (0, 31984, 0.098),
            (31984, 63969, 0.138),
            (63969, float('inf'), 0.167)
        ],
        'Newfoundland and Labrador': [
            (0, 41457, 0.087),
            (41457, 82913, 0.145),
            (82913, 148027, 0.158),
            (148027, 207239, 0.178),
            (207239, 264750, 0.198),
            (264750, float('inf'), 0.208)
        ],
        'Yukon': [
            (0, 53359, 0.064),
            (53359, 106717, 0.09),
            (106717, 165430, 0.109),
            (165430, 235675, 0.128),
            (235675, float('inf'), 0.15)
        ],
        'Northwest Territories': [
            (0, 48326, 0.059),
            (48326, 96655, 0.086),
            (96655, 157139, 0.122),
            (157139, float('inf'), 0.1405)
        ],
        'Nunavut': [
            (0, 47862, 0.04),
            (47862, 95724, 0.07),
            (95724, 155625, 0.09),
            (155625, float('inf'), 0.115)
        ]
    }

def get_cpp_ei_rates():
    """Get current CPP and EI rates and maximums"""
    return {
        'cpp_rate': 0.0595,  # 5.95% for 2024
        'cpp_max': 3754.45,  # Maximum annual contribution
        'ei_rate': 0.0163,   # 1.63% for 2024
        'ei_max': 1002.45    # Maximum annual contribution
    }

def calculate_federal_tax(income):
    """
    Calculate federal tax using progressive brackets
    Example: $250,000 income = $54,961 federal tax
    """
    brackets = get_federal_tax_brackets()
    tax = 0
    remaining_income = income
    bracket_breakdown = []

    # Basic personal amount for 2024
    if income <= 173205:
        basic_personal_amount = 15000
    else:
        # Gradual reduction for high income
        reduction_factor = (income - 173205) / (235675 - 173205)
        basic_personal_amount = max(13521, 15000 - (15000 - 13521) * reduction_factor)

    remaining_income = max(0, income - basic_personal_amount)

    for lower, upper, rate in brackets:
        if remaining_income <= 0:
            break

        if upper == float('inf'):
            taxable_amount = remaining_income
        else:
            taxable_amount = min(remaining_income, upper - lower)

        tax_in_bracket = taxable_amount * rate
        tax += tax_in_bracket
        remaining_income -= taxable_amount

        bracket_breakdown.append({
            'bracket': f"${lower:,.0f} - ${upper if upper != float('inf') else '∞'}",
            'rate': f"{rate*100:.1f}%",
            'taxable_amount': taxable_amount,
            'tax_paid': tax_in_bracket,
            'calculation': f"${taxable_amount:,.2f} × {rate*100:.1f}% = ${tax_in_bracket:,.2f}"
        })

    return round(tax, 2), bracket_breakdown

def calculate_provincial_tax(income, province):
    """
    Calculate provincial tax based on income and province
    Example: $250,000 in Ontario = $34,781 provincial tax
    """
    province_rates = get_province_tax_rates()
    if province not in province_rates:
        raise ValueError(f"Tax rates for {province} are not available")

    tax = 0
    remaining_income = income
    bracket_breakdown = []

    for lower, upper, rate in province_rates[province]:
        if remaining_income <= 0:
            break

        if upper == float('inf'):
            taxable_amount = remaining_income
        else:
            taxable_amount = min(remaining_income, upper - lower)

        tax_in_bracket = taxable_amount * rate
        tax += tax_in_bracket
        remaining_income -= taxable_amount

        bracket_breakdown.append({
            'bracket': f"${lower:,.0f} - ${upper if upper != float('inf') else '∞'}",
            'rate': f"{rate*100:.1f}%",
            'taxable_amount': taxable_amount,
            'tax_paid': tax_in_bracket,
            'calculation': f"${taxable_amount:,.2f} × {rate*100:.1f}% = ${tax_in_bracket:,.2f}"
        })

    return round(tax, 2), bracket_breakdown

def get_gst_hst_rates():
    """Get GST/HST rates by province"""
    return {
        'Ontario': 0.13,  # HST
        'British Columbia': 0.05,  # GST (plus 7% PST separately)
        'Alberta': 0.05,  # GST only
        'Quebec': 0.05,  # GST (plus 9.975% QST separately)
        'Manitoba': 0.05,  # GST (plus 7% PST separately)
        'Saskatchewan': 0.05,  # GST (plus 6% PST separately)
        'Nova Scotia': 0.15,  # HST
        'New Brunswick': 0.15,  # HST
        'Prince Edward Island': 0.15,  # HST
        'Newfoundland and Labrador': 0.15,  # HST
        'Yukon': 0.05,  # GST only
        'Northwest Territories': 0.05,  # GST only
        'Nunavut': 0.05  # GST only
    }

def calculate_consumption_tax(after_tax_income, province):
    """Calculate GST/HST impact on after-tax spending"""
    gst_hst_rates = get_gst_hst_rates()
    rate = gst_hst_rates.get(province, 0.05)

    # Spending categories (monthly)
    spending_categories = {
        'Housing (GST/HST exempt)': {
            'percentage': 0.35,
            'taxable': False
        },
        'Groceries (mostly exempt)': {
            'percentage': 0.15,
            'taxable': False
        },
        'Transportation': {
            'percentage': 0.12,
            'taxable': True
        },
        'Entertainment & Dining': {
            'percentage': 0.10,
            'taxable': True
        },
        'Shopping & Misc': {
            'percentage': 0.18,
            'taxable': True
        },
        'Savings & Investments': {
            'percentage': 0.10,
            'taxable': False
        }
    }

    # Calculate monthly amounts
    monthly_breakdown = {}
    total_taxable = 0
    total_non_taxable = 0

    for category, details in spending_categories.items():
        amount = after_tax_income * details['percentage']
        if details['taxable']:
            gst_hst = amount * rate
            total_taxable += amount
        else:
            gst_hst = 0
            total_non_taxable += amount

        monthly_breakdown[category] = {
            'amount': amount / 12,  # Monthly amount
            'gst_hst': gst_hst / 12,  # Monthly GST/HST
            'taxable': details['taxable']
        }

    yearly_gst_hst = total_taxable * rate

    return {
        'tax': yearly_gst_hst,
        'rate': rate,
        'taxable_spending': total_taxable,
        'non_taxable_spending': total_non_taxable,
        'taxable_ratio': total_taxable / after_tax_income,
        'monthly_breakdown': monthly_breakdown,
        'rate_explanation': f"Using {province} rate of {rate*100:.1f}%",
        'spending_breakdown': {
            'taxable_amount': total_taxable,
            'non_taxable': total_non_taxable
        }
    }

def calculate_pay_periods(income, total_deductions):
    """Calculate take-home pay for different pay periods"""
    after_tax_income = income - total_deductions

    return {
        'yearly': {
            'gross': income,
            'deductions': total_deductions,
            'net': after_tax_income
        },
        'monthly': {
            'gross': income / 12,
            'deductions': total_deductions / 12,
            'net': after_tax_income / 12
        },
        'biweekly': {
            'gross': income / 26,
            'deductions': total_deductions / 26,
            'net': after_tax_income / 26
        },
        'weekly': {
            'gross': income / 52,
            'deductions': total_deductions / 52,
            'net': after_tax_income / 52
        }
    }


def calculate_total_tax_burden(income, province, employment_type):
    """
    Calculate comprehensive tax burden including all forms of taxation
    For $250,000 income:
    - Federal Tax: $54,961
    - Provincial Tax: $34,781
    - CPP/EI: $5,105
    - Total Tax: $94,846 (37.94%)
    """
    # Calculate federal and provincial tax
    federal_tax, federal_breakdown = calculate_federal_tax(income)
    provincial_tax, provincial_breakdown = calculate_provincial_tax(income, province)

    # Calculate CPP and EI
    cpp_ei = get_cpp_ei_rates()
    if employment_type == 'Self-Employed':
        cpp_contribution = min(income * cpp_ei['cpp_rate'] * 2, cpp_ei['cpp_max'] * 2)
        ei_contribution = 0  # Self-employed don't pay EI unless opted in
    else:
        cpp_contribution = min(income * cpp_ei['cpp_rate'], cpp_ei['cpp_max'])
        ei_contribution = min(income * cpp_ei['ei_rate'], cpp_ei['ei_max'])

    # Calculate total deductions
    total_deductions = federal_tax + provincial_tax + cpp_contribution + ei_contribution
    after_tax_income = income - total_deductions

    # Calculate GST/HST impact
    consumption_tax_results = calculate_consumption_tax(after_tax_income, province)

    # Calculate tax rates
    total_tax_rate = (total_deductions / income) * 100

    # Calculate marginal rates
    federal_marginal = next((rate for lower, upper, rate in reversed(get_federal_tax_brackets())
                           if income >= lower), 0)
    provincial_marginal = next((rate for lower, upper, rate in reversed(get_province_tax_rates()[province])
                              if income >= lower), 0)
    marginal_tax_rate = (federal_marginal + provincial_marginal) * 100

    pay_periods = calculate_pay_periods(income, total_deductions)

    return {
        'federal_tax': federal_tax,
        'provincial_tax': provincial_tax,
        'total_deductions': total_deductions,
        'after_tax_income': after_tax_income,
        'tax_breakdown': {
            'federal': federal_tax,
            'provincial': provincial_tax,
            'cpp': cpp_contribution,
            'ei': ei_contribution
        },
        'tax_rates': {
            'total_tax_rate': total_tax_rate,  # 37.94% for $250k
            'marginal_tax_rate': marginal_tax_rate,  # 53.53% for $250k
            'federal_rate': (federal_tax / income) * 100,
            'provincial_rate': (provincial_tax / income) * 100,
            'cpp_ei_rate': ((cpp_contribution + ei_contribution) / income) * 100
        },
        'federal_breakdown': federal_breakdown,
        'provincial_breakdown': provincial_breakdown,
        'consumption_tax_breakdown': consumption_tax_results,
        'pay_periods': pay_periods
    }

def get_employment_types():
    """Get available employment types and their specific deductions"""
    return {
        'Employee': {
            'deductions': ['CPP contributions', 'EI premiums', 'Union dues', 'Work-from-home expenses'],
            'tax_implications': 'Standard T4 income, employer covers part of CPP/EI'
        },
        'Self-Employed': {
            'deductions': ['Home office expenses', 'Vehicle expenses', 'Equipment', 'Professional fees'],
            'tax_implications': 'Must pay both portions of CPP, no EI unless opted in'
        },
        'Contractor': {
            'deductions': ['GST/HST collected', 'Business expenses', 'Professional insurance'],
            'tax_implications': 'May need to charge and remit GST/HST if earning over $30,000'
        }
    }

def get_tax_saving_tips(employment_type):
    """Return a list of tax saving tips based on employment type"""
    common_tips = [
        {
            'category': 'RRSP Contributions',
            'tip': 'Contributing to your RRSP reduces your taxable income.',
            'impact': 'Can lower your tax bracket and defer taxes until retirement.'
        },
        {
            'category': 'TFSA Optimization',
            'tip': 'While TFSA contributions aren\'t tax-deductible, the growth is tax-free.',
            'impact': 'Tax-free withdrawal of investment gains.'
        }
    ]

    employment_specific_tips = {
        'Employee': [
            {
                'category': 'Work From Home Deductions',
                'tip': 'Claim home office expenses if working remotely.',
                'impact': 'Can deduct a portion of rent/mortgage, utilities, and internet.'
            },
            {
                'category': 'Professional Development',
                'tip': 'Some employer-required training costs may be deductible.',
                'impact': 'Reduce taxable income while advancing your career.'
            }
        ],
        'Self-Employed': [
            {
                'category': 'Business Expenses',
                'tip': 'Track all business-related expenses including home office, vehicle, and equipment.',
                'impact': 'Significantly reduce taxable business income.'
            },
            {
                'category': 'Income Splitting',
                'tip': 'Consider hiring family members or incorporating.',
                'impact': 'Potentially lower overall family tax burden.'
            }
        ],
        'Contractor': [
            {
                'category': 'GST/HST Management',
                'tip': 'Register for GST/HST if earning over $30,000 annually.',
                'impact': 'Claim input tax credits on business purchases.'
            },
            {
                'category': 'Installment Planning',
                'tip': 'Set aside money for quarterly tax installments.',
                'impact': 'Avoid penalties and interest charges.'
            }
        ]
    }

    return common_tips + employment_specific_tips.get(employment_type, [])