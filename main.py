import asyncpraw
import discord
import os
from discord.ext import tasks, commands
from time import time, sleep
import asyncio

#bot intents
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='>', intents=intents)

async def getsubmissions(subreddit):
  
  #Filter the posts
  hot_mtg = subreddit.hot(limit=30)
  async for submission in hot_mtg:
    if submission.link_flair_text == 'Spoiler':
      await process_submission(submission)

async def process_submission(submission):

  identifier = "["
  if identifier not in submission.title:
    return
  
  
  # Ignore posts that have already been posted, checks the log file if the
  # post is in it. Will add it to this log file if it hasn't.
  with open('log.txt') as x:
    if f"{submission}" in x.read():
      return
  #calculate like-ratio percentage
  likeratio = str(int(submission.upvote_ratio * 100)) + '%'

  #Add new posts to the log so they don't get posted again.
  with open('log.txt', "a", encoding="utf-8") as f:
    f.write(f"{submission}\n")
  channel = bot.get_channel("Channel Number Here")
  await channel.send(f'{submission.title} has a upvote ratio of {likeratio} , {submission.url}')
  await asyncio.sleep(120)

@tasks.loop(minutes=15.0)
async def startup():
  reddit = asyncpraw.Reddit(
    client_id= 'client ID here',
    client_secret = 'client secret ID here',
    user_agent= 'Magic The Gathering Spoiler Grabber v.1'
  )
  channel = bot.get_channel("Channel Number here")
  #Select your subreddit
  subreddit = await reddit.subreddit('MagicTCG')
  await getsubmissions(subreddit)


@bot.event
async def on_ready():
  startup.start()

bot.run('Bot Code Here')
