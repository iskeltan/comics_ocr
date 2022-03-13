import re
import json
import requests


def normalize_content(value):
    if value:
        return re.sub("\W+", " ", value).lower()
    return ""


def get_page(url, end_cursor, variables):
    if end_cursor:
        variables["after"] = end_cursor
    url += json.dumps(variables)

    req = requests.get(url)
    return req.json()


def fetch_instagram_photos(profile_id):
    url = 'https://www.instagram.com/graphql/query/?query_hash=d496eb541e5c789274548bf473cc553e&variables='
    variables = {
        "id": profile_id,
        "first": 100
    }
    end_cursor = None
    has_next_page = True
    while True:
        if not has_next_page:
            break
        data = get_page(url, end_cursor, variables)
        has_next_page = \
        data["data"]["user"]["edge_owner_to_timeline_media"]["page_info"][
            "has_next_page"]
        end_cursor = \
        data["data"]["user"]["edge_owner_to_timeline_media"]["page_info"][
            "end_cursor"]

        edges = data["data"]["user"]["edge_owner_to_timeline_media"]["edges"]
        for edge in edges:
            yield edge["node"]["display_url"]