import discord
import json

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author.id}: {message.content}')

        if message.content.startswith("HD!register"):
            records = open("records.json", "r")
            data = json.load(records)

            for i in data["users"]:
                if i["id"] == "<@" + str(message.author.id) + ">":
                    await message.channel.send("You already have an account!")
                    records.close()
                    return
            
            records = open("records.json", "w")
            print(str(message.author).split("#")[0])
            newUser = {
                "id": "<@" + str(message.author.id) + ">",
                "alias": str(message.author).split("#")[0], #removes tag from message author
                "points": 100,
                "pointsSent": 0,
                "pointsReceived": 0
            }
            data["users"].append(newUser)
            records.write(json.dumps(data))
            records.close()
            await message.channel.send("Account created! You have 100 points!")

        if message.content.startswith("HD!leaderboard"):
            records = open("records.json", "r")
            data = json.load(records)

            embed = discord.Embed(title="Leaderboard!!!!", description="This is a temporary leaderboard. The real winner of the challenge is based\non how many points they have been sent, not total points")
            for i in data["users"]:       
                embed.add_field(name=i["alias"], value=i["points"], inline=False)
            await message.channel.send(embed=embed)

            records.close()

        if message.content.startswith("HD!check"):
            splitMessage = message.content.split()

            if len(splitMessage) == 1:
                records = open("records.json", "r")
                data = json.load(records)
                for i in data["users"]:
                    if i["id"] == "<@" + str(message.author.id) + ">":
                        await message.channel.send("You have " + str(i["points"]) + " points!")
                        records.close()
                        return
                await message.channel.send("Could not find account")
            else:
                records = open("records.json", "r")
                data = json.load(records)
                for i in data["users"]:
                    if i["id"] == str(splitMessage[1]):
                        await message.channel.send(str(i["alias"]) + " has " + str(i["points"]) + " points!")
                        return
                
                await message.channel.send("Could not find account")
                records.close()

        if message.content.startswith("HD!send"):
            fail = False
            splitMessage = message.content.split()
            userId = splitMessage[1]
            pointsVal = splitMessage[2]

            foundReceiver = False
            foundSender = False

            if int(pointsVal) > 0:
                records = open("records.json", "r")
                data = json.load(records)
                for i in data["users"]:
                    if i["id"] == userId:
                        foundReceiver = True
                        i["points"] += int(pointsVal)
                        i["pointsReceived"] += int(pointsVal)
                    if i["id"] == "<@" + str(message.author.id) + ">":
                        foundSender = True
                        if i["points"] - int(pointsVal) < 0:
                            fail = True;
                            break;
                        print("Subtracting points")
                        i["points"] -= int(pointsVal)
                        i["pointsSent"] += int(pointsVal)

                if fail == False and foundSender and foundReceiver:
                    await message.channel.send("Sent " + str(pointsVal) + " points to " + str(userId))
                elif foundSender:
                    await message.channel.send("That account does not exist!")
                elif foundReceiver and fail == False:
                    await message.channel.send("You do not have an account yet!")
                else:
                    await message.channel.send("You cannot send that many points!")

                records.close()
                records = open("records.json", "w")
                records.write(json.dumps(data))
            else:
                await message.channel.send("Muthu!")

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('MTA0MjYyOTI1Mzc1NTMxODI3Mg.GRH2th.J4tIUJ9Ld_1n_CawkZAXr2S11-uk3XRn02oQA8')
