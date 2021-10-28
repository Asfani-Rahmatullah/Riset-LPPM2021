import os
import sys
import joblib
import pandas as pd
import numpy as np
import xlrd
import math
from flask import Flask, render_template
app = Flask(__name__)

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
                print("i", i)
                cells = first_sheet.row_slice(rowx=i+1, start_colx=0, end_colx=12) #membaca data perbaris
                index = 0
                for cell in cells: #perulangan untuk mengambil data perkolom
                    Data_Excel[index].append(str(cell.value))
                    index += 1
            Full_Data_Excel.append(Data_Excel)
        return Full_Data_Excel
    def load_Detail(self, DataKe):
        DataRekom_Usulan = []
        DataTest = []
        print("Proses Memuat Data Rekomendasi dan Testing")
        DataRekom_Usulan.append(joblib.load("Dataset1/TopN_M10_1.sav"))
        DataTest.append(joblib.load("Dataset1/Testing1.sav"))

        if(DataKe == 1):
            NamaItem = joblib.load("Dataset1/NamaItem.sav")
        elif(DataKe == 2):
            NamaItem = [[], [], []]
            NamaItem[2] = ["Restoran ID-"+str(i+1) for i in range(131)]

        return DataRekom_Usulan, DataTest, NamaItem


class Main3():
    def __init__(self, DataRekom, DataTest, NamaItem, DataKe):
        self.DataRekom = DataRekom
        self.DataTest = DataTest
        self.NamaItem = NamaItem
        self.DataKe = DataKe
        self.TopN = []
        self.User = []
        for i in range(100): #perulangan untuk membuat topn
            self.TopN.append(i) #menyimpan nilai TopN
        for i in range(len(self.DataTest[0])): #perulangan target user berdasarkan data tes
            if(len(self.DataTest[0][i]) > 0): #kondisi pengecekan apakah data tes lebih besar dari 0, atau user tersebut sudah pernah memberi rating
                self.User.append(str(i+1))
        self.Fold = 1 #mengubah nilai fold combobox dengan memanggil fungsi show_user, dimana perubahan fold tersebut digunakan untuk menampilkan target user

    def _Show_User(self, text):
        index_fold = int(text)-1
        X = []
        self.ui.cb_user1.clear()
        for i in range(len(self.DataTest[index_fold])): #perulangan untuk menampilkan datates berdasarkan fold yang dipilih
            if(len(self.DataTest[index_fold][i]) > 0):
                X.append(i+1)
                self.ui.cb_user1.addItem(str(i+1))
        print ("ini yang di test")
        print (X)

    def _Tombol_Rekom(self):
        print("Rekomendasi")
        Fold = int(self.ui.cb_fold1.currentText())-1
        Target_User = int(self.ui.cb_user1.currentText())-1
        TopN = int(self.ui.cb_topn1.currentText())

        if(self.DataKe == 1):
            Full_Item = [i for i in range(5209)]
        elif(self.DataKe == 2):
            Full_Item = [i for i in range(131)]
            
        Rekom_Eval = []
        Test_Eval = []
        
        print("lw_rekom")
        self.ui.lw_rekom.clear()
        for i in range(TopN):
            NamaHotel = int(self.DataRekom[Fold][Target_User][i])
            self.ui.lw_rekom.addItem(str(NamaHotel+1)+". "+self.NamaItem[2][NamaHotel])
            Rekom_Eval.append(self.DataRekom[Fold][Target_User][i]) #untuk perhitungan evaluasi
        print("lw_test")
        self.ui.lw_test.clear()
        for i in range(len(self.DataTest[Fold][Target_User])):
            NamaHotel = int(self.DataTest[Fold][Target_User][i])
            self.ui.lw_test.addItem(str(NamaHotel+1)+". "+self.NamaItem[2][NamaHotel])
            Test_Eval.append(self.DataTest[Fold][Target_User][i])
        print("lw_pelatihan")
        self.ui.lw_training.clear()
        data_pelatihan = np.setdiff1d(Full_Item, self.DataRekom[Fold][Target_User])
        for i in range(len(data_pelatihan)):
            NamaHotel = data_pelatihan[i]
            self.ui.lw_training.addItem(str(NamaHotel+1)+". "+self.NamaItem[2][NamaHotel])
        print("lw_irisan")
        self.ui.lw_irisan.clear()
        Jumlah_Irisan = 0
        for i in range(TopN):
            if(Rekom_Eval[i] in Test_Eval):
                NamaHotel = int(Rekom_Eval[i])
                self.ui.lw_irisan.addItem(str(NamaHotel+1)+". "+self.NamaItem[2][NamaHotel])
                Jumlah_Irisan = Jumlah_Irisan+1

        print("sukses")

        nilai_Precision = self.Precision(Rekom_Eval, Test_Eval, TopN)
        print("nilai_Precision", nilai_Precision)
        nilai_Recall = self.Recall(Rekom_Eval, Test_Eval, TopN)
        print("nilai_Recall", nilai_Recall)
        nilai_F1Score = self.F1Score(Rekom_Eval, Test_Eval, TopN)
        print("nilai_F1Score", nilai_F1Score)
        nilai_AP = self.AP(Rekom_Eval, Test_Eval, TopN)
        print("nilai_AP", nilai_AP)
        nilai_DCG = self.DCG(Rekom_Eval, Test_Eval, TopN)
        print("nilai_DCG", nilai_DCG)
        nilai_NDCG = self.NDCG(Rekom_Eval, Test_Eval, TopN)
        print("nilai_NDCG", nilai_NDCG)

        self.ui.label_rekom.setText("Rekomendasi ("+str(len(Rekom_Eval))+" Item)")
        self.ui.label_test.setText("Data Test ("+str(len(Test_Eval))+" Item)")
        self.ui.label_training.setText("Data Training ("+str(len(data_pelatihan))+" Item)")
        self.ui.label_irisan.setText("Irisan Rekom & Test("+str(Jumlah_Irisan)+" Item)")

        self.ui.l_pre3.setText(str(nilai_Precision[TopN-1])[:7])
        self.ui.l_rec3.setText(str(nilai_Recall[TopN-1])[:7])
        self.ui.l_f1s3.setText(str(nilai_F1Score)[:7])
        self.ui.l_ap3.setText(str(nilai_AP)[:7])
        self.ui.l_dcg3.setText(str(nilai_DCG[TopN-1])[:7])
        self.ui.l_ndcg3.setText(str(nilai_NDCG)[:7])
        #self.ui.label_hasil1.setText("Hasil : Fold "+str(Fold+1)+", User "+str(Target_User+1)+", TopN "+str(TopN))

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
Detail_Data_Training, Detail_Data_Test, NamaItem = main2.load_Detail(1)
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    gui = Main3(Detail_Data_Training, Detail_Data_Test, NamaItem, 1)
    sys.exit(app.exec_())
