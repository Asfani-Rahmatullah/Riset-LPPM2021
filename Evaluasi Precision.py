def Precision(indek_topN, Tes, N): 
    tampung = np.zeros((len(Tes))) 
    precision = [] 
    precision_pertop = [] 
    for top in range(N): 
        hitung_precision = 0 
        precision_peruser = [] 
        for user in range(len(Tes)): 
            if(indek_topN[user][top] in Tes[user]): 
                tampung[user] = tampung[user] + 1 
            if(len(Tes[user]) > 0): 
                hitung_precision = tampung[user]/(top+1) 
                precision_peruser.append(hitung_precision) 
        precision.append(precision_peruser) 
        precision_pertop.append(sum(precision_peruser)/len(precision_peruser)) 
    return precision, precision_pertop