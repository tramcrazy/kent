import os, sys, html
from bs4 import BeautifulSoup, Tag

WIKIMEDIA_URL = "upload.wikimedia.org"
MANIFEST_URL = "https://iiif.juncture-digital.org"
GH_ACCOUNT_NAME = "kent-map"
GH_REPO_NAME = "images"

invalidTags = []

# If given, use given rootDir, otherwise use current directory
def getRootDir():
    if (len(sys.argv) > 1):
        return sys.argv[1]
    else:
        return '.'

# Some tags have url in ve-image attribute
def getUrl(tag):
    if "url" in tag.attrs:
        return tag["url"]
    else: 
        return tag["ve-image"]

# Either wc for wikicommons or gh for selfhosted on GitHub
def getTagPrefix(url):
    if ((url.startswith("https://" + WIKIMEDIA_URL)) or (url.startswith("http://" + WIKIMEDIA_URL))):
        return "wc"
    elif ((not url.startswith("https://")) and (not url.startswith("http://"))):
        return "gh"
    else:
        invalidTags.append(tag)
        return ""

# Output tags not converted (as they are not selfhosted or wikicommons images)
def generateReport(reportFileName):

    # Remove duplicate results
    invalidSet = set(invalidTags)

    if (len(invalidSet) == 0):
        output = ["All tags converted"]
    else:
        output = ["Tags neither self hosted or from wikimedia so will not be converted: "]
        for tag in invalidSet:
            output.append(tag)
        
    with open(reportFileName, 'w') as reportFile:
        reportFile.write("")

    with open(reportFileName, 'a') as reportFile:
        for line in output:
            reportFile.write("{}\n".format(line))

# Gets URL to manifest
def getManifest(tag, imagePath):

    url = getUrl(tag)
    tagPrefix = getTagPrefix(url)

    splitUrl = url.split("/")
    imageName = splitUrl[len(splitUrl) - 1]

    if (tagPrefix == "wc"):
        return getWcManifest(tagPrefix, imageName)

    if (tagPrefix == "gh"):
        return getGhManifest(tagPrefix, imagePath, imageName)
    
    else:
        return ""

# Wikicommons image
def getWcManifest(tagPrefix, imageName):
    return "{}/{}:{}/manifest.json".format(MANIFEST_URL, tagPrefix, imageName)

# Self hosted tags
def getGhManifest(tagPrefix, imagePath, imageName):
    if (imagePath.startswith(".")):
        imagePath = imagePath[1:]

    if (imagePath.startswith("/")):
        imagePath = imagePath[1:]

    return  "{}/{}:{}/{}/{}/{}/manifest.json".format(MANIFEST_URL, tagPrefix, GH_ACCOUNT_NAME, GH_REPO_NAME, imagePath, imageName)

rootDir = getRootDir()

for dirName, subdirList, fileList in os.walk(rootDir):
    
    # For all files in sub directory
    for fname in fileList:

        # For all files in sub directory
        for fname in fileList:

            if fname.endswith("md"):
                
                changeMade = False
                markdown = open("{}/{}".format(dirName, fname), "r").read()
                markdownSoup = BeautifulSoup(markdown, "html5lib")

                # For all <param> tags in markdown
                for tag in markdownSoup.find_all('param'):
    
                    # If tag contains ve-image attribute, change it to ve-image-v2
                    if "ve-image" in tag.attrs:

                        manifest = getManifest(tag, dirName)

                        # If a manifest was generated, replace tag
                        if (len(manifest) > 0):

                            newTag = Tag(
                                builder = markdownSoup.builder, 
                                name = "param", 
                                attrs = {"ve-image-v2" : None, "manifest" : manifest})

                            tag.replace_with(newTag)
                            changeMade = True

                # Write changes
                if (changeMade):
                    with open("{}/{}".format(dirName, fname), "w") as file:
                        file.write(str(html.unescape(markdownSoup)))

generateReport("tag_renaming_result.txt")