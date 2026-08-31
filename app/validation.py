# Missing name
if data.name is None:
    missing_information.append("name")

# Missing address
if data.address is None:
    missing_information.append("address")

# Invalid income
if data.monthly_income is not None and data.monthly_income < 0:
    invalid_information.append("monthly_income")

# Invalid unemployment duration
if data.months_unemployed is not None and data.months_unemployed < 0:
    invalid_information.append("months_unemployed")