import json
import requests
from datetime import datetime


def is_json(myjson_string):
    """
    Checks if a string is valid JSON.

    Args:
        myjson_string: The string to check.

    Returns:
        True if the string is valid JSON, False otherwise.
    """
    try:
        json.loads(myjson_string)
    except json.JSONDecodeError:
        return False
    except TypeError:
        return False
    return True


today_dt = datetime.today()
bein_sport_format_date = today_dt.strftime("%Y%m%d")
url_format_date = today_dt.strftime("%Y-%m-%d")


url = f"https://prod-cmseventmanagement.beinsports.com/w2w/getWatch?type=page&page=1&pageLimit=100&desiredLanguage=en-mena&isLive=100&eventDate={url_format_date}&eventTime=00%3A00%3A00&sport=soccer_data&comp_id=&team_id="


headers = {
    "accept": "application/json",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9,ar;q=0.8,fr;q=0.7",
    "cache-control": "no-cache",
    "origin": "https://www.beinsports.com",
    "pragma": "no-cache",
    "referer": "https://www.beinsports.com/",
    "sec-ch-ua": '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
}

response = requests.get(url, headers=headers)


if is_json(response.text):
    data = response.json()

    result = data["result"][bein_sport_format_date]
    today_matches = []
    bein_sport_media_url = "https://prod-media.beinsports.com/image/{}.png"
    # repo_url = "https://gitlab.com/sportism/sportism-backend"
    # servers_base_url = "{}/-/raw/main/channels-streaming-urls/{}.json?ref_type=heads"

    repo_url = "https://raw.githubusercontent.com/sportism/sportism-hidden-api"
    servers_base_url = "{}/refs/heads/main/channels-streaming-urls/{}.json"

    def channel_name_convertor(channe_name: str) -> str:
        return "-".join(channe_name.lower().split())

    unsupported_channels = ["xtra", "max", "en", "fr"]

    # print(json.dumps(result))

    for i, obj in enumerate(result):
        match = {
            # "eventExternalId": "2486593803668",
            # "eventTitle": "Al-Wakrah vs Al Ahli",
            # "eventDateTime": "2026-02-06T14:35:00.000Z",
            # "eventEndDateTime": "2026-02-06T16:45:00.000Z",
            # "sport": "soccer_data",
            #
            # "channelRedirectUrl": "https://beinconnect.app/beINSPORTS3",
            # "description": "Al Wakrah vs Al Ahli",
            # "homeTeamName": "Wakrah",
            # "awayTeamName": "Ahli",
            # "homeTeamCode": "WAK",
            # "awayTeamCode": "AHL",
            #
            # "motosportsData": "",
            # "localDateTime": "2026-02-06T15:35:00.000Z"
            #
            "category": obj["category"],
            #
            "channelName": obj["channelName"],
            "channelExternalId": "94130ea17023c4837f0dcdda95034b65",
            "channelLogo": bein_sport_media_url.format(obj["channelExternalId"]),
            "channelServers": servers_base_url.format(
                repo_url, channel_name_convertor(obj["channelName"])
            ),
            #
            "competitionName": obj["competitionName"],
            "competitionOptaId": obj["competitionOptaId"],
            "competitionLogo": bein_sport_media_url.format(obj["competitionOptaId"]),
            "matchOptaId": obj["matchOptaId"],
            #
            "homeTeamOptaId": obj["homeTeamOptaId"],
            "homeTeamColor": obj["homeTeamColor"],
            "homeTeamfullName": obj["homeTeamfullName"],
            "homeTeamLogo": bein_sport_media_url.format(obj["homeTeamOptaId"]),
            #
            "awayTeamOptaId": obj["awayTeamOptaId"],
            "awayTeamColor": obj["awayTeamColor"],
            "awayTeamfullName": obj["awayTeamfullName"],
            "awayTeamLogo": bein_sport_media_url.format(obj["awayTeamOptaId"]),
            #
            "round": "Regular Season",
            "matchDate": obj["matchDate"],
            "matchTime": obj["matchTime"],
        }

        channel_name = match["channelName"].lower()
        is_match_broadcating_on_supporting_channel = (
            not any(
                channel_suffix in channel_name
                for channel_suffix in unsupported_channels
            )
            and "bein sports" in channel_name
        )

        if is_match_broadcating_on_supporting_channel:
            today_matches.append(match)

    with open("../data/live-events.json", "w") as file:
        json.dump(today_matches, file)

    print(json.dumps(today_matches))
else:
    print("response is not valid (is not json)")
