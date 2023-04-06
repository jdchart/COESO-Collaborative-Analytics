import utils
import os
from PIL import Image

manifestPath = "https://coeso.tetras-libre.fr/data/coeso-deliverable"
manifestNetworkPath = "/Users/jacob/Documents/Git Repos/coeso-deliverable"

#manifestNetworkPath = "/Users/jacob/Documents/Git Repos/POC-mirador/www/COESO-Project-Network"
#manifestPath = "http://localhost:9000/data/COESO-Project-Network"


manifestFiles = utils.collectFiles(manifestNetworkPath, ["json"])

def resiezThumbnail(orginalImage, savePath, maxDim):
    print()
    image = Image.open(orginalImage)

    if image.size[0] > maxDim or image.size[1] > maxDim:
        print("resizing " + orginalImage + '...')
        if image.size[0] > image.size[1]:
            scaleFactor = maxDim / image.size[0]
            otherDim = int(image.size[1] * scaleFactor)

            rgbIm = image.convert('RGB')
            rgbIm.thumbnail((maxDim, otherDim))
            rgbIm.save(savePath)

            return [maxDim, otherDim]
        else:
            scaleFactor = maxDim / image.size[1]
            otherDim = int(image.size[0] * scaleFactor)

            rgbIm = image.convert('RGB')
            rgbIm.thumbnail((otherDim, maxDim))
            rgbIm.save(savePath)

            return [otherDim, maxDim]
        
    else:
        print("Image was already the right size")
        return [image.size[0], image.size[1]]

for manifest in manifestFiles:
    manifestData = utils.readJson(manifest)
    manifestTitle = manifestData["label"][list(manifestData["label"].keys())[0]][0]


    if "thumbnail" in list(manifestData["items"][0].keys()):
        if len(manifestData["items"][0]["thumbnail"]) > 0:

            realThumbPath = manifestData["items"][0]["thumbnail"][0]["id"]
            mediaAlone = realThumbPath.split(manifestPath)[1][1:]
            localThumbPath = os.path.join(manifestNetworkPath, mediaAlone)
            newSizes = resiezThumbnail(localThumbPath, localThumbPath, 100)

            manifestData["items"][0]["thumbnail"][0]["width"] = newSizes[0]
            manifestData["items"][0]["thumbnail"][0]["height"] = newSizes[1]
        else:
            print("NO THUMBNAIL for " + manifestTitle)

            realImagePath = manifestData["items"][0]["items"][0]["items"][0]["body"]["id"]
            thumbName = os.path.splitext(os.path.basename(realImagePath))[0] + "_THUMBNAIL.jpg"
        
            mediaAlone = realImagePath.split(manifestPath)[1][1:]
            localThumbPath = os.path.join(manifestNetworkPath, mediaAlone)

            imageWritePath = os.path.join(manifestNetworkPath, "media/" + thumbName)
            imageRealPath = os.path.join(manifestPath, "media/" + thumbName)

            print(realImagePath)
            print(thumbName)
            print(localThumbPath)
            print(imageWritePath)
            print(imageRealPath)

            newSizes = resiezThumbnail(localThumbPath, imageWritePath, 100)

            manifestData["items"][0]["thumbnail"] = [
                {
                    "id" : imageRealPath,
                    "type": "Image",
                    "format": "image/jpeg",
                    "height": newSizes[0],
                    "width": newSizes[1]
                }
            ]

    else:
        print("NO THUMBNAIL for " + manifestTitle)

        realImagePath = manifestData["items"][0]["items"][0]["items"][0]["body"]["id"]
        thumbName = os.path.splitext(os.path.basename(realImagePath))[0] + "_THUMBNAIL.jpg"
    
        mediaAlone = realImagePath.split(manifestPath)[1][1:]
        localThumbPath = os.path.join(manifestNetworkPath, mediaAlone)

        imageWritePath = os.path.join(manifestNetworkPath, "media/" + thumbName)
        imageRealPath = os.path.join(manifestPath, "media/" + thumbName)

        print(realImagePath)
        print(thumbName)
        print(localThumbPath)
        print(imageWritePath)
        print(imageRealPath)

        newSizes = resiezThumbnail(localThumbPath, imageWritePath, 100)

        manifestData["items"][0]["thumbnail"] = [
            {
                "id" : imageRealPath,
                "type": "Image",
                "format": "image/jpeg",
                "height": newSizes[0],
                "width": newSizes[1]
            }
        ]

    utils.writeJson(manifestData, manifest)