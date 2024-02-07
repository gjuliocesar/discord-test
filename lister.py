import sys
print(sys.executable)
import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

intents = discord.Intents.all()  # Enable all intents for member tracking
bot_token = 'MTIwMzUzOTYxNTg2NTExNDYzNA.GtSHVs.SKvjJl3GZCs1VQ1zW7XyBtlGBHVCarBfGPufdM'
prefix = '!'

bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='list')
async def list_members(ctx):
    # Check if the command is invoked in a voice channel
    if ctx.author.voice:
        voice_channel = ctx.author.voice.channel

        # Get the members in the voice channel
        members = voice_channel.members

        # Print the list of members
        member_list = [member.nick if member.nick else member.name for member in members]
        await ctx.send(f'Members \n {", ".join(member_list)}')
    else:
        await ctx.send('You are not in a voice channel.')

@bot.command(name='bd')
async def scrape_url(ctx):
    try:
        # Specify the URL to scrape
        url = 'https://pirateking.online/database/portal/'

        # Use Selenium to wait for JavaScript to load dynamic content
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        # Wait for dynamic content to load (you may need to adjust the timeout)
        driver.implicitly_wait(10)

        # Get the page source after JavaScript has executed
        page_source = driver.page_source

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Extract the timer value based on the HTML structure
        timer_element = soup.find('span', class_='boss-time-3-3')

     # Check if the element was found
        if timer_element:
            # Extract the timer text content
            timer_text = timer_element.text.strip()

            # Use regular expressions to extract only numbers
            numbers_only = re.sub(r'\D', '', timer_text)

            # Convert the string to integers for hours, minutes, and seconds
            hours = int(numbers_only[:2])
            minutes = int(numbers_only[2:4])
            seconds = int(numbers_only[4:])

            current_time_utc = datetime.utcnow()
            future_time_utc = current_time_utc + timedelta(hours=hours, minutes=minutes, seconds=seconds)
            future_time_epoch = int(future_time_utc.timestamp())

            # Calculate the total seconds
            total_seconds = hours * 3600 + minutes * 60 + seconds

            # Calculate days, hours, minutes, and seconds
            days, remainder = divmod(total_seconds, 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)

            # Calculate the date and time from the current time in UTC
           
            formatted_timer = f'{days:02} Days, {hours:02} Hours, {minutes:02} minutes, {seconds:02} seconds'

            # Send the calculated date and time to the Discord channel
            await ctx.send(f'**BD Will Spawn in**: {formatted_timer} \n In your local time: <t:{future_time_epoch}:R>')
        
        else:
            await ctx.send('Timer not found on the page.')

    except Exception as e:
        await ctx.send(f'An error occurred: {e}')
    finally:
        # Close the Selenium WebDriver
        driver.quit()

# Run the bot
bot.run(bot_token)