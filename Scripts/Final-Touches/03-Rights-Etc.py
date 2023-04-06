import utils
import os

manifestNetworkPath = "/Users/jacob/Documents/Git Repos/coeso-deliverable"
#manifestNetworkPath = "/Users/jacob/Documents/Git Repos/POC-mirador/www/COESO-Project-Network"

manifestMediaPath = "https://coeso.tetras-libre.fr/data/coeso-deliverable/media/"
#manifestMediaPath = "http://localhost:9000/data/COESO-Project-Network/media/"


csvMediaPath = "/Users/jacob/Documents/Git Repos/Spider Webs/COESO-Project/media"
dateFile = "/Users/jacob/Desktop/dateFileSCV.csv"
csvData = utils.loadCSV(dateFile)

manifestFiles = utils.collectFiles(manifestNetworkPath, ["json"])

for manifest in manifestFiles:
    manifestData = utils.readJson(manifest)

    manifestData["rights"] = "https://creativecommons.org/licenses/by-nc-nd/4.0/"
    manifestData["provider"] = [
        {
            "id" : "https://www.univ-rennes2.fr/",
            "type" : "Agent",
            "label" : {"en" : ["Rennes 2 University"], "fr" : ["Université Rennes 2"]},
            "homepage" : [
                {
                    "id" : "https://www.univ-rennes2.fr/",
                    "type" : "Text",
                    "label" : {"en" : ["Rennes 2 University"], "fr" : ["Université Rennes 2"]},
                    "format" : "text/html"
                }
            ]
        }
    ]
    manifestData["requiredStatement"] = {
        "label" : {"en" : ["Attribution"], "fr" : ["Attribution"]},
        "value" : {"en" : ["Rennes 2 University"], "fr" : ["Université Rennes 2"]},
    }

    manifestData["logo"] = {
                "id" : "https://intranet.univ-rennes2.fr/sites/default/files/resize/UHB/SERVICE-COMMUNICATION/logor2-noir-150x147.png",
                "type": "Image",
                "format": "image/png",
                "height": 150,
                "width": 147
            }
    
    manifestTitle = manifestData["label"][list(manifestData["label"].keys())[0]][0]
    manifestMedium = manifestData["items"][0]["items"][0]["items"][0]["body"]["type"]


    manifestData["metadata"] = [
        {
            "label" : {"en" : ["Title"],  "fr" : ["Titre"]},
            "value" : {
                "en" : [manifestTitle],  
                "fr" : [manifestTitle]
            }
        },
        {
            "label" : {"en" : ["Creator"],  "fr" : ["Créateur"]},
            "value" : {
                "en" : ["Jacob Hart, Clarissse Bardiot, Cosetta Graffione, Stefania Ferrando, Daniele Marranca, Irénée Blin, Sébastien Hildebrand, David Rouquet, Anthony Geourgeon"],  
                "fr" : ["Jacob Hart, Clarissse Bardiot, Cosetta Graffione, Stefania Ferrando, Daniele Marranca, Irénée Blin, Sébastien Hildebrand, David Rouquet, Anthony Geourgeon"]
            }
        },
        {
            "label" : {"en" : ["Medium"],  "fr" : ["Médium"]},
            "value" : {
                "en" : [manifestMedium],  
                "fr" : [manifestMedium]
            }
        }
    ]

    thisMediaFile = manifestData["items"][0]["items"][0]["items"][0]["body"]["id"]
    onlyMedia = thisMediaFile.split(manifestMediaPath)[1]
    toSearch = os.path.join(csvMediaPath, onlyMedia)
    
    dates = utils.csvGetDates(csvData, toSearch)

    finalDate = ''
    gotStart = False
    if dates[0] != None:
        finalDate = finalDate + dates[0].split(' ')[0]
        gotStart = True

    if dates[1] != None:
        if gotStart:
            finalDate = finalDate + ' - '
        finalDate = finalDate + dates[1].split(' ')[0]
    
    if finalDate != '':
        manifestData["metadata"].append({
            "label" : {"en" : ["Date"],  "fr" : ["Date"]},
            "value" : {
                "en" : [finalDate],  
                "fr" : [finalDate]
            }
        })
    
    if dates[2] != None:
        manifestData["metadata"].append({
            "label" : {"en" : ["Region"],  "fr" : ["Région"]},
            "value" : {
                "en" : [dates[2]],  
                "fr" : [dates[2]]
            }
        })

    utils.writeJson(manifestData, manifest)