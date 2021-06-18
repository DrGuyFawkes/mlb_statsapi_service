import json
import requests
import pandas as pd


def get_playbyplay_statsapi(gamepk):

    apicall = 'https://statsapi.mlb.com/api/v1/game/' + str(gamepk) + '/playByPlay'
    statapi = requests.get(apicall)
    playbyplay = json.loads(statapi.text)

    pbp = []
    
    if len(playbyplay['allPlays']) > 0:
        for play in playbyplay['allPlays']:    

            Pitcher_Id = play['matchup']['pitcher']['id']
            Pitcher_Throws = play['matchup']['pitchHand']['code']
            Batter_Id = play['matchup']['batter']['id']
            Batter_Stands = play['matchup']['batSide']['code']
        
            if len(play['playEvents']) > 0:
                for play_event in play['playEvents']:        
                    if play_event['type'] == 'pitch': 

                        json_normalized = pd.io.json.json_normalize(play_event, sep='_')
                        row = json_normalized.to_dict(orient='records')[0]
                        row['PitcherId'] = play['matchup']['pitcher']['id']
                        row['PitcherThrows'] = play['matchup']['pitchHand']['code']
                        row['BatterId'] = play['matchup']['batter']['id']
                        row['BatterStands'] = play['matchup']['batSide']['code']
                        row['gamepk'] = str(gamepk)
                        row['id'] = str(row['playId'])
                        
                        drop_list = ['index', 'playId']
                        for key in drop_list:
                            del row[key]

                        pbp.append(row)
    
    return pbp