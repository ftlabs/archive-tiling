from bs4 import BeautifulSoup
import urllib2
import os

archiveRoot = "http://newspaperarchive.ftroot.com"

if not os.path.exists("output"):
    os.makedirs("output")

yearLinks = []

for tag in BeautifulSoup(urllib2.urlopen(archiveRoot + "/html").read(), "html5lib").find_all('a'):
	
	HREF = tag.get('href')
	
	if HREF != "/html/web.config" and HREF != "/":
		yearLinks.append( str(HREF) )


for year in yearLinks:
	
	publicationYear = year.split('/')[2]
	
	if not os.path.exists("output/" + publicationYear):
		os.makedirs("output/" + publicationYear)
		
	months = BeautifulSoup(urllib2.urlopen(archiveRoot + year).read(), "html5lib").find_all('a')
	months.pop(0)
	
	for month in months:
		
		publicationMonth = month.get_text()
	
		if not os.path.exists("output/" + publicationYear + "/" + publicationMonth):
			os.makedirs("output/" + publicationYear + "/" + publicationMonth)
			
		days = BeautifulSoup(urllib2.urlopen(archiveRoot + month.get('href')).read(), "html5lib").find_all('a')
		days.pop(0)
		
		for day in days:
			
			publicationDay = day.get_text()
			
			if not os.path.exists("output/" + publicationYear + "/" + publicationMonth + "/" + publicationDay):
				os.makedirs("output/" + publicationYear + "/" + publicationMonth + "/" + publicationDay)
			
			pages = BeautifulSoup(urllib2.urlopen(archiveRoot + day.get('href')).read() , "html5lib").find_all('a')
			pages.pop(0)
			
			for idx, page in enumerate(pages):
				imagePath = BeautifulSoup(urllib2.urlopen(archiveRoot + page.get('href')).read() , "html5lib").find('img').get('src')
				print(imagePath)
				print("Retrieving " + archiveRoot + imagePath)			
				image = urllib2.urlopen(archiveRoot + imagePath).read()
				
				outputPath = "output/" + publicationYear + "/" + publicationMonth + "/" + publicationDay + "/"
				outputFile = outputPath + "page" + str(idx) + ".jpg"
				
				print("Writing " + archiveRoot + imagePath + " to " + outputFile)
				l = open(outputFile, "wb")
				l.write(image)
				print("Write complete.")
				print("Generating tiles")
				# Example: gdal2tiles.py -z "1-5" -v -w "all" -p 'raster' -a 0 [PATH TO ARCHIVE IMAGE]/[ARCHIVE IMAGE].JPG ./gdal_tiles
				os.system("gdal2tiles-mod.py -z '1-5' -w 'all' -p 'raster' -a 0 " + outputFile +  " " + outputPath + "/" + str(idx) )
				print("Tile generation complete. \n")
				
		break
		
	break