def IDCG(N): 
    IDCG = [] 
    for top in range(N): 
        hitung_idcg = [] 
        for indek_idcg in range(top+1): 
            hitung_idcg.append(1/math.log2(1+(indek_idcg+1)))
        IDCG.append(sum(hitung_idcg)) 
    return IDCG 