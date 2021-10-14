def Excel2Matriks(Fold, Lokasi_Excel, Lokasi_Output): 
    FoldKe = str(Fold+1) 
    List_Kriteria = ["Overall", "useful", "funny", "cool"] 
    List_Simpan = ['MatrikOverall_'+FoldKe+'.sav', 'MatrikUseful_'+FoldKe+'.sav', 'MatrikFunny_'+FoldKe+'.sav', 'MatrikCool_'+FoldKe+'.sav'] 
    df1 = pd.read_excel(Lokasi_Excel+"Training"+FoldKe+".xlsx", names=["","User_id", "Item_id", "Overall", "useful", "funny", "cool"]) 
    user_max = df1["User_id"].max() 
    item_max = df1["Item_id"].max() 
    for i in range(4): 
        matrik_data = np.zeros((user_max, item_max)) 
        kriteria = List_Kriteria[i] 
        for li in range(len(df1)): 
            user = df1["User_id"][li] 
            item = df1["Item_id"][li] 
            rating = df1[kriteria][li] 
            matrik_data[user-1,item-1] = rating 
        joblib.dump(matrik_data, Lokasi_Output+List_Simpan[i])