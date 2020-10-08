from riotGamesAPI import download_match_data

# Input the desired regions. The possibilities are:
# eun1 ... Europe North East server
# euw1 ... Europe West server
# kr   ... Korean served
# na1  ... North American Server

regionIds = ["na1"]

# Input the number of matches you wish to download.
# Can be a specific value or None. If the value is None, all of the available matches are downloaded.
# If the specified number of matches is larger than the number of games held in the database,
# then the behaviour is reverted to the behaviour of None.

numMatches = None

# Downloads the data

for regionId in regionIds:
    download_match_data(
        regionId=regionId,
        numMatches=numMatches
    )
