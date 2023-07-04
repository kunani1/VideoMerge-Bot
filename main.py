# (c) @AbirHasan2005
# This is a very simple Telegram Videos Merge Bot.
# Coded by a Nub.
# Don't laugh seeing the codes.
# Me learning.

import os
import time
import string
import shutil
import psutil
import random
import asyncio
from PIL import Image
from configs import Config
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery, InputMediaPhoto
from pyrogram.raw.functions.account import UpdateProfile

from helpers.markup_maker import MakeButtons
from helpers.streamtape import UploadToStreamtape
from helpers.clean import delete_all
from hachoir.parser import createParser
from helpers.check_gap import CheckTimeGap
from helpers.database.access_db import db
from helpers.database.add_user import AddUserToDatabase
from helpers.uploader import UploadVideo
from helpers.settings import OpenSettings
from helpers.forcesub import ForceSub
from hachoir.metadata import extractMetadata
from helpers.display_progress import progress_for_pyrogram, humanbytes
from helpers.broadcast import broadcast_handler
from helpers.ffmpeg import MergeVideo, generate_screen_shots, cult_small_video
from asyncio.exceptions import TimeoutError
from pyrogram.errors import FloodWait, UserNotParticipant, MessageNotModified

QueueDB = {}
ReplyDB = {}
FormtDB = {}

NubBot = Client(
    session_name=Config.SESSION_NAME,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)


@NubBot.on_message(filters.private & filters.command("start"))
async def start_handler(_, m: Message):
    await AddUserToDatabase(m)
    Fsub = await ForceSub(m)
    if Fsub == 400:
        return
    await m.reply_text(
        text=Config.START_TEXT,
        disable_web_page_preview=True,
        quote=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Developer - @AbirHasan2005", url="https://t.me/AbirHasan2005")],
                [InlineKeyboardButton("Support Group", url="https://t.me/linux_repo"),
                 InlineKeyboardButton("Bots Channel", url="https://t.me/Discovery_Updates")],
                [InlineKeyboardButton("Open Settings", callback_data="openSettings")],
                [InlineKeyboardButton("Close", callback_data="closeMeh")]
            ]
        )
    )


@NubBot.on_message(filters.private & (filters.video | filters.document) & ~filters.edited)
async def videos_handler(_, m: Message):
    await AddUserToDatabase(m)
    Fsub = await ForceSub(m)
    if Fsub == 400:
        return
    media = m.video or m.document
    if media.file_name is None:
        await m.reply_text("File Name Not Found!")
        return
    if media.file_name.rsplit(".", 1)[-1].lower() not in ["mp4", "mkv", "webm"]:
        await m.reply_text("This Video Format not Allowed!\nOnly send MP4 or MKV or WEBM.", quote=True)
        return
    if QueueDB.get(m.from_user.id) is None:
        FormtDB.update({m.from_user.id: media.file_name.rsplit(".", 1)[-1].lower()})
    
