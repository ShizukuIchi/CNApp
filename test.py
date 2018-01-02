import json
f = open(fileName,encoding = 'utf8')
data = json.load(f)["records"]
f.close()
holidays = list(map(lambda d: d.split('/')[2], filter(lambda ymd: ymd.split('/')[1] == month ,[holiday["date"] for holiday in data])))
return holidays