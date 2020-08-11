import requests
from bs4 import BeautifulSoup
from newsplease import NewsPlease
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import pandas as pd
import gmplot
from geopy.geocoders import Nominatim
from nltk.stem import WordNetLemmatizer

toi="https://timesofindia.indiatimes.com"
crime_delhi="/topic/Crime/news/"
crime=toi+crime_delhi
l1=[]
for j in range(1,5):
    response=requests.get(crime+str(j))
    data=response.text
    soup=BeautifulSoup(data,"lxml")
    tags=soup.findAll("span",{'data-title':'Crime'})
    l2=[]
    for tag in tags:
        l2.append(tag.get('data-url'))
    for i in l2:
        if(i not in l1):
            l1.append(i)
            
            
rape=['rape','rapes','raped','raping','rapist','rapists']
murder=['murder','murders','murdering','murderer','murderers','murdered']
burglary=['burglary','burglar','burglars','burglaries']
kidnap=['kidnap','kidnapping ','kidnapper','kidnappers','kidnapped','kidnaps']
mug=['mug','mugged','mugs','mugger','mugging','muggings','muggers']
molest=['molest','molests','molester','molested','molesting','molesters','molestation']
pickpocket=['pickpocket','pickpocketing','pickpocketed','pickpockets','pickpocketer']
theft=['theft','thefts','thief','thieves','thievery']
robbery=['robbery','rob','robbed','robs','robberies','robber']
hijack=['h⁬ijack','hijacking','hijackings','hijacked','hijacker']
blackmail=['blackmail','blackmails','blackmailing','blackmailed','blackmailer']
dacoity=['dacoity','dacoit','dacoity','dacoits','dacoited','dacoiting']
fraud=['fraud','frauds']
smuggle=['smuggle','smuggling']
shoplift=['shoplift','shoplifting']
forgery=['forgery','forge','forges','forging','forged']
assassination=['assassination','assassinations','assassinated']
dowry=['dowry','dowries']
riot=['riot','riots']
homicide=['homicide','homicides']
stalk=['stalk','stalker','stalkers','stalked','stalking','stalks']


links=[]
lat = []
long= []
cities={}
j=0



for i in range(len(l1)):
    if(i>=3):
        sub=l1[i].split('/')
        if(sub[1]=='city'):
            cities[j]=sub[2].capitalize()
            j=j+1
            links.append(toi+l1[i])

articles={}
crimes={}
crimelist=['murder','kidnap','burglary', 'mug','molest','pickpocket','rape','arson',
'h⁬ijack', 'fraud','theft','manslaughter','smuggle','shoplift','robbery','blackmail',
'forgery','dacoity','assault','assassination','dowry','harassment','riot','stalk','homicide']
citylist=[
'Delhi','Goa','Thiruvananthapuram', 'Salem','Gurgaon','Bengaluru','Surat','Bhubaneswar',
'Agra', 'Mysuru','Pune','Chandigarh','Ghaziabad','Vijayawada','Noida','Bhopal',
'Aurangabad','Lucknow','Jaipur','Ludhiana','Ahmedabad','Vadodara','Patna','Chennai',
'Cuttack','Mumbai','Hyderabad','Coimbatore','Agartala', 'Nagpur','Thane','Indore',
'Madurai','Kochi','Nashik','Visakhapatnam','Amritsar','Kolkata','Allahabad','Dehradun',
'Mangaluru','Rajkot','Meerut','Kozhikode','Navi-mumbai','Faridabad','Bareilly','Mumbai']

df= pd.DataFrame(  0, 
columns= crimelist,
index= citylist,
)

for i in range(len(links)):
    article=NewsPlease.from_url(links[i])
    articles[i]=article.text

    sub_a=word_tokenize(articles[i])
    stop_words=set(stopwords.words('english'))
    for k in range(len(sub_a)):
        sub_a[k]=re.sub('[^A-Za-z0-9]+', '', sub_a[k]).lower()

    sub_a=' '.join(sub_a).split()
    sub_a = [w for w in sub_a if not w in stop_words]

    lemmatizer = WordNetLemmatizer()
    for k in range(len(sub_a)):
        sub_a[k]=lemmatizer.lemmatize(sub_a[k],pos='n')
        sub_a[k]=lemmatizer.lemmatize(sub_a[k],pos='v')
        if(sub_a[k] in rape):
            sub_a[k]=rape[0]
        if(sub_a[k] in murder):
            sub_a[k]=murder[0]
        if(sub_a[k] in burglary):
            sub_a[k]=burglary[0]
        if(sub_a[k] in kidnap):
            sub_a[k]=kidnap[0]
        if(sub_a[k] in mug):
            sub_a[k]=mug[0]
        if(sub_a[k] in molest):
            sub_a[k]=molest[0]
        if(sub_a[k] in pickpocket):
            sub_a[k]=theft[0]
        if(sub_a[k] in theft):
            sub_a[k]=theft[0]
        if(sub_a[k] in robbery):
            sub_a[k]=robbery[0]
        if(sub_a[k] in hijack):
            sub_a[k]=hijack[0]
        if(sub_a[k] in blackmail):
            sub_a[k]=blackmail[0]
        if(sub_a[k] in dacoity):
            sub_a[k]=dacoity[0]
        if(sub_a[k] in fraud):
            sub_a[k]=fraud[0]
        if(sub_a[k] in smuggle):
            sub_a[k]=smuggle[0]
        if(sub_a[k] in shoplift):
            sub_a[k]=shoplift[0]
        if(sub_a[k] in forgery):
            sub_a[k]=forgery[0]
        if(sub_a[k] in assassination):
            sub_a[k]=assassination[0]
        if(sub_a[k] in dowry):
            sub_a[k]=dowry[0]            
        if(sub_a[k] in stalk):
            sub_a[k]=stalk[0]
        if(sub_a[k] in riot):
            sub_a[k]=riot[0]
        if(sub_a[k] in homicide):
            sub_a[k]=homicide[0]  
    c=open('C:\\Users\Tanya\Downloads\crimes.txt',encoding='utf-8').read().splitlines()
    crime=[]
    for k in sub_a:
        if(k in c and k not in crime):
            crime.append(k)
    crimes[i]=crime
    print("Done ",i)
    print(article.title)
    '''places = GeoText(articles[i])'''
    print(crimes[i])
    print(cities[i])
        
    geolocator = Nominatim(user_agent="Tanya")
    location = geolocator.geocode(cities[i])
    print((location.latitude, location.longitude))
    lat.append(location.latitude)
    long.append(location.longitude)
    print("\n")
    
    df.loc[cities[i]][crimes[i]]+=1
    print(df.loc[cities[i]][crimes[i]])
    print("\n")
    
gmap4 = gmplot.GoogleMapPlotter(21,78, 5 ) 
gmap4.heatmap( lat, long ) 
gmap4.draw( "C:\\Users\\Tanya\\Desktop\\map.html" ) 
print(df)