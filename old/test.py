import requests
r = requests.get(url = 'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=370271383631C9089D74EBA5806050F9&format=json&steamids=7656198036370701')
data = r.json()
print(data)
print(str(r.json()['response']['players']) == '[]')