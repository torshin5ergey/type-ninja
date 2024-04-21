import requests

def get_random_wikipedia_article():
    url = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
    
    try:
        # GET-request to Wikipedia API
        response = requests.get(url)
        response.raise_for_status()
        # Extract data into JSON
        data = response.json()
        title = data['title']
        content = data['extract']
        return title, content
    except requests.exceptions.RequestException as exc:
        print("Error:", exc)
        return None, None

def get_random_word() -> list[str]:
    url = "https://random-word-api.herokuapp.com/word?number=20"

    try:
        # GET-request to Random word API
        response = requests.get(url)
        response.raise_for_status()
        # Extract data into JSON
        data = response.json()
        return data

    except requests.exceptions.RequestException as exc:
        print("Error:", exc)
        return None, None


if __name__ == "__main__":
    #print(get_random_wikipedia_article())
    print(get_random_word())
    pass