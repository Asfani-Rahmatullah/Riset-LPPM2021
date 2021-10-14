def Penggabungan(Predik_UBCF, Predik_IBCF, w): 
    MatrikFusion = np.zeros((len(Predik_UBCF), len(Predik_IBCF[0]))) 
    for user in range(len(Predik_UBCF)): 
        for item in range(len(Predik_IBCF[0])): 
            Fusion = (w*Predik_UBCF[user][item])+((1-w)*Predik_IBCF[user][item]) 

            MatrikFusion[user][item] = Fusion 

    return MatrikFusion 