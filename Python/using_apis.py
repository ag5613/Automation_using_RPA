import pandas as pd
import os
import requests
import googlemaps
import pyperclip
import time

API_KEY = "AIzaSyC-XXXXXXXORau-X09hhebpRS8fkhuk"

def get_place_id(x):
    name = x.replace(" ","%20")
    url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={name}&inputtype=textquery&key={API_KEY}"
    response = requests.get(url)
    temp = response.json()
    if(len(temp['candidates'])>0):
        return temp['candidates'][0]['place_id']
    else:
        return " "
    
def get_data(place_id):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=address_component%2Cadr_address%2Cbusiness_status%2Cformatted_address%2Cgeometry%2Cicon%2Cicon_mask_base_uri%2Cicon_background_color%2Cname%2Cpermanently_closed%2Cphoto%2Cplace_id%2Cplus_code%2Ctype%2Curl%2Cutc_offset%2Cvicinity,formatted_phone_number%2Cinternational_phone_number%2Copening_hours%2Cwebsite&key={API_KEY}"
    response = requests.get(url)
    return response.json()

def get_country(x):
    with open("country.txt","r") as f:
        country_list = [i.upper() for i in f.read().split("\n")]
    for i in country_list:
        if(i in x):
            return i
    return " "
        
def process_data(df):
    df.columns = ['Name','Address']
    df = df.fillna(" ")
    df.fillna(" ",inplace=True)
    df['Address'] = df['Address'].apply(lambda x : " ".join(str(x).split("\n")))
    df['Address'] = df['Address'].apply(lambda x : x.strip())
    df.fillna(" ",inplace=True)
    df['Country'] = df['Address'].apply(lambda x : get_country(x))
    df['For_Search'] = [f"{df.iloc[i,0]} {df.iloc[i,2]}" for i in range(len(df))]
    return df

def convert_data():
    sheets = ['Shipper','Consignee']
    for i in range(1,5):
        for j in sheets:
            print(f"{j}_{i} ",end=" ")
            a = time.time()
            df = pd.read_excel(f"D:/PROJECTS/Devanshu/shipper-consignee/shipper-consignee-{i}.xlsx",sheet_name = j)
            df = process_data(df)
            df.to_csv(f"Data_{j}_{i}.csv",index = False)
            print(f"Took {round(time.time()-a,2)} sec")
            
def parse_data(x):
    col = ["name","formatted_phone_number","formatted_address","website","url"]
    data = [i:" " for i in col]
    for i in x:
        data[i]=x[i]
    return data
df = pd.read_csv("Data_Shipper_2.csv")
df = df.iloc[:50000,]
print(df.columns)
df['Place_id'] = df['For_Search'].apply(lambda x : get_place_id(x))
df['Data'] = df['Place_id'].apply(lambda x : parse_data(get_data(x)))
df.to_csv("Processed_Shipper_2.csv",index=False)
final = pd.DataFrame()
final['Name'] = df['Data'].apply(lambda x : x['name'])
final['Phone'] = df['Data'].apply(lambda x : x['formatted_phone_number'])
final['Address'] = df['Data'].apply(lambda x : x['formatted_address'])
final['Website'] = df['Data'].apply(lambda x : x['website'])
final['Url'] = df['Data'].apply(lambda x : x['url'])
final.to_csv("Final_Shipper_2.csv",index=False)

