import requests
import untangle
import shutil

xmlcast = requests.get('https://www.democracynow.org/podcast.xml')
casts = untangle.parse(xmlcast.text)
print(casts.get_elements('xmlns:media'))
baseurl='https://traffic.libsyn.com/democracynow/dn'
year='2021'
day='12'
month='03'
extension = '.mp3'
filename= f'Democracy_Now_{day}{month}{year}{extension}'
h = requests.get(f'{baseurl}{year}-{month}{day}{extension}', stream=True)
with open(filename, 'wb') as f:
    shutil.copyfileobj(h.raw, f)
