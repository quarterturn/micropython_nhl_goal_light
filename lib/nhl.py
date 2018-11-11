import time
import urequests as requests

NHL_API_URL = "http://statsapi.web.nhl.com/api/v1/"


def get_teams():
    """ Function to get a list of all the teams name"""

    url = '{0}teams'.format(NHL_API_URL)
    response = requests.get(url)
    results = response.json()
    teams = []

    for team in results['teams']:
        teams.append(team['franchise']['teamName'])
    response.close()
    return teams


def get_team_id(team_name):
    """ Function to get team of user and return NHL team ID"""

    url = '{0}teams'.format(NHL_API_URL)
    response = requests.get(url)
    results = response.json()
    teams = []

    for team in results['teams']:
        if team['franchise']['teamName'] == team_name:
            return team['id']

    raise Exception("Could not find ID for team {0}".format(team_name))
    response.close()

def fetch_score(team_id):
    """ Function to get the score of the game depending on the chosen team.
    Inputs the team ID and returns the score found on web. """
    # assign it somethign so it won't cause problems if get(url) fails
    score = 0
    # Set URL depending on team selected
    url = '{0}schedule?teamId={1}'.format(NHL_API_URL, team_id)
    # Avoid request errors (might still not catch errors)
    try:
        response = requests.get(url)
        score = response.json()
        if int(team_id) == int(score['dates'][0]['games'][0]['teams']['home']['team']['id']):
            score = int(score['dates'][0]['games'][0]['teams']['home']['score'])
        else:
            score = int(score['dates'][0]['games'][0]['teams']['away']['score'])

        # Print score for test
        # print("Score: {0} Time: {1}:{2}:{3}".format(score, now.hour, now.minute, now.second))
        # print("Score: {0}".format(score))
        response.close()
        return score
    except:
        print("Error encountered, returning -1 for score")
        return -1


def check_season():
    """ Function to check if in season. Returns True if in season, False in off season. """
    # Get current time
    now = time.localtime()
    # element 1 of the now tuple is the month
    if now[1] in (7, 8):
        return False
    else:
        return True


def check_if_game(team_id):
    """ Function to check if there is a game now with chosen team. Returns True if game, False if NO game. """

    
    # Set URL depending on team selected
    url = '{0}schedule?teamId={1}'.format(NHL_API_URL, team_id) #Only shows games after noon, so will sleep till 12:10 pm
    # print("Gameday check URL:")
    # print(url)
    try:
        gameday_url = requests.get(url)
        # print(gameday_url.text)
        if "gamePk" in gameday_url.text:
            gameday_url.close()
            return True
        else:
            gameday_url.close()
            return False
    except:
        # Return True to allow for another pass for test
        print("Error encountered, returning True for check_game")
        #gameday_url.close()
        return True

      
def check_game_end(team_id):
    """ Function to check if the game ofchosen team is over. Returns True if game, False if NO game. """

    # Set URL depending on team selected
    url = '{0}schedule?teamId={1}'.format(NHL_API_URL, team_id)
    # Avoid request errors
    try:
        game_status = requests.get(url)
        game_status_data = game_status.json()
        data = int(game_status_data['dates'][0]['games'][0]['status']['statusCode'])
        if data == 7:
            game_status.close()
            return True
        else:
            game_status.close()
            return False
    except:
        # Return False to allow for another pass for test
        print("Error encountered, returning False for check_game_end")
        # game_status.close()
        return False
