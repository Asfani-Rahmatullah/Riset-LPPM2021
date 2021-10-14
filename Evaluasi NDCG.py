def NDCG(dcg, idcg, N): 
    NDCG = [] 
    for top in range(N): 
        hitung_ndcg = [] 
        for user in range(len(dcg[top])): 
            hitung_ndcg.append(dcg[top][user]/idcg[top]) 
        
        NDCG.append(sum(hitung_ndcg)/len(hitung_ndcg)) 
    return NDCG 