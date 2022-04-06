#hi this is the cutest slot huehuehueimport discord
# xD
import os
from datetime import datetime,timedelta
import pendulum
import threading
from requests_html import AsyncHTMLSession
import discord

from discord.ext import commands

#Secrets
TOKEN = os.environ['TOKEN']

intents = discord.Intents.all()
client = discord.Client(intents=intents,
                        activity=discord.Game(name='Pirate King Online'))
bot = commands.Bot(command_prefix='!')

utc = pendulum.timezone('UTC')
now = datetime.now(utc)


asession = AsyncHTMLSession()

#link gp sheet
url3 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQz_TOawRjAmJLLQ4qjwrH3Y6YV3zeOuyWuzdtau8ZFdtEb8CPSC0iEjf6i7IMUeq1oltW90pnqRPRk/pubhtml?gid=1349973443&single=true"

#asession = AsyncHTMLSession()
async def PointsExcel():
  rc = await asession.get(url3)
  #await rc.html.arender()
  return rc  #TODO: Find a way to keep repeating this

thepointsheet = []
pointsitems = []
pointsdata = []

#HORA QUE COMEÇA
event_exp_start = ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']

#semana 1
event_exp_start[0] = datetime.fromisoformat('2022-03-20 11:00:00')
event_exp_start[1] = datetime.fromisoformat('2022-03-20 16:00:00')
event_exp_start[2] = datetime.fromisoformat('2022-03-21 02:00:00')
event_exp_start[3] = datetime.fromisoformat('2022-03-21 13:00:00')
event_exp_start[4] = datetime.fromisoformat('2022-03-22 07:00:00')
event_exp_start[5] = datetime.fromisoformat('2022-03-22 17:00:00')
event_exp_start[6] = datetime.fromisoformat('2022-03-23 05:00:00')
event_exp_start[7] = datetime.fromisoformat('2022-03-23 18:00:00')
event_exp_start[9] = datetime.fromisoformat('2022-03-24 19:00:00')
event_exp_start[8] = datetime.fromisoformat('2022-03-24 09:00:00')
event_exp_start[10] = datetime.fromisoformat('2022-03-25 02:00:00')
event_exp_start[11] = datetime.fromisoformat('2022-03-25 20:00:00')
event_exp_start[12] = datetime.fromisoformat('2022-03-26 04:00:00')
event_exp_start[13] = datetime.fromisoformat('2022-03-26 14:00:00')

#semana 2
event_exp_start[14] = datetime.fromisoformat('2022-03-27 04:00:00')
event_exp_start[15] = datetime.fromisoformat('2022-03-27 14:00:00')
event_exp_start[16] = datetime.fromisoformat('2022-03-28 05:00:00')
event_exp_start[17] = datetime.fromisoformat('2022-03-28 15:00:00')
event_exp_start[18] = datetime.fromisoformat('2022-03-29 06:00:00')
event_exp_start[19] = datetime.fromisoformat('2022-03-29 16:00:00')
event_exp_start[20] = datetime.fromisoformat('2022-03-30 07:00:00')
event_exp_start[21] = datetime.fromisoformat('2022-03-30 17:00:00')
event_exp_start[22] = datetime.fromisoformat('2022-03-31 08:00:00')
event_exp_start[23] = datetime.fromisoformat('2022-03-31 18:00:00')
event_exp_start[24] = datetime.fromisoformat('2022-04-01 09:00:00')
event_exp_start[25] = datetime.fromisoformat('2022-04-01 19:00:00')
event_exp_start[26] = datetime.fromisoformat('2022-04-02 02:00:00')
event_exp_start[27] = datetime.fromisoformat('2022-04-02 20:00:00')

#semana 3
event_exp_start[28] = datetime.fromisoformat('2022-04-03 05:00:00')
event_exp_start[29] = datetime.fromisoformat('2022-04-03 10:00:00')
event_exp_start[30] = datetime.fromisoformat('2022-04-04 03:00:00')
event_exp_start[31] = datetime.fromisoformat('2022-04-04 14:00:00')
event_exp_start[32] = datetime.fromisoformat('2022-04-05 07:00:00')
event_exp_start[33] = datetime.fromisoformat('2022-04-05 16:00:00')
event_exp_start[34] = datetime.fromisoformat('2022-04-06 04:00:00')
event_exp_start[35] = datetime.fromisoformat('2022-04-06 17:00:00')
event_exp_start[36] = datetime.fromisoformat('2022-04-07 09:00:00')
event_exp_start[37] = datetime.fromisoformat('2022-04-07 15:00:00')
event_exp_start[38] = datetime.fromisoformat('2022-04-08 06:00:00')
event_exp_start[39] = datetime.fromisoformat('2022-04-08 09:00:00')
event_exp_start[40] = datetime.fromisoformat('2022-04-09 11:00:00')
event_exp_start[41] = datetime.fromisoformat('2022-04-09 14:00:00')

#semana 4
event_exp_start[42] = datetime.fromisoformat('2022-04-10 04:00:00')
event_exp_start[43] = datetime.fromisoformat('2022-04-10 20:00:00')
event_exp_start[44] = datetime.fromisoformat('2022-04-11 05:00:00')
event_exp_start[45] = datetime.fromisoformat('2022-04-11 15:00:00')
event_exp_start[46] = datetime.fromisoformat('2022-04-12 07:00:00')
event_exp_start[47] = datetime.fromisoformat('2022-04-12 16:00:00')
event_exp_start[48] = datetime.fromisoformat('2022-04-13 04:00:00')
event_exp_start[49] = datetime.fromisoformat('2022-04-13 17:00:00')
event_exp_start[50] = datetime.fromisoformat('2022-04-14 07:00:00')
event_exp_start[51] = datetime.fromisoformat('2022-04-14 17:00:00')
event_exp_start[52] = datetime.fromisoformat('2022-04-15 10:00:00')
event_exp_start[53] = datetime.fromisoformat('2022-04-15 18:00:00')
event_exp_start[54] = datetime.fromisoformat('2022-04-16 08:00:00')
event_exp_start[55] = datetime.fromisoformat('2022-04-16 22:00:00')
      
      
#Tempo de evento
event_exp_duration = ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']
#semana 1
event_exp_duration[0] = timedelta(hours = 2, minutes = 30)
event_exp_duration[1] = timedelta(hours = 2, minutes = 30)
event_exp_duration[2] = timedelta(hours = 2, minutes = 30)
event_exp_duration[3] = timedelta(hours = 2, minutes = 30)
event_exp_duration[4] = timedelta(hours = 2, minutes = 30)
event_exp_duration[5] = timedelta(hours = 2, minutes = 30)
event_exp_duration[6] = timedelta(hours = 3, minutes = 00)
event_exp_duration[7] = timedelta(hours = 3, minutes = 00)
event_exp_duration[8] = timedelta(hours = 2, minutes = 00)
event_exp_duration[9] = timedelta(hours = 2, minutes = 00)
event_exp_duration[10] = timedelta(hours = 1, minutes = 30)
event_exp_duration[11] = timedelta(hours = 1, minutes = 30)
event_exp_duration[12] = timedelta(hours = 1, minutes = 30)
event_exp_duration[13] = timedelta(hours = 1, minutes = 30)

#semana 2
event_exp_duration[14] = timedelta(hours = 1, minutes = 30)
event_exp_duration[15] = timedelta(hours = 1, minutes = 30)
event_exp_duration[16] = timedelta(hours = 2, minutes = 00)
event_exp_duration[17] = timedelta(hours = 2, minutes = 00)
event_exp_duration[18] = timedelta(hours = 2, minutes = 30)
event_exp_duration[19] = timedelta(hours = 2, minutes = 30)
event_exp_duration[20] = timedelta(hours = 1, minutes = 30)
event_exp_duration[21] = timedelta(hours = 1, minutes = 30)
event_exp_duration[22] = timedelta(hours = 1, minutes = 00)
event_exp_duration[23] = timedelta(hours = 1, minutes = 00)
event_exp_duration[24] = timedelta(hours = 2, minutes = 00)
event_exp_duration[25] = timedelta(hours = 2, minutes = 00)
event_exp_duration[26] = timedelta(hours = 1, minutes = 30)
event_exp_duration[27] = timedelta(hours = 1, minutes = 30)

#semana 3
event_exp_duration[28] = timedelta(hours = 1, minutes = 30)
event_exp_duration[29] = timedelta(hours = 1, minutes = 30)
event_exp_duration[30] = timedelta(hours = 2, minutes = 00)
event_exp_duration[31] = timedelta(hours = 2, minutes = 00)
event_exp_duration[32] = timedelta(hours = 3, minutes = 00)
event_exp_duration[33] = timedelta(hours = 3, minutes = 00)
event_exp_duration[34] = timedelta(hours = 1, minutes = 30)
event_exp_duration[35] = timedelta(hours = 1, minutes = 30)
event_exp_duration[36] = timedelta(hours = 2, minutes = 00)
event_exp_duration[37] = timedelta(hours = 2, minutes = 00)
event_exp_duration[38] = timedelta(hours = 2, minutes = 00)
event_exp_duration[39] = timedelta(hours = 2, minutes = 00)
event_exp_duration[40] = timedelta(hours = 1, minutes = 30)
event_exp_duration[41] = timedelta(hours = 1, minutes = 30)

#semana 4
event_exp_duration[42] = timedelta(hours = 2, minutes = 30)
event_exp_duration[43] = timedelta(hours = 2, minutes = 30)
event_exp_duration[44] = timedelta(hours = 2, minutes = 30)
event_exp_duration[45] = timedelta(hours = 2, minutes = 30)
event_exp_duration[46] = timedelta(hours = 1, minutes = 30)
event_exp_duration[47] = timedelta(hours = 1, minutes = 30)
event_exp_duration[48] = timedelta(hours = 1, minutes = 00)
event_exp_duration[49] = timedelta(hours = 1, minutes = 00)
event_exp_duration[50] = timedelta(hours = 3, minutes = 00)
event_exp_duration[51] = timedelta(hours = 3, minutes = 00)
event_exp_duration[52] = timedelta(hours = 1, minutes = 30)
event_exp_duration[53] = timedelta(hours = 1, minutes = 30)
event_exp_duration[54] = timedelta(hours = 2, minutes = 00)
event_exp_duration[55] = timedelta(hours = 2, minutes = 00)


#Tipo do evento
event_exp_style = ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']
#semana 1
event_exp_style[0] = "1.5/2X EXP/Fairy"
event_exp_style[1] = "1.5/2X EXP/Fairy"
event_exp_style[2] = "1.5/2X EXP/Fairy"
event_exp_style[3] = "1.5/2X EXP/Fairy"
event_exp_style[4] = "1.5/2X EXP/Fairy"
event_exp_style[5] = "1.5/2X EXP/Fairy"
event_exp_style[6] = "1.5/2X EXP/Fairy"
event_exp_style[7] = "1.5/2X EXP/Fairy"
event_exp_style[8] = "1.5/2X EXP/Fairy"
event_exp_style[9] = "1.5/2X EXP/Fairy"
event_exp_style[10] = "1.5/2X EXP/Fairy"
event_exp_style[11] = "1.5/2X EXP/Fairy"
event_exp_style[12] = "1.5/2X EXP/Fairy"
event_exp_style[13] = "1.5/2X EXP/Fairy"

#semana 2
event_exp_style[14] = "1.5/2X EXP/Drop"
event_exp_style[15] = "1.5/2X EXP/Drop"
event_exp_style[16] = "1.5/2X EXP/Drop"
event_exp_style[17] = "1.5/2X EXP/Drop"
event_exp_style[18] = "2X/2X EXP/Drop"
event_exp_style[19] = "2X/2X EXP/Drop"
event_exp_style[20] = "2X/2X EXP/Drop"
event_exp_style[21] = "2X/2X EXP/Drop"
event_exp_style[22] = "2X/2X EXP/Drop"
event_exp_style[23] = "2X/2X EXP/Drop"
event_exp_style[24] = "1.5/2X EXP/Drop"
event_exp_style[25] = "1.5/2X EXP/Drop"
event_exp_style[26] = "1.5/2X EXP/Drop"
event_exp_style[27] = "1.5/2X EXP/Drop"


#semana 3
event_exp_style[28] = "2/2X Resource/Drop"
event_exp_style[29] = "2/2X Resource/Drop"
event_exp_style[30] = "1.5/2X Resource/Drop"
event_exp_style[31] = "1.5/2X Resource/Drop"
event_exp_style[32] = "2/2X Resource/Drop"
event_exp_style[33] = "2/2X Resource/Drop"
event_exp_style[34] = "2/2X Resource/Drop"
event_exp_style[35] = "2/2X Resource/Drop"
event_exp_style[36] = "1.5/2X Resource/Drop"
event_exp_style[37] = "1.5/2X Resource/Drop"
event_exp_style[38] = "1.5/2X Resource/Drop"
event_exp_style[39] = "1.5/2X Resource/Drop"
event_exp_style[40] = "2/2X Resource/Drop"
event_exp_style[41] = "1.5/2X Resource/Drop"

#semana 4
event_exp_style[42] = "2/1.5X Resource/EXP"
event_exp_style[43] = "2/1.5X Resource/EXP"
event_exp_style[44] = "2/1.5X Resource/EXP"
event_exp_style[45] = "2/1.5X Resource/EXP"
event_exp_style[46] = "2/1.5X Resource/EXP"
event_exp_style[47] = "2/1.5X Resource/EXP"
event_exp_style[48] = "2/1.5X Resource/EXP"
event_exp_style[49] = "2/1.5X Resource/EXP"
event_exp_style[50] = "2/1.5X Resource/EXP"
event_exp_style[51] = "2/1.5X Resource/EXP"
event_exp_style[52] = "2/1.5X Resource/EXP"
event_exp_style[53] = "2/1.5X Resource/EXP"
event_exp_style[54] = "2/1.5X Resource/EXP"
event_exp_style[55] = "2/1.5X Resource/EXP"

def eventduration(tempo):
    durationtotal = tempo.total_seconds()
    days, remainder = divmod(durationtotal, 86400)
    hours, remaindermin = divmod(remainder, 3600)
    minutes, seconds = divmod(remaindermin, 60)
    if (hours > 0):
      duration = ('{:02}h {:02}m'.format(int(hours), int(minutes)))
    else:
      duration = ('{:02}m'.format(int(minutes)))

    return duration


def repeat():
    global now
    threading.Timer(1.0, repeat).start()  # called every second
    now = datetime.now(utc)

repeat()

@client.event
async def on_ready():
    global pointsdata
    global thepointsheet

    thepointsheet = await PointsExcel()
    #pointsitems = [element.text for element in thepointsheet.html.find('.s2')]
    pointsdata = [element.text for element in thepointsheet.html.find('.s4')]
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    #variables
    channel = message.channel
    content = message.content.lower()

    #global pointsitems
    global pointsdata
    global thepointsheet


    #global event timers
    global event_exp_start
    global event_exp_duration
  
    #bot cant trigger own commands
    if message.author == client.user:
        return

    '''
    #private message command
    if message.content.startswith('/private'):
        if message.author.guild_permissions.administrator == True or message.author.id == 307640466638110721:
            text = message.content[len('/private'):]
            for member in guild.members:
                try:
                    await member.send(text)
                except Exception:
                    print(guild.get_member(member.id).display_name)
                    pass
    '''

    """
    SHARE SHEET COMMANDS
    """

    if content.startswith('.sheet') or content.startswith('!sheet'):
      await channel.send('https://docs.google.com/spreadsheets/d/1q7bbrm7cVyO-XtLhoP8yDJ2ZJwSUV34rR5WFacLFcas/edit?usp=sharing')


    #command for make list
    if content.startswith('.points'):
        pointsname = content[len('.points'):].strip()
            
        if pointsname == 'update':

            thepointsheet = await PointsExcel()

            pointsdata = [element.text for element in thepointsheet.html.find('.s4')]

            try:
              await message.delete()
            except Exception:
              pass

        elif pointsname.startswith("<@"):
            discordid = pointsname.replace("!", "")
            usergp = 'No GP/BD Data'

            for item in ("".join(pointsdata)).split("."):
                if discordid in item:
                    usergp = item.split(">")[1]

            await channel.send(usergp, delete_after=15)
          
            await message.delete(delay=1)
          
            #try:
            #  await message.delete(delay=1)
            #except Exception:
            #  pass

        else:
            await channel.send(
                "invalid syntax. Use command: `.points @user`"
            )

    if content.startswith('!points'):
          await channel.send(
              "invalid syntax. Use command: `.points @user`"
          )

	#command for make list
    if content.startswith('.list'):

      await message.delete(delay=1)
      
      if message.author.voice and message.author.voice.channel:
        voice_channel = message.author.voice.channel
      else:
        await channel.send("You are not connected to a voice channel", delete_after=5)
        return

      count = 0
      
      ca_members = voice_channel.members
      memids = []  #(list)
      for member in ca_members:
        if not member.bot:
          memids.append(member.id)
        list_members = ""

      list_header = (f"**MAZE LIST**\n\n"
                        f"**----MEMBERS----**\n\n")
      
      list_drops = (f"\n**----DROPS----**\n")

      for i in range(len(memids)):  #insert voice ppl in list
        list_members = list_members + message.guild.get_member(memids[i]).display_name + "\n"
        count = count + 1

      count_msg = f"\n**" + str(count) + " MEMBERS IN VOICE.**"
      final_msg = (f"\n**This is just a model. Make a copy of this list and after that delete this message.**")
      
      ca_list = list_header + list_members + list_drops + count_msg + final_msg
      await channel.send(ca_list)  #send the list complete in one message



  
    if content.startswith('.event'):

      nextevent = 0
      status_event = 1 # 1=happening , 2=later
      eventtimeutc = ['','','','','']
      stringeventtimeutc = ['','','','','']
      
      for x in range(len(event_exp_start)):
        if(event_exp_start[nextevent].replace(tzinfo=utc) - now < timedelta(seconds=1) and (event_exp_start[nextevent]+event_exp_duration[nextevent]).replace(tzinfo=utc) - now < timedelta(seconds=1)):
          nextevent = nextevent + 1
          
        elif(event_exp_start[nextevent].replace(tzinfo=utc) - now < timedelta(seconds=1) and (event_exp_start[nextevent]+event_exp_duration[nextevent]).replace(tzinfo=utc) - now > timedelta(seconds=1)):
          #print("Happening event n. " + str(nextevent))
          status_event = 1
          break
        else:
          status_event = 2
          #print("Next event is n. " + str(nextevent))
          break

      if(status_event == 1):
        end_time = (event_exp_start[nextevent] + event_exp_duration[nextevent]).replace(tzinfo=utc)
        missing_time = end_time - now
      if(status_event == 2): 
        start_time = event_exp_start[nextevent].replace(tzinfo=utc)
        missing_time = start_time - now
      
      if (content.find('+') != -1):
          userutc = content.partition('+')[2]
          userutc = '+' + userutc
      elif (content.find('-') != -1):
          userutc = content.partition('-')[2]
          userutc = '-' + userutc
      else:
          userutc = '+0'

      missing_timefloat = missing_time.total_seconds()
      days, remainder = divmod(missing_timefloat, 86400)
      hours, remaindermin = divmod(remainder, 3600)
      minutes, seconds = divmod(remaindermin, 60)
      if (hours > 0):
        msg2 = ('**{:02}h {:02}m {:02}s**'.format(int(hours), int(minutes), int(seconds)))
      else:
        msg2 = ('**{:02}m {:02}s**'.format(int(minutes), int(seconds)))

      duration = eventduration(event_exp_duration[nextevent])
      event_style = event_exp_style[nextevent]

      #if(content[len('.event'):].strip() == 'list'):
      if 'list' in content:
        for x in range(5):
          try:
            eventtimeutc[x] = event_exp_start[nextevent + x].replace(tzinfo=utc) + timedelta(hours=int(userutc))
            stringeventtimeutc[x] = eventtimeutc[x].strftime('%A, %B %d | **%H:%M')
          except Exception:
            eventtimeutc[x] = ''
            stringeventtimeutc[x] = ''

        if (userutc == '+0'):
          userutc = ''

        if(status_event == 1):
          ishappening = '**(EVENT HAPPENING)** '
        elif(status_event == 2):
          ishappening = ''

        event_text = ['','','','','']
        
        event_text[0] = ishappening + stringeventtimeutc[0] + userutc + ' UTC Timezone**' + ' @ **Duration:** ' + eventduration(event_exp_duration[nextevent]) + ' | **' + event_exp_style[nextevent] + '**\n'
        
        for x in range(1,5):
          try:
            event_text[x] = stringeventtimeutc[x] + userutc + ' UTC Timezone**' + ' @ **Duration:** ' + eventduration(event_exp_duration[nextevent + x]) + ' | **' + event_exp_style[nextevent + x] + '**\n'
          except Exception:
            event_text[x] = ''
        
        await channel.send('**Next 5 events at ' + userutc + ' UTC timezone will be at:**\n\n' + event_text[0] + event_text[1] + event_text[2] + event_text[3] + event_text[4])
        return
      
      if(status_event == 1): 
          eventtimeutc = end_time + timedelta(hours=int(userutc))
          stringeventtimeutc = eventtimeutc.strftime('%A, %B %d | **%H:%M')
          if (userutc == '+0'):
              userutc = ''
          await channel.send('Event will end in ' + msg2 + '\n' + '**Duration:** ' + duration + ' | **' + event_style + '**\n' + stringeventtimeutc + ' ' + userutc + ' UTC Timezone.**')
        
      if(status_event == 2): 
          eventtimeutc = start_time + timedelta(hours=int(userutc))
          stringeventtimeutc = eventtimeutc.strftime('%A, %B %d | **%H:%M')
          if (userutc == '+0'):
              userutc = ''
          await channel.send('Next event will be in ' + msg2 + '\n' + '**Duration:** ' + duration + ' | **' + event_style + '**\n' + stringeventtimeutc + ' ' + userutc + ' UTC Timezone.**')


try:
  client.run(TOKEN)
except discord.errors.HTTPException:
  print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")