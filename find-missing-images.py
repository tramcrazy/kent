import os, sys, requests, json
from tabnanny import check
from bs4 import BeautifulSoup

MISSING_IMAGE_TEXT = "internal server error"

missingImages = []
checkedManifests = []

# If given, use given rootDir, otherwise use current directory
def getRootDir():
    if (len(sys.argv) > 1):
        return sys.argv[1]
    else:
        return '.'

def generateReport(reportFileName):

    # Remove duplicate results
    missingImagesSet = set(missingImages)

    if (len(missingImagesSet) == 0):
        output = ["No missing images"]
    else:
        output = ["Missing images: "]
        for tag in missingImagesSet:
            output.append(tag)
        
    with open(reportFileName, 'w') as reportFile:
        reportFile.write("")

    with open(reportFileName, 'a') as reportFile:
        for line in output:
            reportFile.write("{}\n".format(line))

rootDir = getRootDir()
imagesChecked = 0

for dirName, subdirList, fileList in os.walk(rootDir):
    
    # For all files in sub directory
    for fname in fileList:

        # For all files in sub directory
        for fname in fileList:

            if fname.endswith("md"):

                markdown = open("{}/{}".format(dirName, fname), "r").read()
                markdownSoup = BeautifulSoup(markdown, "html5lib")

                # For all <param> tags in markdown
                for tag in markdownSoup.find_all('param'):
    
                    # If tag contains ve-image attribute
                    if "ve-image-v2" in tag.attrs:

                        manifest = tag["manifest"]
                        imagesChecked += 1                  

                        if (not manifest in checkedManifests):

                            checkedManifests.append(manifest)

                            try:
                                url = requests.get(manifest)
                                text = url.text
                            except:
                                text = MISSING_IMAGE_TEXT

                            if (text.lower() == MISSING_IMAGE_TEXT):

                                imageName = manifest.replace("https://iiif.juncture-digital.org/", "")
                                output = "{} in {}".format(imageName, fname)

                                print(output + ", " + str(imagesChecked))
                                missingImages.append(output)

generateReport("missingImages.txt")
