for i in range(1,10):
    if(i==2 or i==4):
        break
    else:
        print(i)

for i in range(1,10):
    if(i==2 or i==4):
       continue
else:
    print(i)

print("---Employee ID Processing System------")
for i in range(1,51):
    if(i==37):
        break
    elif(i%5==0):
        continue
    elif(i>20):
        print(i)