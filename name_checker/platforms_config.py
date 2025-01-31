# platforms_config.py

platforms = {
    "steam": {
        "name": "Steam",
        "checks": [
            {"url": "https://steamcommunity.com/id/{}",
                "detection": "The specified profile could not be found", "method": "GET"},
            {"url": "https://steamid.io/lookup/{}",
                "detection": "profile not found", "method": "GET"}
        ]
    },
    "bluesky": {
        "name": "Bluesky",
        "checks": [
            {"url": "https://public.api.bsky.app/xrpc/com.atproto.identity.resolveHandle?handle={}.bsky.social",
                "detection": "Unable to resolve handle", "method": "GET"}
        ]
    },
    "vrchat": {
        "name": "VRChat",
        "checks": [
            {"url": "https://vrchat.com/api/1/auth/exists?username={}&displayName={}",
                "detection": '{"nameOk":true,"userExists":false}', "method": "GET"}
        ]
    },
    "twitch": {
        "name": "Twitch",
        "checks": [
            {"url": "https://www.twitch.tv/{}",
                "detection": "Sorry. Unless you've got a time machine, that content is unavailable", "method": "GET"}
        ]
    },
    "snapchat": {
        "name": "Snapchat",
        "checks": [
            {"url": "https://www.snapchat.com/add/{}",
                "detection": "This content was not found", "method": "GET"}
        ]
    },
    "soundcloud": {
        "name": "SoundCloud",
        "checks": [
            {"url": "https://api-v2.soundcloud.com/resolve?url=https%3A//soundcloud.com/{}&client_id=meQQRL0IxbE5bGwr7b9pBtluA7WtDzYX&app_version=1737115213&app_locale=en",
                "detection": "{}", "method": "GET"}
        ]
    },
    "apple_music": {
        "name": "Apple Music",
        "checks": [
            {"url": "https://music.apple.com/profile/{}",
                "detection": "The page you're looking for can't be found.", "method": "GET"}
        ]
    },
    "twitter": {
        "name": "twitter",
        "checks": [
            {"url": "https://x.com/{}",
                "detection": "This account doesn’t exist", "method": "GET"}
        ]
    },
    "steam_groups": {
        "name": "Steam Groups",
        "checks": [
            {"url": "https://steamcommunity.com/groups/{}",
                "detection": "No group could be retrieved for the given URL.", "method": "GET"}
        ]
    },
    "youtube": {
        "name": "YouTube",
        "checks": [
            {"url": "https://www.youtube.com/@{}",
                "detection": "error?src=404&amp", "method": "GET"}
        ]
    },
    "instagram": {
        "name": "Instagram",
        "checks": [
            {"url": "https://www.instagram.com/{}",
                "detection": "Sorry, this page isn't available.", "method": "GET"}
        ]
    },
    "minecraft": {
        "name": "Minecraft",
        "checks": [
            {"url": "https://api.mojang.com/users/profiles/minecraft/{}",
                "detection": "Couldn't find any profile with name", "method": "GET"}
        ]
    },
    "github": {
        "name": "Github",
        "checks": [
            {"url": "https://avatars.githubusercontent.com/{}",
                "detection": "Z&BXQ", "method": "GET"},
            {"url": "https://www.github.com/{}",
                "detection": "This is not the web page you are looking for", "method": "GET"}
        ]
    },
    "epic_games": {
        "name": "Epic Games",
        "checks": [
            {"url": "https://fortnitetracker.com/api/v2/fortnite/standard/search?platform=epic&query={}&autocomplete=true",
                "detection": '"data": []', "method": "GET"},
            {"url": "https://api.tracker.gg/api/v2/rocket-league/standard/search?platform=epic&query={}&autocomplete=true",
                "detection": '{"data":[]}', "method": "GET"}
        ]
    },
    "xbox": {
        "name": "Xbox",
        "checks": [
            {"url": "https://xboxgamertag.com/search/{}",
                "detection": "Gamertag doesn't exist", "method": "GET"}
        ]
    },
    "roblox": {
        "name": "Roblox",
        "checks": [
            {"url": "https://auth.roblox.com/v1/usernames/validate?request.username={}&request.birthday=2002-09-09",
                "detection": "Username is valid", "method": "GET"}
        ]
    },
    "pinterest": {
        "name": "Pinterest",
        "checks": [
            {
                "url": "https://pinterest.com/resource/UserResource/get/?source_url=%25{}%2F&data=%7B%22options%22%3A%7B%22field_set_key%22%3A%22profile%22%2C%22username%22%3A%22{}%22%2C%22is_mobile_fork%22%3Atrue%7D%2C%22context%22%3A%7B%7D%7D&_=1640428319046",
                "detection": "User not found.",
                "method": "GET"
            }
        ]
    },
    "telegram": {
        "name": "Telegram",
        "checks": [
            {"url": "https://t.me/{}",
                "detection": '<meta name="robots" content="noindex, nofollow">', "method": "GET"},
            {"url": "https://fragment.com/username/{}",
                "detection": "Unavailable", "method": "GET"}
        ]
    },
    "osu": {
        "name": "Osu",
        "checks": [
            {"url": "https://osu.ppy.sh/users/{}",
                "detection": 'User not found! ;_;', "method": "GET"}
        ]
    },
    "lovense": {
        "name": "Lovense",
        "checks": [
            {"url": "https://www.lovense.com/ajaxCheckIdentityRegisted?identity={}",
                "detection": 'The account does not exist or the password is incorrect, please try again', "method": "POST"}
        ]
    },
    "chesscom": {
        "name": "Chess.com",
        "checks": [
            {"url": "https://www.chess.com/member/{}",
                "detection": '404 Page not found', "method": "GET"}
        ]
    },
    "exit": {
        "name": "Exit",
        "checks": []
    }
}
