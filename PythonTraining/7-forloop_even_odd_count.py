count_even=0
count_odd=0
sum_even=0
sum_odd=0
for i in range(1,50):
    if(i%2==0):
        sum_even+=i
        count_even+=1
        print("Even:",i)
    else:
        sum_odd+=i
        count_odd+=1
        print("Odd:",i)
sum_even_odd=sum_even+sum_odd
count_even_odd=count_even+count_odd
print("Even Sum",sum_even)
print("Even Count:",count_even)
print("Odd Sum:",sum_odd)
print("Odd Count:",count_odd)
print("Sum Even Odd:",sum_even_odd)
print("Even Odd Count:",count_even_odd)
avg=sum_even_odd/count_even_odd
print(avg)

    
        
        