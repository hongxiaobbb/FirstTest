import requests


test_data = [x for x in range(3)]
#test_data += [x for x in range(16)]

response = requests.post('http://SLB-FG2CDZ1.dir.slb.com:5000/inference', json=[test_data, test_data, test_data])
#response = requests.get('http://SLB-FG2CDZ1.dir.slb.com:5000/inference')

temp = response.json()

print(temp[1]+temp[2])
# print("success")