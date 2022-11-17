import discord
import json

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author.id}: {message.content}')
        if message.content.startswith("HD!check"):
            records = open("records.txt", "r")
            data = json.load(records)
            for i in data["users"]:
                if i["id"] == "<@" + str(message.author.id) + ">":
                    await message.channel.send("You have " + str(i["points"]) + " points!")
            records.close()
        
        if message.content.startswith("HD!send"):
            splitMessage = message.content.split()
            userId = splitMessage[1]
            pointsVal = splitMessage[2]

            records = open("records.txt", "r")
            data = json.load(records)
            for i in data["users"]:
                if i["id"] == userId:
                    i["points"] += int(pointsVal)
                if i["id"] == "<@" + str(message.author.id) + ">":
                    i["points"] -= int(pointsVal)
            await message.channel.send("Sent " + str(pointsVal) + " points to " + str(userId))
            records.close()

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('MTA0MjYyOTI1Mzc1NTMxODI3Mg.GRH2th.J4tIUJ9Ld_1n_CawkZAXr2S11-uk3XRn02oQA8')
