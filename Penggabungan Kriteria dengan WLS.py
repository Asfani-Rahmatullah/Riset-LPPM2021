def WLS(Matrik, Overall, Useful, Funny, Cool): 
    Hasil_WLS = ((np.multiply(0.2, Overall))+(np.multiply(0.2, Useful))+(np.multiply(0.4, Funny))+(np.multiply(0.2, Cool))) 
    matrik_rating_WLS = [] 
    matrik_indek_WLS = [] 
    for user in range(len(Overall)): 
        tampung_rating = [] 
        tampung_indek = [] 
        for item in range(len(Overall[0])): 
            if(Matrik[user][item] == 0): 
                tampung_rating.append(Hasil_WLS[user][item]) 
                tampung_indek.append(item) 
        
        matrik_rating_WLS.append(tampung_rating) 
        matrik_indek_WLS.append(tampung_indek) 
    
    return matrik_rating_WLS, matrik_indek_WLS