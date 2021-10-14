def Main_UBCF(FoldKe, Lokasi_Output, topK, jenis, normalisasi): 
    FoldKe = str(Fold+1) 
    List_Kriteria = ["MatrikOverall_"+FoldKe, "MatrikUseful_"+FoldKe, "MatrikFunny_"+FoldKe, "MatrikCool_"+FoldKe] 
    List_Simpan = ["MatrikOverall", "MatrikUseful", "MatrikFunny", "MatrikCool"] 

    MatrikOverall = joblib.load(Lokasi_Output+List_Kriteria[0]+".sav") 
    MatrikUseful = joblib.load(Lokasi_Output+List_Kriteria[1]+".sav") 
    MatrikFunny = joblib.load(Lokasi_Output+List_Kriteria[2]+".sav") 
    MatrikCool = joblib.load(Lokasi_Output+List_Kriteria[3]+".sav") 
    
    MatrikOverall_MinMax = joblib.load(Lokasi_Output+'MatrikOverall(MinMax).sav') 
    MatrikUseful_MinMax = joblib.load(Lokasi_Output+'MatrikUseful(MinMax).sav') 
    MatrikFunny_MinMax = joblib.load(Lokasi_Output+'MatrikFunny(MinMax).sav') 
    MatrikCool_MinMax = joblib.load(Lokasi_Output+'MatrikCool(MinMax).sav')
    Rata2_DataAsli = [] 
    Rata2_MinMax = [] 

    print("Rata2 Data Asli") 
    Rata2_DataAsli.append(UB_rata2MatrikUser(MatrikOverall, MatrikOverall))
    Rata2_DataAsli.append(UB_rata2MatrikUser(MatrikOverall, MatrikUseful))
    Rata2_DataAsli.append(UB_rata2MatrikUser(MatrikOverall, MatrikFunny)) 
    Rata2_DataAsli.append(UB_rata2MatrikUser(MatrikOverall, MatrikCool))

    print("Rata2 Data Normalisasi") 
    Rata2_MinMax.append(UB_rata2MatrikUser(MatrikOverall, MatrikOverall_MinMax)) 
    Rata2_MinMax.append(UB_rata2MatrikUser(MatrikOverall, MatrikUseful_MinMax)) 
    Rata2_MinMax.append(UB_rata2MatrikUser(MatrikOverall, MatrikFunny_MinMax)) 
    Rata2_MinMax.append(UB_rata2MatrikUser(MatrikOverall, MatrikCool_MinMax)) 
    
##### PERHITUNGAN SIMILARITAS USER ######
    print("Similaritas") 
    Similaritas = [] 
    Similaritas.append(UB_uSim(MatrikOverall, MatrikOverall_MinMax, Rata2_MinMax[0])) 
    Similaritas.append(UB_uSim(MatrikOverall, MatrikUseful_MinMax, Rata2_MinMax[1])) 
    Similaritas.append(UB_uSim(MatrikOverall, MatrikFunny_MinMax, Rata2_MinMax[2])) 
    Similaritas.append(UB_uSim(MatrikOverall, MatrikCool_MinMax, Rata2_MinMax[3])) 
    joblib.dump(Similaritas, Lokasi_Output+"Similaritas_UserMinMax"+FoldKe+".sav") 
    
##### MENCARI NILAI AVERAGE ######
    Nilai_Sim_Avg = UB_TopK(Similaritas[0], Similaritas[1], Similaritas[2],Similaritas[3]) 
    Array_Sim = np.array(Nilai_Sim_Avg) 
    index_Sim = np.argsort(-Array_Sim) 
    File_Simpan = ['UBCF(Avg)_Predik_Overall.sav', 'UBCF(Avg)_Predik_Useful.sav', 'UBCF(Avg)_Predik_Funny.sav', 'UBCF(Avg)_Predik_Cool.sav'] 
    Kriteria = ['MatrikOverall', 'MatrikUseful', 'MatrikFunny', 'MatrikCool'] 

##### PREDIKSI RATING USER ######
    for i in range(4): 
        MatrikOverall = joblib.load('MatrikOverall.sav') 
        MatrikKriteria = joblib.load(Kriteria[i]+'.sav') 
        Prediksi = UB_prediksiUser(MatrikOverall, MatrikKriteria, Rata2_DataAsli[i], Similaritas[i], index_Sim, topK) 
        #print("\nPrediksi User "+Kriteria[i]+"\n", Prediksi) 
        joblib.dump(Prediksi, Lokasi_Output+File_Simpan[i])