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


def make_evolution_chain(species: pokebase.pokemon_species):
    evolution_chain = [None, None, None]
    evolution_chain[0] = [species.evolution_chain.chain.species.name]

    if (species.evolution_chain.chain.evolves_to != []):
        temp_list = []
        for s in species.evolution_chain.chain.evolves_to:
            temp_list.append(s.species.name)
        evolution_chain[1] = temp_list

        if (species.evolution_chain.chain.evolves_to[0].evolves_to != []):
            temp_list = []
            for s in species.evolution_chain.chain.evolves_to[0].evolves_to:
                temp_list.append(s.species.name)
            evolution_chain[2] = temp_list

    return evolution_chain


@tree.command(name = 'search', description = 'Search for a Pokemon')
async def search(interaction: discord.Interaction, name: str):
    name = name.lower()
    id = pokebase.pokemon_species(name).id
    image = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{id}.png"
    species = pokebase.pokemon_species(name)
    evolution_chain = make_evolution_chain(species)
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



    if species.name in evolution_chain[0]:
        embed.add_field(name = "Evolves From", value = "N/A", inline = True)
        evolves_to = ""
        if evolution_chain[1] != None:
            for s in evolution_chain[1]:
                evolves_to += s
                evolves_to += ', '
            embed.add_field(name = "Evolves To", value = evolves_to, inline = True)
        else:
            embed.add_field(name = "Evolves To", value = "N/A", inline = True)
    elif species.name in evolution_chain[1]:
        embed.add_field(name = "Evolves From", value = evolution_chain[0][0], inline = True)
        if evolution_chain[2] != None:
            evolves_to = ""
            for s in evolution_chain[2]:
                evolves_to += s
                evolves_to += ', '
            embed.add_field(name = "Evolves To", value = evolves_to, inline = True)
        else:
            embed.add_field(name = "Evolves To", value = "N/A", inline = True)
    else:
        embed.add_field(name = "Evolves From", value = evolution_chain[1][0], inline = True)
        embed.add_field(name = "Evolves To", value = "N/A", inline = True)

    await interaction.response.send_message(embed=embed)

file = open('bot_token.txt')

bot.run(file.readline())

