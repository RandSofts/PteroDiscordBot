from dotenv import load_dotenv
import os

load_dotenv()

import nextcord
from nextcord.ext import commands
import requests

bot = commands.Bot(intents=nextcord.Intents.all())

TESTID = [os.getenv("GUILD_ID")]

urlPan = os.getenv("PANEL_LINK")
apiKey = os.getenv("API_KEY")
idServ = os.getenv("SERVER_ID")

class NewStuff(nextcord.ui.View):
    def __init__(self,bot):
        super().__init__()
        self.bot = bot


    @nextcord.ui.button(label="🫸🏻| Start",style=nextcord.ButtonStyle.blurple)
    async def start(self,button:nextcord.ui.Button,interaction:nextcord.Interaction):
        print("start")
        url = f'{urlPan}/api/client/servers/{idServ}/power'
        headers = {
            "Authorization": f"Bearer {apiKey}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        payload = {
            "signal": "start"
        }

        response = requests.post(url,json=payload,headers=headers)
        await interaction.send(f"The server response was as follows: \n**CODE**: {response.status_code}\n**TEXT**: {response.text}")


    @nextcord.ui.button(label="🛑| Stop",style=nextcord.ButtonStyle.secondary)
    async def stop(self,button:nextcord.ui.Button,interaction:nextcord.Interaction,id:str):
        print("stop")
        url = f'{urlPan}/api/client/servers/{idServ}/power'
        headers = {
            "Authorization": f"Bearer {apiKey}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        payload = {
            "signal": "stop"
        }

        response = requests.post(url,json=payload,headers=headers)
        await interaction.send(f"The server response was as follows: \n**CODE**: {response.status_code}\n**TEXT**: {response.text}")

    @nextcord.ui.button(label="🔄️| Restart",style=nextcord.ButtonStyle.green)
    async def res(self,button:nextcord.ui.Button,interaction:nextcord.Interaction):
        print("res")
        url = f'{urlPan}/api/client/servers/{idServ}/power'
        headers = {
            "Authorization": f"Bearer {apiKey}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        payload = {
            "signal": "restart"
        }

        response = requests.post(url,json=payload,headers=headers)
        await interaction.send(f"The server response was as follows: \n**CODE**: {response.status_code}\n**TEXT**: {response.text}")

    @nextcord.ui.button(label="🧨| Kill",style=nextcord.ButtonStyle.red)
    async def kill(self,button:nextcord.ui.Button,interaction:nextcord.Interaction):
        print("kill")
        url = f'{urlPan}/api/client/servers/{idServ}/power'
        headers = {
            "Authorization": f"Bearer {apiKey}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        payload = {
            "signal": "kill"
        }

        response = requests.post(url,json=payload,headers=headers)
        await interaction.send(f"The server response was as follows: \n**CODE**: {response.status_code}\n**TEXT**: {response.text}")

@bot.slash_command(name="manage",guild_ids=TESTID)
async def manage(interaction:nextcord.Interaction):
    pass


@manage.subcommand(name="stats",description="Get server status")
async def serverStatus(interaction:nextcord.Interaction):
    message = await interaction.send(f"Pinging server....",ephemeral=True)
    print("Server Status")
    headers = {
    "Authorization": f"Bearer {apiKey}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

    data = requests.get(f"{urlPan}/api/client/servers/{idServ}",headers=headers)
    jsonData = data.json()
    embed = nextcord.Embed(title=f"Safecord  server details | {jsonData['attributes']['name']}",description=f"```\nDescription:{jsonData['attributes']['description']}\n```")
    embed.add_field(name="UUID",value=f"```\n{jsonData['attributes']['uuid']}\n```",inline=False)
    limit_text = f"""
```
Memory: {jsonData['attributes']['limits']['memory']}
Swap:   {jsonData['attributes']['limits']['swap']}
Disk:   {jsonData['attributes']['limits']['disk']}
IO:     {jsonData['attributes']['limits']['io']}
CPU:    {jsonData['attributes']['limits']['cpu']}
```
    """
    embed.add_field(name="Limits",value=limit_text,inline=False)
    embed.add_field(name="Suspended",value=jsonData['attributes']['is_suspended'],inline=False)

    moreData = requests.get(f"{urlPan}/api/client/servers/{idServ}/resources",headers=headers)
    jmData = moreData.json()
    embed.add_field(name="State",value=f"```\n{jmData['attributes']['current_state']}\n```",inline=False)
    
    moreText = f"""
```
Memory Bytes:       {jmData['attributes']['resources']['memory_bytes']}
CPU:                {jmData['attributes']['resources']['cpu_absolute']}
Disk Bytes:         {jmData['attributes']['resources']['disk_bytes']}
Network rx bytes:   {jmData['attributes']['resources']['network_rx_bytes']}
Network tx bytes:   {jmData['attributes']['resources']['network_tx_bytes']}

```
    
    """
    embed.add_field(name="Resources",value=moreText,inline=False)
    embed.set_footer(text="Made Letdowntovoid at Randsoft Interactive. Any issues; ask here! https://discord.gg/NTVNwbpKQ4")
    await message.edit(embed=embed)

@manage.subcommand(name="panel",description="Work with the power of your server")
async def power(interaction:nextcord.Interaction):
    if interaction.user.id not in [os.getenv("ADMIN")]:
        return await interaction.send("You cannot run this command!")
    await interaction.send("What would you like to do?",view=NewStuff(bot),ephemeral=True)


bot.run("") # add your bots key lmao