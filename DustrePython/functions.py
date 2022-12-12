from urllib import response
import requests, json
from requests.exceptions import HTTPError


def postOmie(endpoint, app_key, app_secret, call, param,):

    header = {
        'Content-type': "application/json"
    }

    content = {
        "app_key":app_key,
        "app_secret":app_secret,
        "call":call,
        "param":param
    }

    try:
        response = requests.post(
            url=endpoint,
            data=json.dumps(content),
            headers=header
            )
        status = response.status_code
        if (status != 204 and response.headers["content-type"].strip().startswith("application/json")):
            try:
                json_response = response.json()
                return json_response

            except ValueError:
                return("Bad Data from Server. Response content is not valid JSON")

        elif (status != 204):
            try:
                return response.json()

            except ValueError:
                return('Bad Data From Server. Reponse content is not valid text')

    except HTTPError as http_err:
        return(f'HTTP error occurred: {http_err}')

    except Exception as err:
        return(f'Other error occurred: {err}')
    
    return 0

def getPloomes(endpoint, user_key):

    header = {
        'Content-type': "application/json",
        'user-key': user_key
    }

    try:
        ploomesResponse = requests.get(
        url=endpoint,
        headers=header
        )
        status = ploomesResponse.status_code
        if (status != 204 and ploomesResponse.headers["content-type"].strip().startswith("application/json")):
            try:
                json_ploomesResponse = ploomesResponse.json()
                return json_ploomesResponse

            except ValueError:
                return("Bad Data from Server. ploomesResponse content is not valid JSON")

        elif (status != 204):
            try:
                return ploomesResponse.json()

            except ValueError:
                return('Bad Data From Server. Reponse content is not valid text')

    except HTTPError as http_err:
        return(f'HTTP error occurred: {http_err}')

    except Exception as err:
        return(f'Other error occurred: {err}')
    
    return 0
    