"""
This is the main file. Run this script.
"""

import pandas as pd
from scrape import scrape_tool

data = pd.read_csv('urls.csv')
rows = data['urls']
individuals = [row for row in rows if 'https://www.ato.gov.au/Individuals' in row]
super_ = [row for row in rows if 'https://www.ato.gov.au/Super' in row]
business = [row for row in rows if 'https://www.ato.gov.au/Business' in row]
tax_professionals = [row for row in rows if 'https://www.ato.gov.au/Tax-professionals' in row]
general = [row for row in rows if 'https://www.ato.gov.au/General' in row]
rates = [row for row in rows if 'https://www.ato.gov.au/Rates' in row]
non_profit = [row for row in rows if 'https://www.ato.gov.au/Non-profit' in row]

print(f"There are {len(individuals)} items in Individuals list")
print(f"There are {len(super_)} items in super list")
print(f"There are {len(business)} items in business list")
print(f"There are {len(tax_professionals)} items in tax_professionals list")
print(f"There are {len(general)} items in general list")
print(f"There are {len(rates)} items in rates list")
print(f"There are {len(non_profit)} items in non_profit list")

prompt = int(input("""
There are seven list of routes in the site. Choose one that you want to retrieve:
1. Individuals
2. Super
3. Business
4. Tax Professionals
5. General
6. Rates
7. Non-profit
(for example: if you want to choose Individuals then input 1)
input: 
"""))
start = int(input("""
Start index(index start from 1) = 
"""))
end = int(input("""
End index = 
"""))
if prompt == 1:
    scrape_tool(start=start, end=end, data=individuals, name="Individuals")
elif prompt == 2:
    scrape_tool(start=start, end=end, data=super_, name="Super")
elif prompt == 3:
    scrape_tool(start=start, end=end, data=business, name="Business")
elif prompt == 4:
    scrape_tool(start=start, end=end, data=tax_professionals, name="Tax professional")
elif prompt == 5:
    scrape_tool(start=start, end=end, data=general, name="General")
elif prompt == 6:
    scrape_tool(start=start, end=end, data=rates, name="Rates")
elif prompt == 7:
    scrape_tool(start=start, end=end, data=non_profit, name="Non-profit")
else:
    print("invalid input.")


