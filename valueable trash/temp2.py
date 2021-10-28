import os
import sys
import joblib
import pandas as pd
import numpy as np
import xlrd
import math

Cek = joblib.load("Dataset1/Testing1.sav")
User = []
for i in range(len(Cek[0])): #perulangan untuk menampilkan datates berdasarkan fold yang dipilih
    print (Cek[0][i])
    if(len(Cek[0][i]) > 0):
        User.append(str(i+1))
