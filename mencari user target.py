import os
import sys
import joblib
import pandas as pd
import numpy as np
from werkzeug.datastructures import IfRange
import xlrd
import math

class Main2():
    def __init__(self):
        Data_Excel = self.load_excel("Dataset1/Evaluasi Gabungan.xlsx")
        self.Hasil_Eval = Data_Excel
        self.DataKe = 1

    def load_excel(self, file):
        Full_Data_Excel = []
        book = xlrd.open_workbook(file)

        for id_sheet in range(6):
            Data_Excel = []
            for i in range(11): #perulangan sebanyak menu
                Data_Excel.append([])
                
            first_sheet = book.sheet_by_index(id_sheet)
            for i in range(100): #perulangan  untuk mengambil data dari excel, sebanyak jumlah topN yaitu 100
                
                cells = first_sheet.row_slice(rowx=i+1, start_colx=0, end_colx=12) #membaca data perbaris
                index = 0
                for cell in cells: #perulangan untuk mengambil data perkolom
                    Data_Excel[index].append(str(cell.value))
                    index += 1
            Full_Data_Excel.append(Data_Excel)
        return Full_Data_Excel
    def load_Detail(self, Menu):
        DataRekom_Usulan = []
        DataTest = []
        
        DataRekom_Usulan.append(joblib.load("Dataset1/TopN_M"+str(Menu)+"_3.sav"))
        DataTest.append(joblib.load("Dataset1/Testing3.sav"))
        NamaItem = joblib.load("Dataset1/NamaItem.sav")
        
        return DataRekom_Usulan, DataTest, NamaItem


class Main3():
    def __init__(self, DataRekom, DataTest, NamaItem, DataKe, TargetUser, TopN):
        self.DataRekom = DataRekom
        self.DataTest = DataTest
        self.NamaItem = NamaItem
        self.DataKe = DataKe
        self.Target_User = TargetUser
        self.TopNu = TopN
        self.TopN = []
        self.User = []
        for i in range(100): #perulangan untuk membuat topn
            self.TopN.append(i+1) #menyimpan nilai TopN
        for i in range(len(self.DataTest[0])): #perulangan target user berdasarkan data tes
            if(len(self.DataTest[0][i]) > 0): #kondisi pengecekan apakah data tes lebih besar dari 0, atau user tersebut sudah pernah memberi rating
                self.User.append(str(i+1))
        self.Fold = 1 #mengubah nilai fold combobox dengan memanggil fungsi show_user, dimana perubahan fold tersebut digunakan untuk menampilkan target user
    
    def data_userTopN(self):
        return self.User, self.TopN

    def Proses(self):
        
        #Ambil Nilai
        Fold = 1-1
        Target_User = int(self.Target_User)-1
        TopN = int(self.TopNu)
        Hasil_rekom = []
        Hasil_test = []
        Hasil_pelatihan = []
        Hasil_irisan = []

        if(self.DataKe == 1):
            Full_Item = [i for i in range(5209)]
        elif(self.DataKe == 2):
            Full_Item = [i for i in range(131)]
            
        Rekom_Eval = []
        Test_Eval = []
        
        
        for i in range(TopN):
            NamaHotel = int(self.DataRekom[Fold][Target_User][i])
            Hasil_rekom.append(self.NamaItem[2][NamaHotel] + "(ID: " + str(NamaHotel+1)+ ")") #Ubah disini
            Rekom_Eval.append(self.DataRekom[Fold][Target_User][i]) #untuk perhitungan evaluasi
        
        for i in range(len(self.DataTest[Fold][Target_User])):
            NamaHotel = int(self.DataTest[Fold][Target_User][i])
            Hasil_test.append(self.NamaItem[2][NamaHotel] + "(ID: " + str(NamaHotel+1)+ ")")
            Test_Eval.append(self.DataTest[Fold][Target_User][i])
        
        data_pelatihan = np.setdiff1d(Full_Item, self.DataRekom[Fold][Target_User])
        for i in range(len(data_pelatihan)):
            NamaHotel = data_pelatihan[i]
            Hasil_pelatihan.append(self.NamaItem[2][NamaHotel]+ "(ID: " + str(NamaHotel+1)+ ")")
        
        Jumlah_Irisan = 0
        for i in range(TopN):
            if(Rekom_Eval[i] in Test_Eval):
                NamaHotel = int(Rekom_Eval[i])
                Hasil_irisan.append(self.NamaItem[2][NamaHotel] + "(ID: " + str(NamaHotel+1)+ ")")
                Jumlah_Irisan = Jumlah_Irisan+1

        

        nilai_Precision = self.Precision(Rekom_Eval, Test_Eval, TopN)
       
        nilai_Recall = self.Recall(Rekom_Eval, Test_Eval, TopN)
      
        nilai_F1Score = self.F1Score(Rekom_Eval, Test_Eval, TopN)
        
        nilai_AP = self.AP(Rekom_Eval, Test_Eval, TopN)
        
        nilai_DCG = self.DCG(Rekom_Eval, Test_Eval, TopN)
       
        nilai_NDCG = self.NDCG(Rekom_Eval, Test_Eval, TopN)
        

        return Hasil_irisan, Hasil_pelatihan, Hasil_rekom, Hasil_test, nilai_AP, nilai_DCG, nilai_F1Score, nilai_NDCG, nilai_Recall, nilai_Precision

    def Precision(self, indek_topN, Tes, N):
        temp = 0
        precisionFull = []
        for top in range(N):
            if(indek_topN[top] in Tes):
                temp = temp + 1
            hitung_precision = temp/(top+1)
            precisionFull.append(hitung_precision)
        return precisionFull

    def Recall(self, indek_topN, Tes, N):
        temp = 0
        recallFull = []
        for top in range(N):
            if(indek_topN[top] in Tes):
                temp = temp + 1
            if (len(Tes)== 0):
                hitung_recall = 0
            else:
                hitung_recall = temp/(len(Tes))
            recallFull.append(hitung_recall)
        return recallFull

    def F1Score(self, indek_topN, Tes, N):
        precision = self.Precision(indek_topN, Tes, N)
        recall = self.Recall(indek_topN, Tes, N)
        pembilang = (2*precision[N-1]*recall[N-1])
        penyebut = (precision[N-1]+recall[N-1])
        if(pembilang == 0 or penyebut == 0):
            f1score = 0.0
        else :
            f1score = pembilang/penyebut
        return f1score

    def AP(self, indek_topN, Tes, N):
        precision = self.Precision(indek_topN, Tes, N)
        hitung_ap = []
        for i in range(N):
            if(indek_topN[i] in Tes):
                hitung_ap.append(precision[i])
            else:
                hitung_ap.append(0.0)
        if (len(Tes) == 0):
            nilai_AP_Top = 0
        else:
            nilai_AP_Top = sum(hitung_ap)/len(Tes)
        return nilai_AP_Top

    def DCG(self, indek_topN, Tes, N):
        DCG_user = []
        DCGFull = []
        for top in range(N):
            if(indek_topN[top] in Tes):
                DCG_user.append(1/math.log2(1+(top+1)))
            else:
                DCG_user.append(0.0)
            DCGFull.append(sum(DCG_user))
        return DCGFull

    def IDCG(self, N):
        IDCG = []
        for top in range(N):
            IDCG.append(1/math.log2(1+(top+1)))
        return sum(IDCG)

    def NDCG(self, indek_topN, Tes, N):
        dcg = self.DCG(indek_topN, Tes, N)
        idcg = self.IDCG(N)
        NDCG = dcg[N-1]/idcg
        return NDCG

main2 = Main2()
Detail_Data_Training, Detail_Data_Test, NamaItem = main2.load_Detail(11)
for i in range(2954):        
    main3 = Main3(Detail_Data_Training, Detail_Data_Test, NamaItem, 1, i+1, 20)
    Hasil_irisan, Hasil_pelatihan, Hasil_rekom, Hasil_test, nilai_AP, nilai_DCG, nilai_F1Score, nilai_NDCG, nilai_Recall, nilai_Precision = main3.Proses()
    jml_irisan = len(Hasil_irisan)
    if jml_irisan !=0:
        print ("User " + str((i+1)))
