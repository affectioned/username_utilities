# platforms_config.py

platforms = {
    "steam": {
        "name": "Steam",
        "checks": [
            {"url": "https://steamcommunity.com/id/{}", "detection": "The specified profile could not be found"},
             {"url": "https://steamid.io/lookup/{}", "detection": "profile not found"}
        ]
    },
    "bluesky": {
        "name": "Bluesky",
        "checks": [
            {"url": "https://public.api.bsky.app/xrpc/com.atproto.identity.resolveHandle?handle={}.bsky.social", "detection": "Unable to resolve handle"}
        ]
    },
    "vrchat": {
        "name": "VRChat",
        "checks": [
            {"url": "https://vrchat.com/api/1/auth/exists?username={}&displayName={}&excludeUserId=usr_f8e5f44a-bc1a-4aeb-b426-f849b8e5dcb0", "detection": '{"nameOk":true,"userExists":false}'}
        ]
    },
    "twitch": {
        "name": "Twitch",
        "checks": [
            {"url": "https://www.twitch.tv/{}", "detection": "Sorry. Unless you've got a time machine, that content is unavailable"}
        ]
    },
    "snapchat": {
        "name": "Snapchat",
        "checks": [
            {"url": "https://www.snapchat.com/add/{}", "detection": "This content was not found"}
        ]
    },
    "soundcloud": {
        "name": "SoundCloud",
        "checks": [
            {"url": "https://soundcloud.com/{}", "detection": "We can’t find that user."}
        ]
    },
    "apple_music": {
        "name": "Apple Music",
        "checks": [
            {"url": "https://music.apple.com/profile/{}", "detection": "The page you're looking for can't be found."}
        ]
    },
    "twitter": {
        "name": "twitter",
        "checks": [
            {"url": "https://x.com/{}", "detection": "This account doesn’t exist"}
        ]
    },
    "steam_groups": {
        "name": "Steam Groups",
        "checks": [
            {"url": "https://steamcommunity.com/groups/{}", "detection": "No group could be retrieved for the given URL."}
        ]
    },
    "youtube": {
        "name": "YouTube",
        "checks": [
            {"url": "https://www.youtube.com/@{}", "detection": "error?src=404&amp"}
        ]
    },
    "instagram": {
        "name": "Instagram",
        "checks": [
            {"url": "https://www.instagram.com/{}", "detection": '"desktop_show_sign_up_as_primary_cta": false'}
        ]
    },
    "minecraft": {
        "name": "Minecraft",
        "checks": [
            {"url": "https://api.mojang.com/users/profiles/minecraft/{}", "detection": "Couldn't find any profile with name"}
        ]
    },
    "github": {
        "name": "Github",
        "checks": [
            {"url": "https://www.github.com/{}", "detection": "This is not the web page you are looking for"}
        ]
    },
    "epic_games": {
        "name": "Epic Games (Fortnite)",
        "checks": [
            {"url": "https://fortnitetracker.com/profile/all/{}", "detection": "404 Not Found. We are unable to find your profile."}
        ]
    },
    "xbox": {
        "name": "Xbox",
        "checks": [
            {"url": "https://xboxgamertag.com/search/{}", "detection": "Gamertag doesn't exist"}
        ]
    },
    "roblox": {
        "name": "Roblox",
        "checks": [
            {"url": "https://auth.roblox.com/v1/usernames/validate?request.username={}&request.birthday=2002-09-09", "detection": "Username is valid"}
        ]
    },
    "pinterest": {
        "name": "Pinterest",
        "checks": [
            {"url": "https://www.pinterest.com/{}", "detection": '!--><template id="B:0"></template><!--/$--><!--$--><title></title'}
        ]
    },
    "telegram": {
        "name": "Telegram",
        "checks": [
            {"url": "https://t.me/{}", "detection": '<meta name="robots" content="noindex, nofollow">'},
            {"url": "https://fragment.com/username/{}", "detection": "Unavailable"}
        ]
    },
    "exit": {
        "name": "Exit",
        "checks": []
    }
}