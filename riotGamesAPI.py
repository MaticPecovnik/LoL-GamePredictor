import numpy as np
import pandas as pd
import os
import sys
import time
from riotwatcher import LolWatcher, ApiError

from processMatch import processMatch
from saveMatch import saveMatch
import config

# get api key from the config file. The user has to get his own API key from: https://developer.riotgames.com/
apiKey = config.apiKey

# a lightweight wrapper around the Riot Games API. Check it out on: https://riot-watcher.readthedocs.io/en/latest/riotwatcher/LeagueOfLegends/index.html
lol_watcher = LolWatcher(apiKey)


def download_match_data(regionId, numMatches):
    # A function that downloads a number of matches (input variable: numMatches) from the desired region (input variable: regionId).

    # Defines the match ID collection location and import it
    dir_path = os.path.join(os.getcwd(), "data", regionId, "matchIDs.txt")
    matchIDs = np.loadtxt(dir_path, dtype=str, delimiter=", ")

    # Checks the logic behind the number of desired matches
    if numMatches != None and numMatches < len(matchIDs):
        matchIDs = matchIDs[:numMatches]

    # Saving the data for each minute between 5 min and including 40 min.
    processedMatches = [[] for i in range(36)]

    print("Calling the Riot API... Downloading data for " +
          str(len(matchIDs)) + " matches on the " + str(regionId) + " server.")

    # Goes over the match IDs inside the entire collection
    for (k, matchID) in enumerate(matchIDs):

        # Used for estimating the remaining time.
        start_time = time.time()

        # Tries to get data from the Riot API
        try:
            # Calls the API for the game timeline which is aggregated
            match_timeline = lol_watcher.match.timeline_by_match(
                regionId, matchID)

            # Calls the API to see who won
            match_end = lol_watcher.match.by_id(regionId, matchID)

            # Determines who won the game
            blueWin = 0
            if match_end["teams"][0]["win"] == "Win":
                blueWin = 1

            # Goes over all of the aggregated data that is returned from the processMatch function defined in the processMatch.py file
            for (i, aggregated) in enumerate(processMatch(match_timeline, match_end)):
                if aggregated != None:
                    aggregated["blueWin"] = blueWin
                    processedMatches[i].append(aggregated)

        # Else it passes the specific match ID that lead to the failure
        except:
            pass

        # Used for estimating the remaining time.
        stop_time = time.time()
        time_diff = stop_time - start_time
        remaining_matches = len(matchIDs) - (k + 1)
        # Every 50 matches the API puts the API key on hold so this has to be factored in. The wait time is approximately 75 seconds.
        remaining_waitimes = remaining_matches // 50
        time_to_end = np.round(time_diff*remaining_matches +
                               75*remaining_waitimes, 1)

        sys.stdout.write("\rProcessed: " + str(k + 1) + " of " +
                         str(len(matchIDs)) + " matches on the " + str(regionId) + " server. Estimated time to end: " + str(time_to_end) + "s")
        sys.stdout.flush()

    print()
    print("Saving the match data.")
    for (i, matches) in enumerate(processedMatches):
        # Goes over all of the aggregated matches and saves them in the appropriate .csv file using the saveMatch function
        # found in the saveMatch.py file.
        saveMatch(
            matches=matches,
            fileName="match_summary_" +
            str(i + 5) + "min_" + str(regionId) + ".csv",
            regionId=regionId
        )
    print("Done for region " + str(regionId) + "!")
    print()

    return None
