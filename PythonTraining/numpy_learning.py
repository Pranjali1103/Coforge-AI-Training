#step1-Import NumPy
import numpy as np

#step2-Create Salary Array
salary=np.array([65000,58000,72000,80000,85000,68000,90000,76000])
print("=====================Salary=======================")
print(salary)

#step3-Check NumPy Array Properties
print("========================Salary Operations============================")
print("Array:",salary)
print("Type:",type(salary))
print("Dimensions:",salary.ndim)
print("Shape",salary.shape)
print("Size:",salary.size)
print("Datatype:",salary.dtype)
# salary=np.array([[65000,58000,72000,80000,85000,68000,90000,76000]])
print("Dimensions:",salary.ndim)

rating=np.array([4.5,4.2,4.8,4.6,4.1,4.7,4.9,4.3])
print("=====================Ratings====================")
print(rating)

#check properties
print("Rating Shape",rating.shape)
print("Rating Size:",rating.size)
print("Rating Datatype:",rating.dtype)

#NumPy Indexing
print("=======================NumPy Indexing============================")
print("First Salary:",salary[0])
print("Third Salary:",salary[2])
print("Last Salary:",salary[-1])
print("Second Last Salary:",salary[-2])
print("Third Last Salary:",salary[-3])
print(type(salary))

#NumPy Slicing

# salary=np.array([65000,58000,72000,80000,85000,68000,90000,76000])

#first three
print(salary[0:3])

#last three
print(salary[-3:])

#all except first 2
print(salary[2:])

#find employees earning above 75000
#business:identify employees on a higher salary bracket

high_salary=salary[salary>75000]
print("Employees Salary:",high_salary)
print("Employees Count:",len(high_salary))

# find employees with Rating above 4.5
print("===================High Performing Employees======================")
high_rating=rating[rating>4.5]
print(high_rating)
print("No of Employees:",len(high_rating))

#Conditional Salary Increment
new_salary=np.where(salary<7000,salary*1.10,salary*1.05)
print("Original Salary:",salary)
print("Updated Salary:",new_salary)

print("Performance Bonus")
bonus = np.where(rating>=4.5, salary*0.15, salary*0.05)
print(bonus) 