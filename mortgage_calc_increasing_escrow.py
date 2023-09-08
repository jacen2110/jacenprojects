import math

def calculate_daily_interest(principal, annual_interest_rate, days_in_year = 365):
    daily_interest_rate = ((1 + annual_interest_rate)**(1/days_in_year)) - 1
    return daily_interest_rate * principal

# Example usage
principal = float(input("Enter your initial loan amount: "))
annual_interest_rate = 6.375/100
total_biweekly_payment = float(input("Enter your total bi-weekly payment: ")) 

# Monthly escrow amount (part of bi-weekly payment but not deducted from loan)
monthly_escrow = float(input("Enter your monthly escrow payment: ")) 
bi_weekly_escrow = monthly_escrow / 2

# Ask for the annual escrow growth rate
escrow_growth_rate = float(input("Enter your annual escrow growth rate in percentage: ")) / 100

# Compute the portion of the bi-weekly payment that will be used to pay off the loan
bi_weekly_loan_payment = total_biweekly_payment - bi_weekly_escrow

# Assumption: Interest compounds every day
days_in_year = 365
payments_per_year = 26

payment_interval_days = math.ceil(days_in_year/payments_per_year)
day_count = 0
payment_count = 0
total_interest_added = 0

for year in range(1, 31):  # Assuming a 30 year mortgage
    for day in range(days_in_year):
        daily_interest = calculate_daily_interest(principal, annual_interest_rate)
        principal += daily_interest
        total_interest_added += daily_interest
        day_count += 1

        # Deduct the payment from the loan amount every two weeks
        if day_count >= payment_interval_days or principal - bi_weekly_loan_payment <= 0:
            payment_made = min(bi_weekly_loan_payment, principal)
            principal -= payment_made
            print(f"\nAfter {payment_count + 1} bi-weekly payment(s) in year {year}:")
            print(f" - Interest added in the last two weeks: {total_interest_added}")
            print(f" - The payment made towards the loan: {payment_made}")
            print(f" - The remaining loan balance is: {principal if principal > 0 else 0}")
            day_count = 0
            total_interest_added = 0
            payment_count += 1
        if principal <= 0:
            break

    # Adjust the escrow payment and the loan payment based on the growth rate at the end of each year
    monthly_escrow *= (1 + escrow_growth_rate)
    bi_weekly_escrow = monthly_escrow / 2
    bi_weekly_loan_payment = total_biweekly_payment - bi_weekly_escrow
    if principal <= 0:
        break

years = payment_count / 26

print(f"\nThe loan is fully paid after {payment_count} bi-weekly payment and that is {years} years.")
