import discord
import os
from requests_html import AsyncHTMLSession
import pendulum
import asyncio
from datetime import datetime, timedelta, time, date
import re
from bs4 import BeautifulSoup
import webparameters
import eventlist
import usersdata

# as per recommendation from @freylis, compile once only
CLEANR = re.compile('<.*?>') 

def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext

utc = pendulum.timezone('UTC')
now = datetime.now(utc)

from discord.ext import commands

#google sheets reader

#Secrets
TOKEN = os.environ['TOKEN']

intents = discord.Intents.all()
client = discord.Client(intents=intents,
                        activity=discord.Game(name='Pirate King Online'))
bot = commands.Bot(command_prefix='!')

#I edited this for the lulz just to add it for now - Luisa
#Shiba Inu copy bot ~ Luisa
url = "https://pirateking.online/database/portal"
asession = AsyncHTMLSession()
async def get_timers():
  r = await asession.get(url)
  await r.html.arender()
  return r

"""
BEGGINING OF TIMERS FUNCTIONS
"""

maze_timer = []
BD1_Time = datetime.now(utc)
BD1_Status1 = []
BD2_Time = datetime.now(utc)
BD2_Status1 = []

def get_user_utc(content):
  if (content.find('+') != -1):
    userutc = content.partition('+')[2]
    userutc = '+' + userutc
  elif (content.find('-') != -1):
    userutc = content.partition('-')[2]
    userutc = '-' + userutc
  else:
    userutc = '+0'
  return userutc

def get_time_left(missing_time):
  
  missing_timefloat = missing_time.total_seconds()
  days, remainder = divmod(missing_timefloat, 86400)
  hours, remaindermin = divmod(remainder, 3600)
  minutes, seconds = divmod(remaindermin, 60)
  if (hours > 0 and days < 1):
    time_left = ('**{:02}h {:02}m {:02}s**'.format(int(hours), int(minutes), int(seconds)))
  elif (days > 0):
    time_left = ('**{:01}d {:02}h {:02}m {:02}s**'.format(int(days), int(hours), int(minutes), int(seconds)))
  else:
    time_left = ('**{:02}m {:02}s**'.format(int(minutes), int(seconds)))
  
  return time_left

ca_isnextday = False
def get_next_ca():
  global now
  global ca_isnextday
  ca_day = ['05','11']
  #second_timezone = False
  
  now = datetime.now(utc)
  first_ca = date.fromisoformat('2022-10-09') #9oct 2022
  days_diff = (now.date() - first_ca).days
  get_day = days_diff % 2

  #case is tomorrow first utc
  if(now.time() > time.fromisoformat(ca_day[get_day] + ':30:00') and
     now.time() > time.fromisoformat(str(int(ca_day[get_day])+12) + ':30:00')
    ):
      ca_isnextday = True
      #second_timezone = False
      if(get_day == 1):
        get_day = 0
      else:
        get_day = get_day + 1

      return(ca_day[get_day])
  
  #case is today second utc
  elif(now.time() > time.fromisoformat(ca_day[get_day] + ':30:00') and 
       now.time() < time.fromisoformat(str(int(ca_day[get_day])+12) + ':30:00')):
      ca_isnextday = False
      #second_timezone = True

      return(str(int(ca_day[get_day])+12))

  #case is today first utc
  elif(now.time() < time.fromisoformat(ca_day[get_day] + ':30:00')):
      ca_isnextday = False
      #second_timezone = False

      return(ca_day[get_day])

  #case is tomorrow second utc (impossible)
  else:
      ca_isnextday = True
      #second_timezone = True

      return 0

canp_isnextday = False
def get_next_canp():
  global now
  global canp_isnextday
  canp_day = ['22','16','01','07']
  #second_timezone = False

  now = datetime.now(utc)
  first_canp = date.fromisoformat('2023-08-11') #11aug 2023
  days_diff = (now.date() - first_canp).days
  get_day = days_diff % 4


  #case is tomorrow first utc
  if(now.time() > time.fromisoformat(canp_day[get_day] + ':30:00')
    ):
      canp_isnextday = True
      get_day = get_day + 1
      if(get_day==4):
        get_day = 0

      return(canp_day[get_day])
  else:
      canp_isnextday = False
      return(canp_day[get_day])


mirage_isnextday = False
mirage_boss = ''
def get_next_mirage():
  global mirage_isnextday
  global mirage_boss

  #timezones are in -3utc for easier calculation
  mirage_day = ['03','09','03','09','03','09']
  mirage_day_end = ['05','11','05','11','05','11']
  mirage_boss_list = ['THUNDORIA', 'SHAITAN', 'ICICLE', 'THUNDORIA', 'SHAITAN', 'ICICLE']

  #second_timezone = False
  
  now_br = datetime.now(utc) - timedelta(hours=3)
  first_mirage = date.fromisoformat('2022-10-13') #13oct 2022
  days_diff = (now_br.date() - first_mirage).days
  get_day = days_diff % 6
  
  #case is tomorrow first utc
  if(now_br.time() > time.fromisoformat(mirage_day_end[get_day] + ':00:00') and
     now_br.time() > (time.fromisoformat(str(int(mirage_day_end[get_day])+12) + ':00:00'))
    ):
      mirage_isnextday = True

      
      #second_timezone = False
      if(get_day == 5):
        get_day = 0
      else:
        get_day = get_day + 1
      mirage_boss = mirage_boss_list[get_day]
      return(mirage_day[get_day])
  
  #case is today second utc
  elif(now_br.time() > time.fromisoformat(mirage_day_end[get_day] + ':00:00') and 
       now_br.time() < time.fromisoformat(str(int(mirage_day_end[get_day])+12) + ':00:00')
      ):
      mirage_isnextday = False
      #second_timezone = True

      mirage_boss = mirage_boss_list[get_day]
      
      if(mirage_day[get_day]=='09'):
        mirage_isnextday = True

      return(str(int(mirage_day[get_day])+12))

  #case is today first utc
  elif(now_br.time() < time.fromisoformat(mirage_day_end[get_day] + ':00:00')):
      mirage_isnextday = False
      #second_timezone = False

      mirage_boss = mirage_boss_list[get_day]
      return(mirage_day[get_day])

  #case is tomorrow second utc (impossible)
  else:
      mirage_isnextday = True
      #second_timezone = True

      return 0

hexa_weekday = 6
def get_next_hexa():
  global now
  global hexa_weekday
  hexa_day = ['06','12','18']
  get_day = ''
  
  now = datetime.now(utc)

  #now.isoweekday() #sat=6, sun=7
  
  if(now.isoweekday() != 6 and now.isoweekday() != 7):
    hexa_weekday = 6
    get_day = '06'
    
  elif(now.isoweekday() == 6):
    for x in hexa_day:
      if(now.time() < time.fromisoformat(x + ':30:00')
        ):
          hexa_weekday = 6
          get_day = x
          break
      if(get_day == ''):
        hexa_weekday = 7
        get_day = '06'
        
  elif(now.isoweekday() == 7):
    for x in hexa_day:
      if(now.time() < time.fromisoformat(x + ':30:00')
        ):
          hexa_weekday = 7
          get_day = x
          break
      if(get_day == ''):
        hexa_weekday = 6
        get_day = '06'

  return(get_day)

newfc_isnextday = False
def newget_next_fc():
  global now
  global newfc_isnextday

  now = datetime.now(utc)
  #now = datetime.fromisoformat('2022-10-29 04:00:00.000000+00:00')

  timers_ref = ['00', '04', '08', '12', '16', '20']


  for x in timers_ref:
    if(now.time() < time.fromisoformat(x + ':45:00')):
      get_timer = x
      newfc_isnextday = False
      #first_maze_id = get_day * 5 + timers_ref.index(x)
      break
    else:
      get_timer = '00'
      newfc_isnextday = True

  next_maze = datetime.fromisoformat(str(now.date()) + " " + get_timer + ":00:00.000000+00:00")
  if(newfc_isnextday == True):
    next_maze = next_maze + timedelta(days=1)

  return next_maze

newds_isnextday = False
def newget_next_ds():
  global now
  global newds_isnextday

  now = datetime.now(utc)
  #now = datetime.fromisoformat('2022-10-29 04:00:00.000000+00:00')

  timers_ref = ['01', '05', '09', '13', '17', '21']


  for x in timers_ref:
    if(now.time() < time.fromisoformat(x + ':45:00')):
      get_timer = x
      newds_isnextday = False
      break
    else:
      get_timer = '01'
      newds_isnextday = True

  next_maze = datetime.fromisoformat(str(now.date()) + " " + get_timer + ":00:00.000000+00:00")
  if(newds_isnextday == True):
    next_maze = next_maze + timedelta(days=1)

  return next_maze

newdw_isnextday = False
def newget_next_dw():
  global now
  global newdw_isnextday

  now = datetime.now(utc)
  #now = datetime.fromisoformat('2022-10-29 04:00:00.000000+00:00')

  timers_ref = ['02', '06', '10', '14', '18', '22']


  for x in timers_ref:
    if(now.time() < time.fromisoformat(x + ':45:00')):
      get_timer = x
      newdw_isnextday = False
      #first_maze_id = get_day * 5 + timers_ref.index(x)
      break
    else:
      get_timer = '02'
      newdw_isnextday = True

  next_maze = datetime.fromisoformat(str(now.date()) + " " + get_timer + ":00:00.000000+00:00")
  if(newdw_isnextday == True):
    next_maze = next_maze + timedelta(days=1)

  return next_maze

abba_isearly = True
def get_next_abba():
  global now
  global abba_isearly

  now = datetime.now(utc)
  #abba_timers = ['12', '18']
  first_abba = date.fromisoformat('2022-10-01') #1oct 2022 , early abba
  #now = datetime.fromisoformat('2022-10-08 21:53:00.016804+00:00')
  next_abba = date.fromisoformat(get_next_weekday(str(now.date()), 5))
  #next_abba = date.fromisoformat('2022-10-08')

  days_diff = (next_abba - first_abba).days
  get_day = days_diff % 14
  
  if(get_day == 0): #early abba
    if(now < datetime.fromisoformat(str(next_abba) + ' 15:00:00').replace(tzinfo=utc)):
      #its really early abba
      abba_isearly = True
      next_abba = datetime.fromisoformat(str(next_abba) + ' 12:00:00')
    else:
      #abba already ended but still saturday, next is late
      abba_isearly = False
      next_abba = datetime.fromisoformat(str(next_abba) + ' 18:00:00') + timedelta(days=7)
    
  elif(get_day == 7): #late abba
    if(now < datetime.fromisoformat(str(next_abba) + ' 21:00:00').replace(tzinfo=utc)):
      #its really late abba
      abba_isearly = False
      next_abba = datetime.fromisoformat(str(next_abba) + ' 18:00:00')
    else:
      #abba already ended but still saturday, next is early
      abba_isearly = True
      next_abba = datetime.fromisoformat(str(next_abba) + ' 12:00:00') + timedelta(days=7)
    
  return next_abba

aurora_first = True ## false = DA AA
def get_next_aada():
  
  global now
  global aurora_first
  now = datetime.now(utc)
  
  first_aada = date.fromisoformat('2022-04-03') #3april 2022 , aa first
  #now = datetime.fromisoformat('2022-10-22 00:00:00.000000+00:00')
  next_aada = date.fromisoformat(get_next_weekday(str(now.date()), 6))

  days_diff = (next_aada - first_aada).days
  get_day = days_diff % 14
  
  if(get_day == 0): #early AA DA
    if(now < datetime.fromisoformat(str(next_aada) + ' 14:00:00').replace(tzinfo=utc)):
      #its early aurora area next
      aurora_first = True
      next_aada = datetime.fromisoformat(str(next_aada) + ' 12:00:00')
    elif(now > datetime.fromisoformat(str(next_aada) + ' 14:00:00').replace(tzinfo=utc)
        and now < datetime.fromisoformat(str(next_aada) + ' 20:00:00').replace(tzinfo=utc)):
      #its late dark area next
      aurora_first = True
      next_aada = datetime.fromisoformat(str(next_aada) + ' 18:00:00')
    else:
      #aada already done, but still sunday its next week
      aurora_first = False
      next_aada = datetime.fromisoformat(str(next_aada) + ' 12:00:00') + timedelta(days=7)
    
  elif(get_day == 7): #dark area first
    if(now < datetime.fromisoformat(str(next_aada) + ' 14:00:00').replace(tzinfo=utc)):
      #its early dark area next
      aurora_first = False
      next_aada = datetime.fromisoformat(str(next_aada) + ' 12:00:00')
    elif(now > datetime.fromisoformat(str(next_aada) + ' 14:00:00').replace(tzinfo=utc)
        and now < datetime.fromisoformat(str(next_aada) + ' 20:00:00').replace(tzinfo=utc)):
      #its late aurora area next
      aurora_first = False
      next_aada = datetime.fromisoformat(str(next_aada) + ' 18:00:00')
    else:
      #aada already done, but still sunday. its next week sunday
      aurora_first = True
      next_aada = datetime.fromisoformat(str(next_aada) + ' 12:00:00') + timedelta(days=7)
  
  return next_aada

def get_next_weekday(startdate, weekday):
  """
    @startdate: given date, in format '2013-05-25'
    @weekday: week day as a integer, between 0 (Monday) to 6 (Sunday)
  """
  d = datetime.strptime(startdate, '%Y-%m-%d')
  t = timedelta((7 + weekday - d.weekday()) % 7)
  return (d + t).strftime('%Y-%m-%d')

def get_weekday(weekday):
  if weekday == 'Mon,':
    return 0
  elif weekday == 'Tue,':
    return 1
  elif weekday == 'Wed,':
    return 2
  elif weekday == 'Thu,':
    return 3
  elif weekday == 'Fri,':
    return 4
  elif weekday == 'Sat,':
    return 5
  elif weekday == 'Sun,':
    return 6
  else:
    return 0

  
#this function is for calculate what time the maze will start or portal close/map active etc.
def maze_timers_const():

    global maze_timer
    global BD1_Time
    global BD1_Status1
    global BD2_Time
    global BD2_Status1
    global now

    #update bd tortuga time
    #update bd tortuga time
    #update bd tortuga time
    #update bd tortuga time
    BD_Tortuga = [
        element.text
        for element in maze_timer.html.find('.boss-time-const-2-2')
    ]
    BD1 = (' \n'.join(BD_Tortuga))
    BD1_Status = [
        element.text for element in maze_timer.html.find('.boss-time-2-2')
    ]
  
    now = datetime.now(utc)

    if (BD1_Status == ['']):
        BD1_Status1 = ['']
    else:
        BD1_Status1 = (' \n'.join(BD1_Status)).split()[0]

    if (BD1_Status1 == ['']):
        BD1_Status1 = 'Alive'
    elif (BD1_Status1 == 'Spawn'):
        BD1_Status1 = 'Dead'
    else:
        BD1_Status1 = 'Bugged'

    if (BD1_Status1 == 'Alive'):
        BD1_Time = now
    elif (BD1_Status1 == 'Dead'):
        if (BD1.split()[1] == 'Tomorrow,'):  #TODO: add if = Tommorow,
            date_entry = BD1[len('Spawn Tomorrow, '):]
            BD_dayBD1 = now.date().strftime('%Y-%m-%d')
            BD_timeBD1 = date_entry.split()[0]
            BD1_Time = datetime.strptime(
                BD_dayBD1 + ' ' + BD_timeBD1 + '.000000+0000',
                '%Y-%m-%d %H:%M:%S.%f%z')
            BD1_Time = BD1_Time + timedelta(days=1)
        elif (BD1.split()[1] == 'Today,'):
            date_entry = BD1[len('Spawn Today, '):]
            BD_dayBD1 = now.date().strftime('%Y-%m-%d')
            BD_timeBD1 = date_entry.split()[0]
            BD1_Time = datetime.strptime(
                BD_dayBD1 + ' ' + BD_timeBD1 + '.000000+0000',
                '%Y-%m-%d %H:%M:%S.%f%z')
        elif (BD1.split()[1] == 'at'
              and (BD1.split()[2] == 'Mon,' or BD1.split()[2] == 'Tue,'
                   or BD1.split()[2] == 'Wed,' or BD1.split()[2] == 'Thu,'
                   or BD1.split()[2] == 'Fri,' or BD1.split()[2] == 'Sat,'
                   or BD1.split()[2] == 'Sun,')):
            date_entryBD1 = BD1[len('Spawn at '):]
            date_entry_weekdayBD1 = get_weekday(
                date_entryBD1.split()[0])  #convert weekday string to integer
            BD_dayBD1 = get_next_weekday(
                now.strftime("%Y-%m-%d"),
                date_entry_weekdayBD1)  #get day of next bd
            BD_timeBD1 = date_entryBD1.split()[1]
            BD1_Time = datetime.strptime(
                BD_dayBD1 + ' ' + BD_timeBD1 + '.000000+0000',
                '%Y-%m-%d %H:%M:%S.%f%z')
        else:
            BD1_Time = now

    #update bd np time
    #update bd np time
    #update bd np time
    #update bd np time
    BD_NP = [
        element.text
        for element in maze_timer.html.find('.boss-time-const-3-3')
    ]
    BD2 = (' \n'.join(BD_NP))
    BD2_Status = [
        element.text for element in maze_timer.html.find('.boss-time-3-3')
    ]

    now = datetime.now(utc)

    if (BD2_Status == ['']):
        BD2_Status1 = ['']
    else:
        BD2_Status1 = (' \n'.join(BD2_Status)).split()[0]

    if (BD2_Status1 == ['']):
        BD2_Status1 = 'Alive'
    elif (BD2_Status1 == 'Spawn'):
        BD2_Status1 = 'Dead'
    else:
        BD2_Status1 = 'Bugged'

    if (BD2_Status1 == 'Alive'):
        BD2_Time = now
    elif (BD2_Status1 == 'Dead'):
        if (BD2.split()[1] == 'Tomorrow,'):  #TODO: add if = Tommorow,
            date_entry = BD2[len('Spawn Tomorrow, '):]
            BD_dayBD2 = now.date().strftime('%Y-%m-%d')
            BD_timeBD2 = date_entry.split()[0]
            BD2_Time = datetime.strptime(
                BD_dayBD2 + ' ' + BD_timeBD1 + '.000000+0000',
                '%Y-%m-%d %H:%M:%S.%f%z')
            BD2_Time = BD2_Time + timedelta(days=1)
        elif (BD2.split()[1] == 'Today,'):
            date_entry = BD2[len('Spawn Today, '):]
            BD_dayBD2 = now.date().strftime('%Y-%m-%d')
            BD_timeBD2 = date_entry.split()[0]
            BD2_Time = datetime.strptime(
                BD_dayBD2 + ' ' + BD_timeBD2 + '.000000+0000',
                '%Y-%m-%d %H:%M:%S.%f%z')
        elif (BD2.split()[1] == 'at'
              and (BD2.split()[2] == 'Mon,' or BD2.split()[2] == 'Tue,'
                   or BD2.split()[2] == 'Wed,' or BD2.split()[2] == 'Thu,'
                   or BD2.split()[2] == 'Fri,' or BD2.split()[2] == 'Sat,'
                   or BD2.split()[2] == 'Sun,')):
            date_entryBD2 = BD2[len('Spawn at '):]
            date_entry_weekdayBD2 = get_weekday(
                date_entryBD1.split()[0])  #convert weekday string to integer
            BD_dayBD2 = get_next_weekday(
                now.strftime("%Y-%m-%d"),
                date_entry_weekdayBD2)  #get day of next bd
            BD_timeBD2 = date_entryBD2.split()[1]
            BD2_Time = datetime.strptime(
                BD_dayBD2 + ' ' + BD_timeBD2 + '.000000+0000',
                '%Y-%m-%d %H:%M:%S.%f%z')
        else:
            BD2_Time = now
    
    maze_timer = []

"""
END OF UPDATE TIMERS FUNCTION
"""

"""
END OF TIMERS FUNCTIONS
"""

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

loop = asyncio.get_event_loop()
tasks = loop.run_until_complete(get_timers())
loop.close()

@client.event
async def on_ready():
    global now
    now = datetime.now(utc)
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    #variables
    channel = message.channel
    content = message.content.lower()

    #timers variables
    global maze_timer
    global BD1_Time
    global BD1_Status1
    global BD2_Time
    global BD2_Status1
    global now

    global babies_respawn_time

    global ca_isnextday
    global canp_isnextday
    global mirage_isnextday
    global mirage_boss
    global hexa_weekday
    global newfc_isnextday
    global newds_isnextday
    global newdw_isnextday
  
    #bot cant trigger own commands
    if message.author == client.user:
        return
      
    #help command
    if content.startswith('.help'):
        print(str(message.author) + content)
        await channel.send("""
`PKO Timers Commands`
`timer aada           `
`what time aada       `
`.aada                `
`when aada            `
`timer aurora         `
`what time aurora     `
`.aurora              `
`when aurora          `
`.aa                  `
`.da                  `
`					 `
`timer abba           `
`what time abba       `
`.abba                `
`when abba            `
`					 `
`.points              `
`					 `
`timer fc             `
`timer ds             `
`what time fc         `
`what time ds         `
`.fc                  `
`.ds                  `
`when fc              `
`when ds              `
`timer dw             `
`what time dw         `
`.dw                  `
`when dw              `
`					 `
`timer hexa           `
`what time hexa       `
`.hexa                `
`when hexa            `
`					 `
`timer mirage         `
`what time mirage     `
`.mirage              `
`when mirage          `
`					 `
`timer ca             `
`what time ca         `
`.ca                  `
`when ca              `
`					 `
`timer bd             `
`what time bd         `
`.bd                  `
`when bd              `
`timer pr bd          `
`what time pr bd      `
`.pr bd               `
`when pr bd           `
`					 `
`.babies              `
`.baby                `
`.set babies          `
`.set baby            `
`					 `
`.event               `
`.event list          `
`					 `
`.list                `
        """
                           )
      
    # BD TIMER
    if content.startswith(
      'timer bd') or content.startswith(
      'what time bd') or content.startswith(
      '.bd') or content.startswith(
      'when bd') or content.startswith(
      'timer pr bd') or content.startswith(
      'what time pr bd') or content.startswith(
      '.pr bd') or content.startswith(
      'when pr bd'):

        print(message.author)

        now = datetime.now(utc)
        missing_time = BD1_Time - now
        
        userutc = get_user_utc(content)

        if (missing_time < timedelta(seconds=1) or BD1_Status1 == 'Alive'):
            maze_timer = await get_timers()
            maze_timers_const()
            now = datetime.now(utc)
            missing_time = BD1_Time - now
            if (BD1_Status1 == 'Alive'):
                await channel.send('**(PORT ROYAL) BD is ALIVE !!!!**')
        else:
            msg1 = '**(PORT ROYAL) BD** Spawns in '

            time_left = get_time_left(missing_time)

            BD1_Timeutc = BD1_Time + timedelta(hours=int(userutc))
            spawntime = BD1_Timeutc.strftime('%A, %B %d | **%H:%M')
            if (userutc == '+0'):
                userutc = ''

            await channel.send(msg1 + time_left + '\n' + spawntime + ' ' + userutc +
                               ' UTC Timezone.**')

    # NEW PROVIDENCE BD TIMER
    if content.startswith(
      'timer np bd') or content.startswith(
      'what time np bd') or content.startswith(
      ',bd') or content.startswith(
      'when np bd') or content.startswith(
      'timer np bd') or content.startswith(
      'what time np bd') or content.startswith(
      ',np bd') or content.startswith(
      'when np bd'):

        print(message.author)

        now = datetime.now(utc)
        missing_time = BD2_Time - now

        userutc = get_user_utc(content)

        if (missing_time < timedelta(seconds=1) or BD2_Status1 == 'Alive'):
            maze_timer = await get_timers()
            maze_timers_const()
            now = datetime.now(utc)
            missing_time = BD2_Time - now
            if (BD2_Status1 == 'Alive'):
                await channel.send('**(NEW PROVIDENCE) BD is ALIVE !!!!**')
        else:
            msg1 = '**(NEW PROVIDENCE) :dragon: BD** Spawns in '

            time_left = get_time_left(missing_time)

            BD2_Timeutc = BD2_Time + timedelta(hours=int(userutc))
            spawntime = BD2_Timeutc.strftime('%A, %B %d | **%H:%M')
            if (userutc == '+0'):
                userutc = ''

            await channel.send(msg1 + time_left + '\n' + spawntime + ' ' + userutc +
                               ' UTC Timezone.**')


    # EVENT TIMERS
    if content.startswith('.event'):

        print(message.author)
        
        nextevent = 0
        status_event = 1  # 1=happening , 2=later
        eventtimeutc = ['', '', '', '', '']
        stringeventtimeutc = ['', '', '', '', '']
        now = datetime.now(utc)
        for x in range(len(eventlist.event_exp_start)):
            if (eventlist.event_exp_start[nextevent].replace(tzinfo=utc) - now <
                    timedelta(seconds=1) and
                (eventlist.event_exp_start[nextevent] + eventlist.event_exp_duration[nextevent]
                 ).replace(tzinfo=utc) - now < timedelta(seconds=1)):
                nextevent = nextevent + 1

            elif (eventlist.event_exp_start[nextevent].replace(tzinfo=utc) - now <
                  timedelta(seconds=1) and
                  (eventlist.event_exp_start[nextevent] + eventlist.event_exp_duration[nextevent]
                   ).replace(tzinfo=utc) - now > timedelta(seconds=1)):
                status_event = 1
                break
            else:
                status_event = 2
                break

        if(nextevent==len(eventlist.event_exp_start)):
            await channel.send('No Event Happening Soon.')
            return
                
        if (status_event == 1):
            end_time = (eventlist.event_exp_start[nextevent] +
                        eventlist.event_exp_duration[nextevent]).replace(tzinfo=utc)
            missing_time = end_time - now
        elif (status_event == 2):
            start_time = eventlist.event_exp_start[nextevent].replace(tzinfo=utc)
            missing_time = start_time - now
        else:
            missing_time = 0

        userutc = get_user_utc(content)

        msg2 = get_time_left(missing_time)

        duration = eventduration(eventlist.event_exp_duration[nextevent])
        event_style = eventlist.event_exp_style[nextevent]

        if 'list' in content:
            for x in range(5):
                try:
                    eventtimeutc[x] = eventlist.event_exp_start[nextevent + x].replace(
                        tzinfo=utc) + timedelta(hours=int(userutc))
                    stringeventtimeutc[x] = eventtimeutc[x].strftime(
                        '%A, %B %d | **%H:%M')
                except Exception:
                    eventtimeutc[x] = ''
                    stringeventtimeutc[x] = ''

            if (userutc == '+0'):
                userutc = ''

            if (status_event == 1):
                ishappening = '**(EVENT HAPPENING)** '
            elif (status_event == 2):
                ishappening = ''

            event_text = ['', '', '', '', '']

            event_text[0] = ishappening + stringeventtimeutc[
                0] + ' ' + userutc + ' UTC Timezone**' + ' @ **Duration:** ' + eventduration(
                    eventlist.event_exp_duration[nextevent]
                ) + ' | **' + eventlist.event_exp_style[nextevent] + '**\n'

            for x in range(1, 5):
                try:
                    event_text[x] = stringeventtimeutc[
                        x] + ' ' + userutc + ' UTC Timezone**' + ' @ **Duration:** ' + eventduration(
                            eventlist.event_exp_duration[nextevent + x]
                        ) + ' | **' + eventlist.event_exp_style[nextevent + x] + '**\n'
                except Exception:
                    event_text[x] = ''

            await channel.send('**Next 5 events at ' + userutc +
                               ' UTC timezone will be at:**\n\n' +
                               event_text[0] + event_text[1] + event_text[2] +
                               event_text[3] + event_text[4])
            return

        if (status_event == 1):
            eventtimeutc = end_time + timedelta(hours=int(userutc))
            stringeventtimeutc = eventtimeutc.strftime('%A, %B %d | **%H:%M')
            if (userutc == '+0'):
                userutc = ''
            await channel.send('Event will end in ' + msg2 + '\n' +
                               '**Duration:** ' + duration + ' | **' +
                               event_style + '**\n' + stringeventtimeutc +
                               ' ' + userutc + ' UTC Timezone.**')

        if (status_event == 2):
            eventtimeutc = start_time + timedelta(hours=int(userutc))
            stringeventtimeutc = eventtimeutc.strftime('%A, %B %d | **%H:%M')
            if (userutc == '+0'):
                userutc = ''
            await channel.send('Next event will be in ' + msg2 + '\n' +
                               '**Duration:** ' + duration + ' | **' +
                               event_style + '**\n' + stringeventtimeutc +
                               ' ' + userutc + ' UTC Timezone.**')

  
    #CA TIMER
    if content.startswith(
      'timer ca') or content.startswith(
      'what time ca') or content.startswith(
      '.ca') or content.startswith(
      'when ca'):

      print(message.author)

      now = datetime.now(utc)

      next_ca = datetime.fromisoformat (now.date().isoformat() + ' ' + get_next_ca() + ':00:00')
      if(ca_isnextday == True):
        next_ca = next_ca + timedelta(days=1)

      userutc = get_user_utc(content)

      missing_time = next_ca.replace(tzinfo=utc) - now
      if(missing_time < timedelta(seconds=1)):
        next_ca = next_ca + timedelta(minutes=30)
        missing_time = next_ca.replace(tzinfo=utc) - now
        ishappening = True
      else:
        ishappening = False

      time_left = get_time_left(missing_time)

      if(ishappening == True):
        msg1 = '**(PORT ROYAL) CA IS HAPPENING!!** <:farmer:1009193279201476670> <:farmer:1009193279201476670> <:farmer:1009193279201476670>'
        msg2 = '\n(PORT ROYAL) Portal will close in '
        await channel.send(msg1 + msg2 + time_left)

      if(ishappening == False):
        ca_utc = next_ca + timedelta(hours=int(userutc))
        spawntime = ca_utc.strftime('%A, %B %d | **%H:%M')
        if (userutc == '+0'):
          userutc = ''

        msg1 = '**(PORT ROYAL) CA** portal opens in '

        await channel.send(msg1 + time_left + '\n' + spawntime + ' ' + userutc + ' UTC Timezone.**')

    # MIRAGE TIMERS
    if content.startswith(
      'timer mirage') or content.startswith(
      'what time mirage') or content.startswith(
      '.mirage') or content.startswith(
      'when mirage'):

      print(message.author)
        
      now = datetime.now(utc)

      getnextmirage = get_next_mirage()
      
      next_mirage = datetime.fromisoformat (now.date().isoformat() + ' ' + getnextmirage + ':00:00') + timedelta(hours=3)
      
      if(mirage_isnextday == True and getnextmirage == '15'):
        next_mirage = next_mirage + timedelta(days=1)
      if(mirage_isnextday == True and getnextmirage == '21' and now.time() < time.fromisoformat('02:00:00')):
        next_mirage = next_mirage - timedelta(days=1)

      userutc = get_user_utc(content)

      missing_time = next_mirage.replace(tzinfo=utc) - now
      if(missing_time < timedelta(seconds=1)):
        next_mirage = next_mirage + timedelta(hours=2)
        missing_time = next_mirage.replace(tzinfo=utc) - now
        ishappening = True
      else:
        ishappening = False

      time_left = get_time_left(missing_time)

      if(ishappening == True):
        msg1 = '**MIRAGE IS HAPPENING!!**'
        msg2 = '\nBoss spawned at: **' + mirage_boss + '**'
        msg3 = '\nPortal will close in '
        await channel.send(msg1 + msg2 + msg3 + time_left)

      if(ishappening == False):
        mirage_utc = next_mirage + timedelta(hours=int(userutc))
        spawntime = mirage_utc.strftime('%A, %B %d | **%H:%M')
        if (userutc == '+0'):
          userutc = ''

        msg1 = '**MIRAGE** portal opens in '
        msg2 = '\nBoss will spawn at: **' + mirage_boss + '**'

        await channel.send(msg1 + time_left + msg2 + '\n' + spawntime + ' ' + userutc + ' UTC Timezone.**')


    # HEXA TIMERS
    if content.startswith(
      'timer hexa') or content.startswith(
      'what time hexa') or content.startswith(
      '.hexa') or content.startswith(
      'when hexa'):

      print(message.author)
        
      now = datetime.now(utc)
      
      get_next_hexa()
      
      next_hexa_date = get_next_weekday(now.date().isoformat(), hexa_weekday-1)

      next_hexa = datetime.fromisoformat (next_hexa_date + ' ' + get_next_hexa() + ':00:00')

      userutc = get_user_utc(content)

      missing_time = next_hexa.replace(tzinfo=utc) - now
      if(missing_time < timedelta(seconds=1)):
        next_hexa = next_hexa + timedelta(minutes=30)
        missing_time = next_hexa.replace(tzinfo=utc) - now
        ishappening = True
      else:
        ishappening = False

      
      time_left = get_time_left(missing_time)

      if(ishappening == True):
        msg1 = '**HEXA IS HAPPENING!!**'
        msg2 = '\nEvent will end in '
        await channel.send(msg1 + msg2 + time_left)

      if(ishappening == False):
        hexa_utc = next_hexa + timedelta(hours=int(userutc))
        spawntime = hexa_utc.strftime('%A, %B %d | **%H:%M')
        if (userutc == '+0'):
          userutc = ''

        msg1 = '**HEXA** will start in '

        await channel.send(msg1 + time_left + '\n' + spawntime + ' ' + userutc + ' UTC Timezone.**')


    #CA TIMER NEW PROVIDENCE
    if content.startswith(
      'timer np ca') or content.startswith(
      'what time np ca') or content.startswith(
      ',ca') or content.startswith(
      'when np ca'):

      print(message.author)

      now = datetime.now(utc)

      next_canp = datetime.fromisoformat (now.date().isoformat() + ' ' + get_next_canp() + ':00:00')


      if(canp_isnextday == True):
        next_canp = next_canp + timedelta(days=1)


      userutc = get_user_utc(content)

      missing_time = next_canp.replace(tzinfo=utc) - now
      if(missing_time < timedelta(seconds=1)):
        next_canp = next_canp + timedelta(minutes=30)
        missing_time = next_canp.replace(tzinfo=utc) - now
        ishappening = True
      else:
        ishappening = False

      time_left = get_time_left(missing_time)

      if(ishappening == True):
        msg1 = '**(NEW PROVIDENCE) CA IS HAPPENING!!** <:farmer:1009193279201476670> <:farmer:1009193279201476670> <:farmer:1009193279201476670>'
        msg2 = '\n(NEW PROVIDENCE) Portal will close in '
        await channel.send(msg1 + msg2 + time_left)

      if(ishappening == False):
        canp_utc = next_canp + timedelta(hours=int(userutc))
        spawntime = canp_utc.strftime('%A, %B %d | **%H:%M')
        if (userutc == '+0'):
          userutc = ''

        msg1 = '**(NEW PROVIDENCE) CA** portal opens in '

        await channel.send(msg1 + time_left + '\n' + spawntime + ' ' + userutc + ' UTC Timezone.**')


    # ABBA TIMER
    if content.startswith(
      'timer abba') or content.startswith(
      'what time abba') or content.startswith(
      '.abba') or content.startswith(
      'when abba'):


      print(message.author)
        
      next_abba = get_next_abba()
      
      userutc = get_user_utc(content)

      missing_time = next_abba.replace(tzinfo=utc) - now
      if(missing_time < timedelta(seconds=1)):
        next_abba = next_abba + timedelta(hours=3)
        missing_time = next_abba.replace(tzinfo=utc) - now
        ishappening = True
      else:
        ishappening = False

      time_left = get_time_left(missing_time)
      
      if(ishappening == True):
        msg1 = '**ABBA IS HAPPENING!!** <:farmer:1009193279201476670> <:farmer:1009193279201476670> <:farmer:1009193279201476670>'
        await channel.send(msg1)

      if(ishappening == False):
        abba_utc = next_abba + timedelta(hours=int(userutc))
        spawntime = abba_utc.strftime('%A, %B %d | **%H:%M')
        if (userutc == '+0'):
          userutc = ''

        msg1 = '**ABBA** portal opens in '
        if abba_isearly == True:
          msg_timezone = ' **(EARLY ABBA)**'
        else:
          msg_timezone = ' **(LATE ABBA)**'

        await channel.send(msg1 + time_left + msg_timezone + '\n' + spawntime + ' ' + userutc + ' UTC Timezone.**')
        

    #AURORA AREA / DARK AREA TIMER
    if content.startswith(
      'timer aada') or content.startswith(
      'what time aada') or content.startswith(
      '.aada') or content.startswith(
      'when aada') or content.startswith(
      'timer aurora') or content.startswith(
      'what time aurora') or content.startswith(
      '.aurora') or content.startswith(
      'when aurora') or content.startswith(
      '.aa') or content.startswith(
      '.da'):

      print(message.author)
        
      next_aada = get_next_aada()

      if aurora_first == True and next_aada.time() == time.fromisoformat('12:00:00') :
        msg2 = ' **(AURORA AREA)**'
      elif aurora_first == True and next_aada.time() == time.fromisoformat('18:00:00') :
        msg2 = ' **(DARK AREA)**'
      elif aurora_first == False and next_aada.time() == time.fromisoformat('12:00:00') :
        msg2 = ' **(DARK AREA)**'
      elif aurora_first == False and next_aada.time() == time.fromisoformat('18:00:00') :
        msg2 = ' **(AURORA AREA)**'
      else:
        msg2 = ''

      userutc = get_user_utc(content)

      missing_time = next_aada.replace(tzinfo=utc) - now
      if(missing_time < timedelta(seconds=1)):
        next_aada = next_aada + timedelta(hours=2)
        missing_time = next_aada.replace(tzinfo=utc) - now
        ishappening = True
      else:
        ishappening = False

      time_left = get_time_left(missing_time)
      
      if(ishappening == True):
        msg1 = '**AA/DA IS HAPPENING!!** <:farmer:1009193279201476670> <:farmer:1009193279201476670> <:farmer:1009193279201476670>'
        await channel.send(msg1 + '\n' + msg2)

      if(ishappening == False):
        aada_utc = next_aada + timedelta(hours=int(userutc))
        spawntime = aada_utc.strftime('%A, %B %d | **%H:%M')
        if (userutc == '+0'):
          userutc = ''

        msg1 = '**AA/DA** portal opens in '

        await channel.send(msg1 + time_left + msg2 + '\n' + spawntime + ' ' + userutc + ' UTC Timezone.**')
     

    # FC TIMER
    if content.startswith(
      'timer fc') or content.startswith(
      'what time fc') or content.startswith(
      ',fc') or content.startswith(
      '.fc') or content.startswith(
      'when fc'):


      #await channel.send("under maintenance")

      print(message.author)

      now = datetime.now(utc)

      next_fc = newget_next_fc()

      userutc = get_user_utc(content)

      missing_time = next_fc.replace(tzinfo=utc) - now
      if(missing_time < timedelta(seconds=1)):
        next_fc = next_fc + timedelta(minutes=40)
        missing_time = next_fc.replace(tzinfo=utc) - now
        ishappening = True
      else:
        ishappening = False


      time_left = get_time_left(missing_time)

      if(ishappening == True):
        msg1 = '**FC IS OPEN RIGHT NOW!!**'
        msg2 = '\nPortal will close in '
        await channel.send(msg1 + msg2 + time_left)

      if(ishappening == False):
        fc_utc = next_fc + timedelta(hours=int(userutc))
        spawntime = fc_utc.strftime('%A, %B %d | **%H:%M')
        if (userutc == '+0'):
          userutc = ''

        msg1 = '**FC** portal opens in '

        await channel.send(msg1 + time_left + '\n' + spawntime + ' ' + userutc + ' UTC Timezone.**' + '\n')


    # DS TIMER
    if content.startswith(
      'timer ds') or content.startswith(
      'what time ds') or content.startswith(
      ',ds') or content.startswith(
      '.ds') or content.startswith(
      'when ds'):

      #await channel.send("under maintenance")


      print(message.author)

      now = datetime.now(utc)

      next_ds = newget_next_ds()
      userutc = get_user_utc(content)

      missing_time = next_ds.replace(tzinfo=utc) - now
      if(missing_time < timedelta(seconds=1)):
        next_ds = next_ds + timedelta(minutes=40)
        missing_time = next_ds.replace(tzinfo=utc) - now
        ishappening = True
      else:
        ishappening = False


      time_left = get_time_left(missing_time)

      if(ishappening == True):
        msg1 = '**DS IS OPEN RIGHT NOW!!**'
        msg2 = '\nPortal will close in '
        await channel.send(msg1 + msg2 + time_left)

      if(ishappening == False):
        ds_utc = next_ds + timedelta(hours=int(userutc))
        spawntime = ds_utc.strftime('%A, %B %d | **%H:%M')
        if (userutc == '+0'):
          userutc = ''

        msg1 = '**DS** portal opens in '

        await channel.send(msg1 + time_left + '\n' + spawntime + ' ' + userutc + ' UTC Timezone.**' + '\n')


    # DW TIMER
    if content.startswith(
      'timer dw') or content.startswith(
      'what time dw') or content.startswith(
      ',dw') or content.startswith(
      '.dw') or content.startswith(
      'when dw'):

      #await channel.send("under maintenance")


      print(message.author)

      now = datetime.now(utc)

      next_dw = newget_next_dw()

      userutc = get_user_utc(content)

      missing_time = next_dw.replace(tzinfo=utc) - now
      if(missing_time < timedelta(seconds=1)):
        next_dw = next_dw + timedelta(minutes=40)
        missing_time = next_dw.replace(tzinfo=utc) - now
        ishappening = True
      else:
        ishappening = False


      time_left = get_time_left(missing_time)

      if(ishappening == True):
        msg1 = '**DW IS OPEN RIGHT NOW!!**'
        msg2 = '\nPortal will close in '
        await channel.send(msg1 + msg2 + time_left)

      if(ishappening == False):
        dw_utc = next_dw + timedelta(hours=int(userutc))
        spawntime = dw_utc.strftime('%A, %B %d | **%H:%M')
        if (userutc == '+0'):
          userutc = ''

        msg1 = '**DW** portal opens in '

        await channel.send(msg1 + time_left + '\n' + spawntime + ' ' + userutc + ' UTC Timezone.**' + '\n')

client.run(TOKEN)


#1800 linhas