def sqrt(n): 

    # We are using n itself as 
    # initial approximation This 
    # can definitely be improved  
        x = n 
        y = 1
          
        # e decides the accuracy level 
        e = 0.000001
        while(x - y > e): 
      
            x = (x + y)/2
            y = n / x 
      
        return x 
