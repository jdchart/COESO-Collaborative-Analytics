import utils
import cv2
import os

manifestPrefix = "https://coeso.tetras-libre.fr/data/coeso-deliverable"
manifestNetworkPath = "/Users/jacob/Documents/Git Repos/coeso-deliverable"
manifestFiles = utils.collectFiles(manifestNetworkPath, ["json"])

for manifest in manifestFiles:
    manifestData = utils.readJson(manifest)
    mainItem = manifestData["items"][0]["items"][0]["items"][0]
    if mainItem["body"]["type"] == "Video":
        localVideoPath = mainItem["body"]["id"].replace(manifestPrefix, manifestNetworkPath)
        
        manifestID = mainItem["id"].split(manifestPrefix + "/")[1]
        manifestID = manifestID.split("/")[0]
        
        #thumbnailWritePath = os.path.join("/Users/jacob/Documents/Git Repos/spider-python/Work/Final-Touches/output", manifestID + ".jpg")
        thumbnailWritePath = os.path.join(manifestNetworkPath, "media/" + manifestID + "_THUMBNAIL.jpg")
        thumnailRealPath = os.path.join(manifestPrefix, "media/" + manifestID + "_THUMBNAIL.jpg")

        openCVvideo = cv2.VideoCapture(localVideoPath)
        frames = openCVvideo.get(cv2.CAP_PROP_FRAME_COUNT)
        width = int(openCVvideo.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(openCVvideo.get(cv2.CAP_PROP_FRAME_HEIGHT))
        middleFrame = int(frames / 2)

        utils.save_frame(localVideoPath, middleFrame, thumbnailWritePath)

        thumnailItem = {
            "id": thumnailRealPath,
            "type": "Image",
            "format": "image/jpeg",
            "height": height,
            "width": width,
        }

        manifestData["items"][0]["thumbnail"].append(thumnailItem)

        print(manifestID)
        print(mainItem["body"]["id"])
        print(thumnailRealPath)
        print(localVideoPath + "\n")

    utils.writeJson(manifestData, manifest)
