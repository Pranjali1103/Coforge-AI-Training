salary=int(input("Enter the salary:"))
if salary>=50000:
    print("20% bonus=",0.2*salary)
elif salary>=30000 and salary<50000:
    print("10% bonus=",0.1*salary)
else:
    print("5% bonus",0.05*salary)
    