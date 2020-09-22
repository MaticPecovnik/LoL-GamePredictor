import numpy as np
import pandas as pd
import os


def saveMatch(matches, fileName):

    column_names = list(matches[0].keys())
    np_matches = np.empty(shape=(len(matches), len(matches[0])))

    for (i, match) in enumerate(matches):
        for (j, key) in enumerate(matches[0].keys()):
            np_matches[i, j] = match[key]

    df_matches = pd.DataFrame(np_matches, columns=column_names)

    save_dir_path = os.path.join(os.getcwd(), "data")
    file_path = os.path.join(save_dir_path, fileName)
    df_matches.to_csv(file_path)

    return None
