import utils


manifestNetworkPath = "/Users/jacob/Documents/Git Repos/coeso-deliverable"
#manifestNetworkPath = "/Users/jacob/Documents/Git Repos/POC-mirador/www/COESO-Project-Network"

manifestPath = "https://coeso.tetras-libre.fr/data/coeso-deliverable/"
#manifestPath = "http://localhost:9000/data/COESO-Project-Network/"

webPath = "/Users/jacob/Documents/Git Repos/Spider Webs/COESO-Project"
webFiles = utils.collectFiles(webPath, ["json"])

manifestFiles = utils.collectFiles(manifestNetworkPath, ["json"])

for manifest in manifestFiles:
    manifestData = utils.readJson(manifest)

    manifestUUID = manifestData["items"][0]["id"].split(manifestPath)[1].split("/")[0]
    
    for item in webFiles:
        webRead = utils.readJson(item)
        if "uuid" in list(webRead.keys()):
            if webRead["uuid"] == manifestUUID:
                print(webRead["description"])
                manifestData["metadata"].append({
                    "label" : {"en" : ["Description"], "fr" : ["Déscription"]},
                    "value" : {
                        "en" : [webRead["description"]["en"]], 
                        "fr" : [webRead["description"]["fr"]]
                    }
                })

    utils.writeJson(manifestData, manifest)