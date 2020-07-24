import requests
import json

class PlayerRoster():
    def __init__(self, teamRoster):
        self.__teamRoster = {}


    # CREATES THE ROSTER (A DICTIONARY) {TEAM: PLAYERS}
    def createPlayerRoster(self):
        #used to creat newLink to iterate through pages
        page = 1
        linkStart = "https://www.balldontlie.io/api/v1/players?page="
        linkEnd = "&per_page=100"

        #gets number of total pages
        getMeta = requests.get("https://www.balldontlie.io/api/v1/players?page=1&per_page=100").text
        getMetaJson = json.loads(getMeta)
        meta = getMetaJson["meta"]
        numPages = meta["total_pages"]

        #adds players to dictionary {team: name id, name id}
        while page <= numPages:
            valueDict = {}
            newLink = linkStart + str(page) + linkEnd

            response = requests.get(newLink).text
            playerList = json.loads(response)
            
            for player in playerList["data"]:
                playerValue = 0
                team = player["team"]
                abbreviation = team["abbreviation"]
                playerID = player["id"]
                name = player["first_name"] + " " + player["last_name"] + " " + str(player["id"])
                self.getPlayerStats(valueDict, str(playerID), playerValue)
                if playerValue > 0:
                    if abbreviation in self.__teamRoster:
                        self.__teamRoster[abbreviation].append(name)
                    else:
                        self.__teamRoster[abbreviation] = [name]
            page += 1   

        print(self.__teamRoster)


    # GETS THE STATS AND OVERALL VALUE OF A PLAYER BASED ON ID
    def getPlayerStats(self, valueDict: dict, player_id: str, playerValue) -> float:
        statDict = {}

        # Getting information from API
        requestString = "https://www.balldontlie.io/api/v1/season_averages?season=2018&player_ids[]="
        requestString = requestString + player_id
        # response = requests.get("https://www.balldontlie.io/api/v1/season_averages?season=2018&player_ids[]=666786")
        response = requests.get(requestString)
        playerStats = response.json()

        # Creating a dictionary with simple stats {id: points, assists, rebounds, fg%}
        for player in playerStats["data"]:
            statDict[player["player_id"]] = [player["pts"], player["ast"], player["reb"], player["fg_pct"]]

        # Calculate overall player value (NEED FUNCTION TO CALCULATE THIS)
        for value in statDict.values():
            playerValue = value[0] + value[1]*0.75 + value[2]*0.25

        return playerValue