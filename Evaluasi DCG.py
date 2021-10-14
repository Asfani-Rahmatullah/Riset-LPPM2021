def DCG(indek_topN, Tes, N): 
    DCG_user = [] 
    rata2_top_DCG = [] 
    for top in range(N): 
        user_dcg = 0 
        DCG = [] 
        for user in range(len(Tes)): 
            if(len(Tes[user])>0): 
                hitung_dcg = [] 
                for indek_dcg in range(top+1): 
                    if(indek_topN[user][indek_dcg] in Tes[user]): 
                        hitung_dcg.append(1/math.log2(1+(indek_dcg+1)))
                    else: 
                        hitung_dcg.append(0) 
                DCG.append(sum(hitung_dcg)) 
                user_dcg = user_dcg+1 
        rata2_top_DCG.append(sum(DCG)/len(DCG)) 
        DCG_user.append(DCG) 
    return DCG_user, rata2_top_DCG