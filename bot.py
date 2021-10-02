import discord
import datetime
import time
import asyncio
import os
from discord.ext.commands import ConversionError
from datetime import date
from discord import utils
from asyncio import sleep
from discord.ext import commands
from config import settings

bot = commands.Bot(command_prefix = settings['prefix'])
bot.remove_command('help')


#command
@bot.command()
@commands.has_role(settings['id_role']) # Не передаём аргумент pass_context, так как он был нужен в старых версиях.
async def помощь(ctx):
	#страница 1 модератарам
	embed=discord.Embed(title="HELP", color=0xff0000)
	embed.add_field(name='!заглушить [Участник] [время]', value='заглушить участника (Время указывать в минутах)')
	embed.add_field(name="!выгнать [Участник]", value="Забанить участника", inline=False)	
	embed.add_field(name='!очистить [Количество]', value='Очистить сообщения',inline=False)
	await ctx.send(embed=embed)
	embed=discord.Embed(title='HELP', color=0xff0000)
	embed.add_field(name='''!ДЗ (Класс) (Предмет) (Страница) (Номер_Задание)''', value='Дать дз')
	embed.set_footer(text=f"Учитель {ctx.message.author}", icon_url=ctx.author.avatar_url)
	await ctx.send(embed=embed)

@bot.command()
@commands.has_role(settings['id_role'])
async def ДЗ(ctx, reason_1, reason_2, reason_3, *, reason_4: int):

	channel = bot.get_channel(882249099989098506)
	embed=discord.Embed(title=f'Дз для {reason_1} класса!', color=0xff0000)
	embed.add_field(name='Домашние задание', value=f'Класс - {reason_1}\nПредмет - {reason_2}\nСтраница - {reason_3}\nЗадание - {reason_4}')
	embed.set_footer(text=f"Учитель {ctx.message.author}", icon_url=ctx.author.avatar_url)
	await channel.send(embed=embed)

@bot.command()
@commands.has_role(settings['id_role'])
async def заглушить(ctx, member:discord.Member, time:int, *, reason:str='Не указана'):
	if not member:
		await ctx.send('Укажите участника которо-го хотите заглушить')
		return
	if not time:
		await ctx.send('Укажите время\n!заглушить [@Участник] [Время] [Причина]')
		return
	if ctx.author.mention == member.mention:
		await ctx.send('Нельзя себя заглушить!\n!заглушить [@Участник] [Время] [Причина)' )
		return

	mute_role = discord.utils.get(ctx.message.guild.roles, name='Мут')
	current_datetime = date.today()

	await member.add_roles(mute_role)
	embed = discord.Embed(title='Участник был Заглушон!',description=f'''
	Ученик(ца): {member.mention}
	Учитель: {ctx.author.mention}
	Причина: {reason}
	На: {time} минут
	Причина: {reason}
	В: {current_datetime}''')
	await ctx.send(embed=embed)
	await asyncio.sleep(time * 60)
	await member.remove_roles(mute_role)
	await ctx.send(f'Ура {member.mention} Может говорить')

#clear
@bot.command()
@commands.has_role(settings['id_role'])
async def очистить(ctx, amount: int = None):
	if not amount:
		await ctx.channel.purge(limit = None)
		embed=discord.Embed(color=0xff0000)
		embed.add_field(name='Сообщения успешно удалены', value=':grinning:')
		embed.set_footer(text=f"Удалил(а) {ctx.message.author}", icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed)
		return
	await ctx.channel.purge(limit = amount)
	embed=discord.Embed(color=0xff0000)
	embed.add_field(name='Сообщения успешно удалены', value=':grinning:')
	embed.set_footer(text=f"Удалил(а) {ctx.message.author}", icon_url=ctx.author.avatar_url)
	await ctx.send(embed=embed)

#banf
@bot.command()
@commands.has_role(settings['id_role'])
async def выгнать(ctx, member:discord.Member=None, reason='Не указана'):
	if (member == ctx.author):
		embed=discord.Embed(color=0xff0000)
		embed.add_field(name='Вы не можете себя забанить', value=':worried: Ошибка', inline=True)
		await ctx.send(embed=embed)
		return
	if (not member):
		embed=discord.Embed(color=0xff0000)
		embed.add_field(name='Укажите кого забанить', value=':worried: Ошибка', inline=True)
		await ctx.send(embed=embed)
		return

	await member.ban(reason=reason)

	embed = discord.Embed(title='Участник был Забанин!',description=f'''
	Участник: {member.mention}
	Учитель: {ctx.author.mention}
	Причина: {reason}''')
	await ctx.send(embed=embed)
#error

#event
@bot.event
async def on_ready():
    print('Logged in as:\n{0.user.name}\n{0.user.id}'.format(bot))  
@bot.event
async def on_command_error(ctx, error):
	emd = discord.Embed(title = 'Error', color=0xff0000)
	emb.add_field(name='Ошибка', value=f'```{error}```')
	await ctx.send(emb = embed)

bot.run(settings['token'])