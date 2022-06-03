import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import aiohttp
import wikipedia
load_dotenv(dotenv_path="config")

default_intents = discord.Intents.default()
default_intents.members = True
bot = commands.Bot(command_prefix = "!", intents=default_intents, description = "Bot de Juliette")
message_random = 0

@bot.event
async def on_ready():
	print("Le bot est prêt ! ;)")

@bot.event
async def on_member_join(member):
	general_channel: discord.TextChannel = bot.get_channel(899986816751525899)
	await general_channel.send(content=f"Bienvenue {member.display_name} 🐱🐶 Ecris !commandes dans le salon général pour voir apparaître la liste des commandes du Bot !")

@bot.event
async def on_message(message):
	if message.content.lower() == "!commandes":
		await message.channel.send("👋 Salut ! Voici quelques commandes utiles : \n➜ !informations : permet de savoir toutes les informations du serveur \n➜ !commandes : permet de savoir toutes les commandes \n➜!team : permet de choisir si tu es team chat ou team chien (et d'accéder aux salons spécifiques) \n➜!chat ou !chien : à utiliser lorsque tu as choisis ta team, permet de savoir toutes les commandes (dans le salon dédié)")
	if message.content.lower() == "!chat":
		await message.channel.send("🐱 Bienvenue dans la team chat ! Voici quelques commandes utiles : \n➜ !photochat : affiche une photo de chat \n➜ !racechat : affiche un résumé sur les races de chats venant de wikipedia, avec le lien vers l'article")
	if message.content.lower() == "!chien":
		await message.channel.send("🐶 Bienvenue dans la team chien ! Voici quelques commandes utiles : \n➜ !photochien : affiche une photo de chien \n➜ !racechien : affiche un résumé sur les races de chiens venant de wikipedia, avec le lien vers l'article")
	await bot.process_commands(message)

@bot.command(name="informations")
async def serverInfo(ctx):
	server = ctx.guild
	numberOfTextChannels = len(server.text_channels)
	numberOfVoiceChannels = len(server.voice_channels)
	numberOfPerson = server.member_count
	serverName = server.name
	msg = f"Le serveur **{serverName}** contient *{numberOfPerson}* membres ! 😊 \nCe serveur possède {numberOfTextChannels} salons écrits et {numberOfVoiceChannels} salon vocaux. 😉"
	await ctx.channel.send(msg)

@bot.command(name="team")
async def reaction_team(ctx):
	global message_random
	message = await ctx.send("Tu es team chat ou team chien ? 😊 \nSi tu es team chat, réagis avec 🐱 \nSi tu es team chien, réagis avec 🐶")
	await message.add_reaction("🐱")
	await message.add_reaction("🐶")
	message_random = message.id

@bot.event
async def on_raw_reaction_add(payload):
	global message_random
	message_id = payload.message_id
	if message_id == message_random:
		guild_id = payload.guild_id
		guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

		if payload.emoji.name == '🐱':
			role = discord.utils.get(guild.roles, name='Chat')
			member = payload.member
			await member.add_roles(role)
		elif payload.emoji.name == '🐶':
			role = discord.utils.get(guild.roles, name='Chien')
			member = payload.member
			await member.add_roles(role)

@bot.command(name="photochien")
async def chien(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/dog')
      dogjson = await request.json()
   embed = discord.Embed()
   embed.set_image(url=dogjson['link'])
   await ctx.send(embed=embed)

@bot.command(name="photochat")
async def chat(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/cat')
      catjson = await request.json()
   embed = discord.Embed()
   embed.set_image(url=catjson['link'])
   await ctx.send(embed=embed)

@bot.command(name="racechat")
async def wikipediachat(ctx):
	wikipedia.set_lang("fr")
	wikichat = wikipedia.summary("Liste des races de chats")
	msg = f"{wikichat} \n\nSuite de l'article avec toutes les races de chats : https://fr.wikipedia.org/wiki/Liste_des_races_de_chats#"
	await ctx.channel.send(msg)

@bot.command(name="racechien")
async def wikipediachien(ctx):
	wikipedia.set_lang("fr")
	wikichien = wikipedia.summary("Liste des races de chiens")
	msg = f"{wikichien} \n\nSuite de l'article avec toutes les races de chiens : https://fr.wikipedia.org/wiki/Liste_des_races_de_chiens"
	await ctx.channel.send(msg)


bot.run(os.getenv("TOKEN"))
