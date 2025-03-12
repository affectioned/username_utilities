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
        "name": "Twitter",
        "checks": [
            {"url": "https://nitter.net/{}",
                "detection": "not found</span>", "method": "GET"}
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
            {"url": "https://youtube.com/@{}",
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
                "url": "https://www.pinterest.com/{}",
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
            {
                "url": "https://www.lovense.com/ajaxCheckIdentityRegisted",
                "method": "POST",
                "data": {"identity": "{}"},
                "detection": "The account does not exist or the password is incorrect, please try again"
            }
        ]
    },
    "chesscom": {
        "name": "Chess.com",
        "checks": [
            {
                "url": "https://www.chess.com/member/{}",
                "method": "GET",
                "detection": "404 Page not found"
            }
        ]
    },
    "discord": {
        "name": "Discord",
        "checks": [
            {
                "url": "https://discord.com/api/v9/unique-username/username-attempt-unauthed",
                "method": "POST",
                "json": {"username": "{}"},
                "detection": "'taken': False"
            }
        ]
    },
    "paypal": {
        "name": "Paypal Me",
        "checks": [
            {
                "url": "https://paypal.me/{}?locale.x=en_US",
                "method": "GET",
                "detection": '<meta name="twitter:title" content="Get your very own PayPal.Me link" />'
            }
        ]
    },
    "ubisoft": {
        "name": "Ubisoft",
        "checks": [
            {
                "url": "https://api.tracker.gg/api/v2/r6siege/standard/search?platform=ubi&query={}&autocomplete=true",
                "method": "GET",
                "detection": '{"data":[]}'
            }
        ]
    },
    "throne": {
        "name": "Throne",
        "checks": [
            {
                "url": "https://throne.com/{}",
                "method": "GET",
                "detection": 'Creator not found'
            }
        ]
    },
    "booth_pm": {
        "name": "Booth.pm",
        "checks": [
            {
                "url": "https://{}.booth.pm/",
                "method": "GET",
                "detection": 'content="website">'
            }
        ]
    },
    "lastfm": {
        "name": "Last.fm",
        "checks": [
            {
                "url": "https://www.last.fm/user/{}",
                "method": "GET",
                "detection": '404 - Page Not Found'
            }
        ]
    },
    "nightlightgg": {
        "name": "nightlight.gg",
        "checks": [
            {
                "url": "https://nightlight.gg/u/{}/stats",
                "method": "GET",
                "detection": "This profile doesn't seem to exist, are you sure you've got the right username?"
            }
        ]
    },
    "exit": {
        "name": "Exit",
        "checks": []
    }
}
