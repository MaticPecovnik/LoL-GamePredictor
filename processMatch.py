import numpy as np


def processMatch(match_timeline):
    # The function recieves a timeline and outputs the aggregated data for the match after 5 min, 10 min, 15 min and 20 min of gameplay.
    # If the game was shorter than any of the alloted times, the function outputs None in its place.

    def processToFrame(match_timeline, minute):
        frameNum = minute - 1

        agg_data = {
            "blueWin": 0,
            "blueGold": 0,
            "blueExp": 0,
            "blueLvl": 0,
            "blueCS": 0,
            "blueJngCS": 0,
            "blueVisionScore": 0,
            "blueTowerScore": 0,
            "blueDrakeScore": 0,
            "blueHeraldScore": 0,
            "blueBaronScore": 0,
            "blueKillScore": 0,
            "blueDeathScore": 0,
            "blueAssistScore": 0,
            "redGold": 0,
            "redExp": 0,
            "redLvl": 0,
            "redCS": 0,
            "redJngCS": 0,
            "redVisionScore": 0,
            "redTowerScore": 0,
            "redDrakeScore": 0,
            "redHeraldScore": 0,
            "redBaronScore": 0,
            "redKillScore": 0,
            "redDeathScore": 0,
            "redAssistScore": 0,
        }

        if len(match_timeline["frames"]) < minute:
            return None
        else:
            # First we append the already aggregated data.
            part_agg_data = match_timeline["frames"][frameNum]["participantFrames"]

            for partId in range(1, 11):
                participant = part_agg_data[str(partId)]
                if partId <= 5:
                    # players on the blue
                    agg_data["blueGold"] += participant["totalGold"]
                    agg_data["blueExp"] += participant["xp"]
                    agg_data["blueLvl"] += participant["level"]
                    agg_data["blueCS"] += participant["minionsKilled"]
                    agg_data["blueJngCS"] += participant["jungleMinionsKilled"]
                else:
                    # players on the red
                    agg_data["redGold"] += participant["totalGold"]
                    agg_data["redExp"] += participant["xp"]
                    agg_data["redLvl"] += participant["level"]
                    agg_data["redCS"] += participant["minionsKilled"]
                    agg_data["redJngCS"] += participant["jungleMinionsKilled"]

            # Now we proceed to process the events
            part_min_data = match_timeline["frames"][:frameNum]

            for frame in part_min_data:
                for event in frame["events"]:
                    # we have various events which we have to treat independently
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
                    elif event["type"] == "BUILDING_KILL" and event["buildingType"] == "TOWER_BUILDING":
                        if int(event["killerId"]) <= 5:
                            agg_data["blueTowerScore"] += 1
                        else:
                            agg_data["redTowerScore"] += 1
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
                    elif event["type"] == "ELITE_MONSTER_KILL":
                        if event["monsterType"] == "DRAGON":
                            if int(event["killerId"]) <= 5:
                                agg_data["blueDrakeScore"] += 1
                            else:
                                agg_data["redDrakeScore"] += 1
                        if event["monsterType"] == "BARON_NASHOR":
                            if int(event["killerId"]) <= 5:
                                agg_data["blueBaronScore"] += 1
                            else:
                                agg_data["redBaronScore"] += 1
                        if event["monsterType"] == "RIFTHERALD":
                            if int(event["killerId"]) <= 5:
                                agg_data["blueHeraldScore"] += 1
                            else:
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

            return agg_data

    return (processToFrame(match_timeline, 5 + i) for i in range(36))
