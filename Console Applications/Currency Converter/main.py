def main():
    print("This program converts US dollars to New Taiwan dollars")
    print()

    dollars = eval(input("Enter amount in US dollars: "))

    twd = convert_to_TWD(dollars)

    print("This is", f"${twd}", "TWD.")

convert_to_TWD = lambda dollars: dollars * 31.04

main()