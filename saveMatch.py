import numpy as np
import pandas as pd
import os


def saveMatch(matches, fileName, regionId):
    # A function that recieves the list of matches (input variable: matches), the desired file name (input variable: fileName) and
    # the desired region (input variable: regionId).

    # Gets the features that we have aggregated the match data on in the processMatch function which can be found in the processMatch.py file.
    column_names = list(matches[0].keys())

    # Creates a numpy array to hold the values of the aggregated data.
    np_matches = np.empty(shape=(len(matches), len(matches[0])))

    # A loop that goes over all of the matches.
    for (i, match) in enumerate(matches):
        # A loop that goes over all features of a single match.
        for (j, key) in enumerate(matches[0].keys()):
            # Fills the previously empty numpy array with the appropriate values
            np_matches[i, j] = match[key]

    # Transfers the numpy array to a pandas.DataFrame
    df_matches = pd.DataFrame(np_matches, columns=column_names)

    # The pandas.DataFrame holding the values of all the games is saved
    save_dir_path = os.path.join(os.getcwd(), "data")
    file_path = os.path.join(save_dir_path, regionId, fileName)
    df_matches.to_csv(file_path)

    return None
