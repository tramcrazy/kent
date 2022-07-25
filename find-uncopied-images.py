# Finds image files hat exist in the kent repo but not in the images repo
# (most likely caused by them not being referenced in an image tag)

import os, filecmp

KENT_REPO_PATH = "."
IMAGES_REPO_PATH = "../images"
IMAGE_ENDS = ["png", "jpeg", "jpg", "gif"]

def getImageList(path):
    imageList = []

    for dirName, subdirList, fileList in os.walk(path):
        for fname in fileList:

            for imageEnd in IMAGE_ENDS:
                if fname.endswith(imageEnd):
                    imageList.append(dirName + "/" + fname)

    return imageList

def getUncopiedImages(kentImages, imagesList):

    uncopiedImages = []
    numCopiedImages = 0

    for kentImage in kentImages:
        imageCopied = False
        for imageImage in imagesList:
            if (filecmp.cmp(kentImage, imageImage, shallow = True)):
                imageCopied = True
                numCopiedImages += 1
                break
        if (not imageCopied):
            uncopiedImages.append(kentImage)

    return uncopiedImages, numCopiedImages


def generateReport(difference, fileName):

    if (len(difference) == 0):
        output = ["No missing images"]
    else:
        output = difference
        
        with open(fileName, 'w') as reportFile:
            reportFile.write("")

        with open(fileName, 'a') as reportFile:
            for line in output:
                reportFile.write("{}\n".format(line))


kentImages = getImageList(KENT_REPO_PATH)
imagesImages = getImageList(IMAGES_REPO_PATH)
uncopiedImages, numCopiedImages = getUncopiedImages(kentImages, imagesImages)

output = []
output.append("Images in kent repo:\t{}".format(len(kentImages)))
output.append("Images in images repo:\t{}".format(len(imagesImages)))
output.append("Copied images:\t\t\t{}".format(numCopiedImages))
output.append("Uncopied images:\t\t{}".format(len(uncopiedImages)))
output.append("All uncopied images:")
output.extend(uncopiedImages)

generateReport(output, "uncopiedImages.txt")
