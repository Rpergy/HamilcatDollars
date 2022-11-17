import discord
import json

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author.id}: {message.content}')

        if message.content.startswith("HD!embedtest"):
            embed = discord.Embed(title="Sample Embed", description="This is a test embed")
            await message.channel.send(embed)

        if message.content.startswith("HD!register"):
            records = open("records.json", "r")
            data = json.load(records)

            for i in data["users"]:
                if i["id"] == "<@" + str(message.author.id) + ">":
                    await message.channel.send("You already have an account!")
                    records.close()
                    return
            
            records = open("records.json", "w")
            newUser = {
                "id": "<@" + str(message.author.id) + ">",
                "alias": message.author.split("#")[0], #removes tag from message author
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

            leaderboard = []
            message = ""
            for i in data["users"]:
                leaderboard.append(i)

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
                        await message.channel.send(splitMessage[1] + " has " + str(i["points"]) + " points!")
                        return
                
                await message.channel.send("Could not find account")
                records.close()

        if message.content.startswith("HD!send"):
            fail = False
            splitMessage = message.content.split()
            userId = splitMessage[1]
            pointsVal = splitMessage[2]

            if(int(pointsVal) > 0):
                records = open("records.json", "r")
                data = json.load(records)
                for i in data["users"]:
                    if i["id"] == userId:
                        print("Adding points")
                        i["points"] += int(pointsVal)
                        i["pointsReceived"] += int(pointsVal)
                    if i["id"] == "<@" + str(message.author.id) + ">":
                        if i["points"] - int(pointsVal) < 0:
                            fail = True;
                            await message.channel.send("You cannot send that many points!")
                            break;
                        print("Subtracting points")
                        i["points"] -= int(pointsVal)
                        i["pointsSent"] += int(pointsVal)

                if fail == False:
                    await message.channel.send("Sent " + str(pointsVal) + " points to " + str(userId))

                records.close()
                records = open("records.json", "w")
                records.write(json.dumps(data))
            else:
                await message.channel.send("You cannot send that many points!")

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('MTA0MjYyOTI1Mzc1NTMxODI3Mg.GRH2th.J4tIUJ9Ld_1n_CawkZAXr2S11-uk3XRn02oQA8')
