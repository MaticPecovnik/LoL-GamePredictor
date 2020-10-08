import numpy as np


def processMatch(match_timeline, match_end):
    # The function recieves a timeline and outputs the aggregated data for the match after 5 min, 10 min, 15 min and 20 min of gameplay.
    # If the game was shorter than any of the alloted times, the function outputs None in its place.

    def processToFrame(match_timeline, minute):

        # Defines translation from input desired minutes to the frame notation used by the Riot API.
        frameNum = minute - 1

        # Defines all of the features.
        agg_data = {
            "blueWin": 0,
            "blueGold": 0,
            "blueExp": 0,
            "blueLvl": 0,
            "blueCS": 0,
            "blueJngCS": 0,
            "blueVisionScore": 0,
            "blueTowerScore": 0,
            "blueInhibScore": 0,
            "blueDrakeScore": 0,
            "blueHeraldScore": 0,
            "blueBaronScore": 0,
            "blueKillScore": 0,
            "blueDeathScore": 0,
            "blueAssistScore": 0,
            "blueFirstHerald": 0,
            "blueFirstDrake": 0,
            "blueFirstBaron": 0,
            "blueFirstElder": 0,
            "blueDrakeSoul": 0,
            "redGold": 0,
            "redExp": 0,
            "redLvl": 0,
            "redCS": 0,
            "redJngCS": 0,
            "redVisionScore": 0,
            "redTowerScore": 0,
            "redInhibScore": 0,
            "redDrakeScore": 0,
            "redHeraldScore": 0,
            "redBaronScore": 0,
            "redKillScore": 0,
            "redDeathScore": 0,
            "redAssistScore": 0,
            "redFirstHerald": 0,
            "redFirstDrake": 0,
            "redFirstBaron": 0,
            "redFirstElder": 0,
            "redDrakeSoul": 0,
            "blueExpDiff": 0,
            "blueLvlDiff": 0,
            "blueGoldDiff": 0,
            "blueDrakeDiff": 0,
            "blueBaronDiff": 0,
            "blueHeraldDiff": 0,
            "blueTowerDiff": 0,
            "blueInhibDiff": 0
        }

        # Checks if the game was shorter than the desired minutes.
        if len(match_timeline["frames"]) < minute:
            # If True the function returns nothing
            return None
        else:
            # If False, the function starts aggregating data.
            # First we append the data that was already aggregated by the Riot API by default.
            part_agg_data = match_timeline["frames"][frameNum]["participantFrames"]

            # A loop that goes over all 10 players
            for partId in range(1, 11):
                # Defines the current participant
                participant = part_agg_data[str(partId)]

                # players on the blue team
                if partId <= 5:
                    agg_data["blueGold"] += participant["totalGold"]
                    agg_data["blueExp"] += participant["xp"]
                    agg_data["blueLvl"] += participant["level"]
                    agg_data["blueCS"] += participant["minionsKilled"]
                    agg_data["blueJngCS"] += participant["jungleMinionsKilled"]
                # players on the red team
                else:
                    agg_data["redGold"] += participant["totalGold"]
                    agg_data["redExp"] += participant["xp"]
                    agg_data["redLvl"] += participant["level"]
                    agg_data["redCS"] += participant["minionsKilled"]
                    agg_data["redJngCS"] += participant["jungleMinionsKilled"]

            # Now we proceed to process the events up to the desired frame number
            part_min_data = match_timeline["frames"][:frameNum]

            # each frame (minute) prior to the desired minute we look at the events that occured
            for frame in part_min_data:
                # we look at each event seperatly
                for event in frame["events"]:

                    # events related to ward placement. We aggregate both ward placement and destruction into a vision score
                    if event["type"] == "WARD_PLACED":
                        if int(event["creatorId"]) <= 5:
                            agg_data["blueVisionScore"] += 1
                        else:
                            agg_data["redVisionScore"] += 1
                    elif event["type"] == "WARD_KILL":
                        if int(event["killerId"]) <= 5:
                            agg_data["redVisionScore"] += 1
                        else:
                            agg_data["blueVisionScore"] += 1

                    # events related to building (tower/inhibitor) destruction
                    elif event["type"] == "BUILDING_KILL":
                        # tower building kills
                        if event["buildingType"] == "TOWER_BUILDING":
                            if int(event["killerId"]) <= 5:
                                agg_data["blueTowerScore"] += 1
                            else:
                                agg_data["redTowerScore"] += 1

                        # inhibitor building kills
                        elif event["buildingType"] == "INHIBITOR_BUILDING":
                            if int(event["killerId"]) <= 5:
                                agg_data["blueInhibScore"] += 1
                            else:
                                agg_data["redInhibScore"] += 1

                    elif event["type"] == "CHAMPION_KILL":
                        if int(event["killerId"]) <= 5:
                            agg_data["blueKillScore"] += 1
                            agg_data["blueAssistScore"] += len(
                                event["assistingParticipantIds"])
                            agg_data["redDeathScore"] += 1
                        else:
                            agg_data["redKillScore"] += 1
                            agg_data["redAssistScore"] += len(
                                event["assistingParticipantIds"])
                            agg_data["blueDeathScore"] += 1
                    # Check if the event type is a baron/herald/drake kill
                    elif event["type"] == "ELITE_MONSTER_KILL":

                        # Drake Kill
                        if event["monsterType"] == "DRAGON":
                            if int(event["killerId"]) <= 5:
                                # Check if it is the first drake of the game
                                if agg_data["blueDrakeScore"] == 0 and agg_data["redDrakeScore"] == 0:
                                    agg_data["blueFirstDrake"] = 1
                                agg_data["blueDrakeScore"] += 1

                                # Check if it is first elder dragon
                                if event["monsterSubType"] == "ELDER_DRAGON":
                                    if agg_data["blueFirstElder"] == 0 and agg_data["redFirstElder"] == 0:
                                        agg_data["blueFirstElder"] = 1

                            else:
                                # Check if it is the first drake of the game
                                if agg_data["blueDrakeScore"] == 0 and agg_data["redDrakeScore"] == 0:
                                    agg_data["redFirstDrake"] = 1
                                agg_data["redDrakeScore"] += 1

                                # Check if it is first elder dragon
                                if event["monsterSubType"] == "ELDER_DRAGON":
                                    if agg_data["blueFirstElder"] == 0 and agg_data["redFirstElder"] == 0:
                                        agg_data["redFirstElder"] = 1

                        # Baron Kill
                        if event["monsterType"] == "BARON_NASHOR":
                            if int(event["killerId"]) <= 5:
                                # Check if it is the first baron of the game
                                if agg_data["blueBaronScore"] == 0 and agg_data["redBaronScore"] == 0:
                                    agg_data["blueFirstBaron"] = 1
                                agg_data["blueBaronScore"] += 1
                            else:
                                # Check if it is the first baron of the game
                                if agg_data["blueBaronScore"] == 0 and agg_data["redBaronScore"] == 0:
                                    agg_data["redFirstBaron"] = 1
                                agg_data["redBaronScore"] += 1
                        # Herald Kill
                        if event["monsterType"] == "RIFTHERALD":
                            if int(event["killerId"]) <= 5:
                                # Check if it is the first herald of the game
                                if agg_data["blueHeraldScore"] == 0 and agg_data["redHeraldScore"] == 0:
                                    agg_data["blueFirstHerald"] = 1
                                agg_data["blueHeraldScore"] += 1
                            else:
                                # Check if it is the first herald of the game
                                if agg_data["blueHeraldScore"] == 0 and agg_data["redHeraldScore"] == 0:
                                    agg_data["redFirstHerald"] = 1
                                agg_data["redHeraldScore"] += 1

            # Finally we engineer some of our own features which we think can be interesting.
            agg_data["blueExpDiff"] = agg_data["blueExp"] - agg_data["redExp"]
            agg_data["blueLvlDiff"] = agg_data["blueLvl"] - agg_data["redLvl"]
            agg_data["blueGoldDiff"] = agg_data["blueGold"] - \
                agg_data["redGold"]
            agg_data["blueDrakeDiff"] = agg_data["blueDrakeScore"] - \
                agg_data["redDrakeScore"]
            agg_data["blueBaronDiff"] = agg_data["blueBaronScore"] - \
                agg_data["redBaronScore"]
            agg_data["blueHeraldDiff"] = agg_data["blueHeraldScore"] - \
                agg_data["redHeraldScore"]
            agg_data["blueTowerDiff"] = agg_data["blueTowerScore"] - \
                agg_data["redTowerScore"]
            agg_data["blueInhibDiff"] = agg_data["blueInhibScore"] - \
                agg_data["redInhibScore"]

            # Check if the team has killed at least 4 drakes thus getting a permanent buff called drake soul
            if agg_data["blueDrakeScore"] >= 4:
                agg_data["blueDrakeSoul"] = 1
            elif agg_data["redDrakeScore"] >= 4:
                agg_data["redDrakeSoul"] = 1

            return agg_data

    return (processToFrame(match_timeline, 5 + i) for i in range(36))
