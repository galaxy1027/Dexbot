import discord
from discord import app_commands
import pokebase

class Client(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f'We have logged in as {bot.user}')

bot = Client()
tree = app_commands.CommandTree(bot)

@tree.command(name = 'search', description = 'Search for a Pokemon')
async def search(interaction: discord.Interaction, name: str):
    name = name.lower()
    id = pokebase.pokemon_species(name).id
    image = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{id}.png"
    species = pokebase.pokemon_species(name)
    
    entry = ""
    entry_list = species.flavor_text_entries
    i = len(entry_list) - 1
    while i > -1:
        if (entry_list[i].language.name == 'en'):
            entry = entry_list[i].flavor_text
            i = -1
        i -= 1

    
    embed = discord.Embed(
    title = species.names[8].name,
    description = entry,
    color = discord.Color.blue()
    )
    embed.set_image(url = image)
    

    await interaction.response.send_message(embed=embed)

file = open('bot_token.txt')

bot.run(file.readline())

