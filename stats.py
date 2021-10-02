from pypresence import Presence
from time import time

RPC = Presence(Id)

btns = [
	{
		'label': 'VK',
		'url': 'https://vk.com/deb228pro' 
	},
	{
		'label': 'Discord',
		'url': 'https://discord.gg/vfamaly'
	}
]

RPC.connect()
RPC.update(
	state='Сидит на стуле',
	buttons=btns,
	start=time(),
	large_image='python',
	large_text='Здесь могла быть ваша реклама',
	small_image='perc'
	)
print('done!')
input()
