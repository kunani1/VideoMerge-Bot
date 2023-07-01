# (c) @AbirHasan2005

import os


class Config(object):
    API_ID = ""
    API_HASH = ""
    BOT_TOKEN = ""
    SESSION_NAME = "Video-Merge-Bot"
    UPDATES_CHANNEL = ""
    LOG_CHANNEL = ""
    DOWN_PATH = "./downloads"
    TIME_GAP = "5"
    MAX_VIDEOS = "5"
    STREAMTAPE_API_USERNAME = ""
    STREAMTAPE_API_PASS = ""
    MONGODB_URI = ""
    BROADCAST_AS_COPY = ""Falss"
    BOT_OWNER = ""

    START_TEXT = """
Hi Unkil, I am Video Merge Bot!
I can Merge Multiple Videos in One Video. Video Formats should be same.

Made by @AbirHasan2005
"""
    CAPTION = "Video Merged by @{}\n\nMade by @AbirHasan2005"
    PROGRESS = """
Percentage : {0}%
Done: {1}
Total: {2}
Speed: {3}/s
ETA: {4}
"""
