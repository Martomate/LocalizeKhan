import requests
from bs4 import BeautifulSoup

page = requests.get("http://www.mathwords.com/a_to_z.htm")

#Om hemsidan har hämtats korrekt så isoleras orden och läggs in i en lista.
if page.status_code == 200:

	#Får ut orden i en lista.
	soup = BeautifulSoup(page.content, 'html.parser')
	listan = []
	for link in soup.find_all('a', target="_self"):
		str = link.get("href").split('/')
		str2 = str[1].split('.')
		listan.append(str2[0])

svList = []

#För varje specifikt ord, kolla om det finns en engelsk wiki-sida om det. 
#Kolla om det finns en svensk motsvarighet av ordet.
#Läs in den svenska hemsidan mha BeautifulSoup och lägg till titeln (översättningen)
#i en lista.
for word in listan:
	print("Current word: " + word)
	tmpPage = requests.get("https://www.wikipedia.org/wiki/" + word)
	
	if tmpPage.status_code == 200:
		#Wiki-sida existerar
		tmpSoup = BeautifulSoup(tmpPage.content, 'html.parser')

		#Kolla om det finns en motsvarande svensk wiki.
		if tmpSoup.find('a', lang="sv") != None:
			#Svensk wiki finns

			#Kopiera Tag:en där svenska wiki-sidan finns.
			sv = tmpSoup.find('a', lang="sv")

			#Extrahera HTML:en av den svenska versionen från Tag:en ovanför.
			svHTML = sv.get('href')

			#Läs in den svenska sidans HTML-kod
			svPage = requests.get(svHTML)
			
			if svPage.status_code == 200:
				#Gör om svPage innehållet till typen BS.
				svSoup = BeautifulSoup(svPage.content, 'html.parser')
				#Hitta wiki-sidans titel som också är översättningen på word.
				svWord = svSoup.find('title')
				#Lägg till svenska ordet i en översättningslista.
				svList.append(word + "=" + svWord.string)
	
print("svList:")
print(svList)

#Skriver det engelska ordet med svensk översättning i ny fil med en översättning per rad.
#Format:	engelska=svenska"\n"
file = open("testfile.txt","w")
for translation in svList:
	file.write(translation.replace(" – Wikipedia", "") + "\n")
file.close()




