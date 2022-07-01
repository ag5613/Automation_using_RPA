import pandas as pd
import pyperclip
import requests
import re
url = "http://delhichamber.com/Custom-Freight-Shipping-Cargo.asp?ALP=All#4"
def city(x):
	data = {"Address":"","City":"","Phone":"","Fax":"","Email":"","ContactPerson":"","PinCode":""}
	for j,i in enumerate(x):
		if(j==0):
			data['Address'] = i
			if(re.search("[0-9]{6}",x[j+1])):
				p = re.findall("[0-9]{6}",x[j-1])
				if(len(p)>0):
					data['PinCode'] = p[0]
			else:
				data['Address'] = data['Address'] + " " + i
		if("City: " in i):
			data['City'] = i.split("City: ")[-1]
		elif("Phone:" in i):
			data['Phone'] = i.split("Phone: ")[-1]
		elif("Fax:" in i):
			data['Fax'] = i.split("Fax: ")[-1]
		elif("Email:" in i):
			data['Email'] = i.split("Email: ")[-1]
		elif("ContactPerson:" in i):
			data['ContactPerson'] = i.split("ContactPerson: ")[-1]
	return data

soup = BeautifulSoup(pyperclip.paste(),"html.parser")
tr = soup.findAll("tr")
data = {"Name":[],"Other":[]}
for i in tr:
    td = i.findAll("td")
    for j in range(2):
        if(j==1):
            data[l[j]].append([inn for inn in td[j].text.split("\n") if len(inn)>0])
	else:
            data[l[j]].extend([inn for inn in td[j].text.split("\n") if len(inn)>0])
            
for i in data:
    print(i,len(data[i]))
df = pd.DataFrame(data)
    
df['Other2'] = df['Other'].apply(lambda x : city(x))
other = df['Other2']
other = list(other)

final = {i:[] for i in other[0]}
for i in other:
    final[i].append(other[i])

for i in other:
    for j in i:
        final[j].append(i[j])
        
oth = pd.DataFrame(final)
f = pd.concat([df,oth],axis=1)

phone = f['Phone'].str.split(',', expand=True)
phone.columns = [f"Phone{i}" for i in list(phone.columns)]
f = pd.concat([f,phone],axis=1)
f.to_csv("Final_data.csv")

