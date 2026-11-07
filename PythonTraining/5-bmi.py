weight=float(input("Enter the weight:"))
height=float(input("Enter the height:"))
bmi=weight/(height**2)
if(bmi==30):
    print("Obese")
elif(bmi>=25 and bmi<30):
    print("Overweight")
elif(bmi>=18.5 and bmi<25):
    print("Normal")
else:
    print("Underweight")