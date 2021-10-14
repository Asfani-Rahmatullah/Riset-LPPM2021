def TopN(MatrikRating, MatrikIndek): 
    matrik_rating_TopN = [] 
    matrik_indek_TopN = [] 
    for user in range(len(MatrikRating)): 
        rating_top = np.array(MatrikRating[user]) 
        
        sort_top = np.argsort(-rating_top) 
        data_rating = rating_top[sort_top[::]] 
        
        #mengurutkan indek rating 
        indek_top = np.array(MatrikIndek[user]) 
        data_indek = indek_top[sort_top[::]] 
        
        matrik_rating_TopN.append(np.array(data_rating).tolist())
        
        matrik_indek_TopN.append(np.array(data_indek).tolist()) 
    return matrik_rating_TopN, matrik_indek_TopN