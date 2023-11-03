import discord
from discord.ext import commands
from pycoingecko import CoinGeckoAPI
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from classes import Coin
import aiohttp
from newsapi import NewsApiClient
from random import randint


default_intents = discord.Intents.default()
default_intents.members = True
default_intents.message_content = True
cg = CoinGeckoAPI()
bot = commands.Bot(command_prefix='$', intents=default_intents)
bot = commands.Bot(command_prefix='!', intents=default_intents)

response = requests.get("https://newsapi.org/v2/everything?q=crypto&apiKey= {a81da3c5c51943e7b06d457559104185}")
def get_crypto_chart(token):
    chart_data = cg.get_coin_market_chart_by_id(id=f'{token}', vs_currency='chf', days='7')

    def unix_to_date(unix_time): 
        if unix_time > 10**12:
             unix_time /= 1000
        timestamp = datetime.fromtimestamp(unix_time)
        return f"{timestamp.strftime('%d-%m-%Y %H:%M:%S')}"


    new_data = {}

    for each in chart_data['prices']:
            date = unix_to_date(each[0])
            new_data[date] = each[1]
    
    df = pd.DataFrame({'Dates': new_data.keys(), 'Prices': new_data.values()})
    print(df.head())

    df.plot(x ='Dates', y='Prices', kind = 'line', legend = None)	
    plt.axis('off')
    plt.title(f'7-day historical market price of {token}', fontsize=15, color= 'white', fontweight='bold');


    filename =  r"test_chart/test.png"
    plt.savefig(filename, transparent=True)

    plt.close()
    
btc = Coin('bitcoin')
sol = Coin('solana')
eth = Coin('ethereum')

@bot.event
async def on_ready():
    print('Dwight, pour vous servir')

@bot.event
async def on_member_join(member):
    general_channel = bot.get_channel(1163877897887547429)
    await general_channel.send(f'{member.display_name} a rejoint le groupe')

@bot.event
async def on_member_connected(member):
    general_channel = bot.get_channel(1163877897887547429)
    await general_channel.send(f'{member.display_name} tu te reveilles!!')

@bot.event
async def on_message(message):
    global targetnumber

    if message.author == bot.user:
        return  # Pour éviter que le bot ne se réponde à lui-même

    if 'salut' in message.content:
        await message.channel.send('Bonjour!')

    elif 'Wouter' in message.content:
        await message.channel.send('Super Wout est là!')
    
    elif 'Arnaud' in message.content:
        await message.channel.send('Il m a créé!')
    
    elif 'Nassim' in message.content:
        await message.channel.send('NAAAAASSSSSSSSSSSIIIIMMMMM')
    
    elif 'Patrice' in message.content:
        await message.channel.send('Patrice dis que c est comme ca')

    elif message.content.startswith("!del"):
        if message.author.guild_permissions.administrator:  # Vérifie si l'utilisateur a les permissions
            number = int(message.content.split()[1])
            messages = []
            async for msg in message.channel.history(limit = number + 1):
                    messages.append(msg)

            await message.channel.delete_messages(messages)
    
    elif message.content =='!HO':
        await message.channel.send('TOUT LE MONDE DEBOUT')
    
    elif message.content.startswith("$command"):
            await message.channel.send("""
                                            
$btc
$sol
$eth
!news
!guessnumber [] and to answer - []
!HO  
                                                                
                                    """)

    elif message.content.startswith('$btc'):
            get_crypto_chart('bitcoin')
            
            #### Create the initial embed object ####
            embed=discord.Embed(title=f"{btc.coin_name}")

            # Add author, thumbnail, fields, and footer to the embed
            embed.set_author(name=f"{bot.user.name}", icon_url=bot.user.avatar)

            embed.set_thumbnail(url=f"{btc.coin_image}")

            embed.add_field(name="Current Price 💵", value=btc.coin_price, inline=True)
            embed.add_field(name="Circulating Supply 🪙", value= btc.coin_circulating_supply, inline=True)
            embed.add_field(name="Market Cap 🤑", value= f"chf{btc.coin_market_cap}", inline=True)

            embed.add_field(name="24h-High ⬆️", value= btc.coin_high_24h, inline=True)
            embed.add_field(name="24h-low ⬇️", value= btc.coin_low_24h, inline=True)
            embed.add_field(name="Price Change 24h ⏰", value= btc.coin_price_change_percent, inline=True)

            embed.add_field(name="All Time High 👑", value= btc.coin_ath_price, inline=True)
            embed.add_field(name="ATH Percent Change 📊", value= btc.coin_ath_change_percent, inline=True)
            embed.add_field(name="ATL 😢", value = btc.coin_atl, inline=True)
            file = discord.File(r"test_chart/test.png", filename="image.png")

            embed.set_image(url="attachment://image.png")

            embed.set_footer(text="Thank you for using Crypto Bot Price Checker 🙏")

            await message.channel.send(file=file, embed=embed)

    elif message.content.startswith('$sol'):
                    get_crypto_chart('solana')
                    
                    #### Create the initial embed object ####
                    embed=discord.Embed(title=f"{sol.coin_name}")

                    # Add author, thumbnail, fields, and footer to the embed
                    embed.set_author(name=f"{bot.user.name}", icon_url=bot.user.avatar)

                    embed.set_thumbnail(url=f"{sol.coin_image}")

                    embed.add_field(name="Current Price 💵", value=sol.coin_price, inline=True)
                    embed.add_field(name="Circulating Supply 🪙", value= sol.coin_circulating_supply, inline=True)
                    embed.add_field(name="Market Cap 🤑", value= f"chf{sol.coin_market_cap}", inline=True)

                    embed.add_field(name="24h-High ⬆️", value= sol.coin_high_24h, inline=True)
                    embed.add_field(name="24h-low ⬇️", value= sol.coin_low_24h, inline=True)
                    embed.add_field(name="Price Change 24h ⏰", value= sol.coin_price_change_percent, inline=True)

                    embed.add_field(name="All Time High 👑", value= sol.coin_ath_price, inline=True)
                    embed.add_field(name="ATH Percent Change 📊", value= sol.coin_ath_change_percent, inline=True)
                    embed.add_field(name="ATL 😢", value = sol.coin_atl, inline=True)
                    file = discord.File(r"test_chart/test.png", filename="image.png")

                    embed.set_image(url="attachment://image.png")

                    embed.set_footer(text="Thank you for using Crypto Bot Price Checker 🙏")

                    await message.channel.send(file=file, embed=embed)

    elif message.content.startswith('$eth'):
            get_crypto_chart('ethereum')
            
            #### Create the initial embed object ####
            embed=discord.Embed(title=f"{eth.coin_name}")

            # Add author, thumbnail, fields, and footer to the embed
            embed.set_author(name=f"{bot.user.name}", icon_url=bot.user.avatar)

            embed.set_thumbnail(url=f"{eth.coin_image}")

            embed.add_field(name="Current Price 💵", value=eth.coin_price, inline=True)
            embed.add_field(name="Circulating Supply 🪙", value= eth.coin_circulating_supply, inline=True)
            embed.add_field(name="Market Cap 🤑", value= f"eth{eth.coin_market_cap}", inline=True)

            embed.add_field(name="24h-High ⬆️", value= eth.coin_high_24h, inline=True)
            embed.add_field(name="24h-low ⬇️", value= eth.coin_low_24h, inline=True)
            embed.add_field(name="Price Change 24h ⏰", value= eth.coin_price_change_percent, inline=True)

            embed.add_field(name="All Time High 👑", value= eth.coin_ath_price, inline=True)
            embed.add_field(name="ATH Percent Change 📊", value= eth.coin_ath_change_percent, inline=True)
            embed.add_field(name="ATL 😢", value = eth.coin_atl, inline=True)
            file = discord.File(r"test_chart/test.png", filename="image.png")

            embed.set_image(url="attachment://image.png")

            embed.set_footer(text="Thank you for using Crypto Bot Price Checker 🙏")

            await message.channel.send(file=file, embed=embed)
    
    elif message.content.startswith('!news'):
        url = ('https://newsapi.org/v2/top-headlines?'
        'country=fr&'
        'apiKey=a81da3c5c51943e7b06d457559104185')

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            print(data)

            if articles:
                for article in articles:
                    author = article.get('author')
                    url = article.get('url')
                    titre = article.get('title')
                    newmessage = f"Titre : {titre}\n Auteur : {author}\nLien : {url}"
                    await message.channel.send(newmessage)
            else:
                await message.channel.send("Aucun article trouvé pour ce sujet sur News.")
        else:
            await message.channel.send("Erreur lors de la récupération des articles News.")
    
    elif message.content.startswith('!guessnumber'):
        try:
            nbmax = int(message.content.split(' ')[1])
            targetnumber = randint(1, nbmax)
            await message.author.send(targetnumber)


           
        except (IndexError, ValueError):
            await message.channel.send("Veuillez entrer un nombre valide après la commande !guessnumber")

    elif message.content.startswith('-') and targetnumber is not None:
            print(targetnumber)
            await message.channel.send(f'{message.author} remporte la partie. Le nombre était {targetnumber}')
            targetnumber = None  

        

bot.run("MTE2ODgyOTMzNDI3NDk2OTYxMA.GeKb5G.RmS2ivFVHu1O5Jps2RN38Z_agK3Cez4xaIC3QY")
