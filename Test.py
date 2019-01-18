import requests
api_key = "89ea3f323d661f91d8df1df3388a2163"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
city_name = input("Enter city name : ")
complete_url = base_url + "appid=" + api_key + "&q=" + city_name
response = requests.get(complete_url)
x = response.json()
if x["cod"] != "404":
    y = x["main"]
    current_temperature = y["temp"]
    celsius = current_temperature - 273.15
    print(f"The temperature is {celsius:.2f} degrees celsius")
