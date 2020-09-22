import numpy as np
import pandas as pd
import os
import sys
import time
from riotwatcher import LolWatcher, ApiError

from processMatch import processMatch
from saveMatch import saveMatch
import config

apiKey = config.apiKey
lol_watcher = LolWatcher(apiKey)

dir_path = os.path.join(os.getcwd(), "data", "matchIDs.txt")
matchIDs = np.loadtxt(dir_path, dtype=str, delimiter=", ")
processedMatches = [
    [],  # game state after 5 minuts of play
    [],  # game state after 10 minuts of play
    [],  # game state after 15 minuts of play
    [],  # game state after 20 minuts of play
    [],  # game state after 25 minuts of play
    []   # game state after 30 minuts of play
]

print("Calling the Riot API... Downloading data for " +
      str(len(matchIDs)) + " matches.")

for (k, matchID) in enumerate(matchIDs):

    start_time = time.time()

    try:
        match_timeline = lol_watcher.match.timeline_by_match("eun1", matchID)
        match_end = lol_watcher.match.by_id("eun1", matchID)

        blueWin = 0
        if match_end["teams"][0]["win"] == "Win":
            blueWin = 1

        for (i, aggregated) in enumerate(processMatch(match_timeline)):
            if aggregated != None:
                aggregated["blueWin"] = blueWin
                processedMatches[i].append(aggregated)
    except:
        pass

    stop_time = time.time()
    time_diff = stop_time - start_time
    time_to_end = np.round(time_diff*(len(matchIDs) - (k + 1)), 1)

    sys.stdout.write("\rProcessed: " + str(k + 1) + " of " +
                     str(len(matchIDs)) + " matches. Estimated time to end: " + str(time_to_end) + "s")
    sys.stdout.flush()

for (i, matches) in enumerate(processedMatches):
    saveMatch(matches, "match_summary_" + str((i+1)*5) + "min.csv")
