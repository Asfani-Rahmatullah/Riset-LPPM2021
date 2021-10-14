def Normalisasi_MinMax(Fold, Lokasi_Output, MinBaru, MaxBaru): 
    FoldKe = str(Fold+1) 
    List_Kriteria = ["MatrikOverall_"+FoldKe, "MatrikUseful_"+FoldKe, "MatrikFunny_"+FoldKe, "MatrikCool_"+FoldKe] 
    List_Simpan = ["MatrikOverall", "MatrikUseful", "MatrikFunny", "MatrikCool"] 

    MatrikOverall = joblib.load(Lokasi_Output+List_Kriteria[0]+".sav") 
    MatrikUseful = joblib.load(Lokasi_Output+List_Kriteria[1]+".sav") 
    MatrikFunny = joblib.load(Lokasi_Output+List_Kriteria[2]+".sav") 
    MatrikCool = joblib.load(Lokasi_Output+List_Kriteria[3]+".sav") 
    
    Jumlah_User = len(MatrikOverall) 
    Jumlah_Item = len(MatrikOverall[0]) 
    print("Jumlah_User", Jumlah_User) 
    print("Jumlah_Item", Jumlah_Item) 
    
    for i in range(4): 
        MatrikBaru = np.zeros((Jumlah_User, Jumlah_Item)) 

        MatrikKriteria=joblib.load(Lokasi_Output+List_Kriteria[i]+".sav") 
        awal = time.time() 
        for user in range(len(MatrikOverall)): 
            awal1 = time.time() 
            TampungData = [] 
            for item in range(len(MatrikOverall[user])): 
                if(MatrikOverall[user][item] != 0): 
                    TampungData.append(MatrikOverall[user][item]) 
                    TampungData.append(MatrikUseful[user][item]) 
                    TampungData.append(MatrikFunny[user][item]) 
                    TampungData.append(MatrikCool[user][item]) 
            
            MinRating = min(TampungData) 
            MaxRating = max(TampungData) 
            
            for indeks_normalisasi in range(len(MatrikOverall[user])): 
                if(MatrikOverall[user][indeks_normalisasi] != 0): 
                    rating_normalisasi = (((MatrikKriteria[user][indeks_normalisasi]-MinRating)/(MaxRating-MinRating))*(MaxBaru-MinBaru))+MinBaru 
                    MatrikBaru[user][indeks_normalisasi] = rating_normalisasi 
            joblib.dump(MatrikBaru, Lokasi_Output+List_Simpan[i]+'(MinMax).sav') 
            akhir1 = time.time() 
            print("Waktu PerUser", akhir1-awal1)
        akhir = time.time() 
        print("waktu", akhir-awal)