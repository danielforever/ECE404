
val = int(input("")) 
flag=0
if val<51 and 0<val:
    if val == 1:
        print ("ring")
    elif val == 2:
        print ("field")
    else:
        for i in range(2, val):
            if val % i ==0:
                print("ring")
                flag=1
                break
        if flag==0:
            print("field")
            

                
        
    
