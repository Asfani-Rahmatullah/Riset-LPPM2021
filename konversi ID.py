df1 = pd.read_excel("Output 25k/FilterDataset25k.xlsx", names=["", "User_id", "Item_id", "Overall", "useful", "funny", "cool"])

Item_id = [], User_id = [] 
DataUser = [], DataItem = [], DataOverall = [], DataUseful = [], DataFunny = [], DataCool = [] 

for li in range(len(df1)): 
    vUser_id = df1["User_id"][li] 
    vItem_id = df1["Item_id"][li] 
    vOverall = df1["Overall"][li] 
    vUseful = df1["useful"][li] 
    vFunny = df1["funny"][li] 
    vCool = df1["cool"][li] 
    
    if (vUser_id in User_id): 
        index_user = User_id.index(vUser_id) 
    else: 
        User_id.append(vUser_id) 
        index_user = User_id.index(vUser_id) 
    
    if (vItem_id in Item_id): 
        index_item = Item_id.index(vItem_id) 
    else: 
        Item_id.append(vItem_id) 
        index_item = Item_id.index(vItem_id) 
    
    DataUser.append(index_user+1) 
    
    DataItem.append(index_item+1) 
    DataOverall.append(vOverall) 
    DataUseful.append(vUseful) 
    DataFunny.append(vFunny) 
    DataCool.append(vCool) 
df = pd.DataFrame({'User_id':DataUser, 'Item_id':DataItem, 'Overall':DataOverall, 'useful':DataUseful, 'funny':DataFunny, 'cool':DataCool}) 
writer = pd.ExcelWriter("Output 25k/Dataset25k(id).xlsx", engine='xlsxwriter') 
df.to_excel(writer, sheet_name='Sheet1') 
workbook = writer.book 
worksheet = writer.sheets['Sheet1'] 
writer.save()