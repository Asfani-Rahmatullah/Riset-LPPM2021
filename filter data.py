#Code 4.1
import csv

Item_id = [], User_id = [], Overall = [], useful = [], funny = [], cool =[]

with open('yelp_review.csv', encoding="utf8") as file:
    reader = csv.reader(file) 
    count = 0 
    a=0 
    for row in reader: 
        if(a>0): 
            vUser_id = row[1] #user_id 
            vItem_id = row[2] #item_id 
            rating_all = row[3] #overall 
            c1 = row[6] #useful 
            c2 = row[7] #funny 
            c3 = row[8] #cool 
            User_id.append(vUser_id) 
            Item_id.append(vItem_id) 
            Overall.append(rating_all) 
            useful.append(c1) 
            funny.append(c2) 
            cool.append(c3) 
            if(a==74050): 
                break 
        else: 
            print(row) 
        a+=1 
##### FILTER DATA ###### 
f_user =[], f_item =[], f_overall =[], f_useful=[], f_funny =[], f_cool =[]
for li in range(len(User_id)): 
    if(li==0): 
        if(User_id[li+1]==User_id[li] and User_id[li+2]==User_id[li]): 
            f_user.append(User_id[li]) 
            f_item.append(Item_id[li]) 
            f_overall.append(Overall[li]) 
            f_useful.append(useful[li]) 
            f_funny.append(funny[li]) 
            f_cool.append(cool[li]) 
    elif(li==1): 
        if((User_id[li-1]==User_id[li] and User_id[li+1]==User_id[li]) or (User_id[li+1]==User_id[li] and User_id[li+2]==User_id[li])): 
            f_user.append(User_id[li]) 
            f_item.append(Item_id[li]) 
            f_overall.append(Overall[li]) 
            f_useful.append(useful[li]) 
            f_funny.append(funny[li]) 
            f_cool.append(cool[li]) 
    elif(len(User_id)-li==2): 
        if((User_id[li-1]==User_id[li] and User_id[li+1]==User_id[li]) or (User_id[li-1]==User_id[li] and User_id[li-2]==User_id[li])): 
            f_user.append(User_id[li]) 

            f_item.append(Item_id[li]) 
            f_overall.append(Overall[li]) 
            f_useful.append(useful[li]) 
            f_funny.append(funny[li]) 
            f_cool.append(cool[li]) 
    elif(len(User_id)-li==1): 
        if(User_id[li-2]==User_id[li] and User_id[li-1]==User_id[li]): 
            f_user.append(User_id[li]) 
            f_item.append(Item_id[li]) 
            f_overall.append(Overall[li]) 
            f_useful.append(useful[li]) 
            f_funny.append(funny[li]) 
            f_cool.append(cool[li]) 
    else: 
        if((User_id[li+1]==User_id[li] and User_id[li+2]==User_id[li]) or (User_id[li-1]==User_id[li] and User_id[li+1]==User_id[li]) or (User_id[li-2]==User_id[li] and User_id[li-1]==User_id[li])): 
            f_user.append(User_id[li]) 
            f_item.append(Item_id[li]) 
            f_overall.append(Overall[li]) 
            f_useful.append(useful[li]) 
            f_funny.append(funny[li]) 
            f_cool.append(cool[li]) 
df = pd.DataFrame({'User_id':f_user, 'Item_id':f_item, 'Overall':f_overall,'useful':f_useful, 'funny':f_funny, 'cool':f_cool}) 
writer = pd.ExcelWriter("Output 25k/FilterDataset25k.xlsx", engine='xlsxwriter') 
df.to_excel(writer, sheet_name='Sheet1') 
workbook = writer.book 
worksheet = writer.sheets['Sheet1'] 
worksheet.set_column('B:C', 28) 
writer.save()