import discord
import json

class MyClient(discord.Client):
    @staticmethod
    def searchUser(userID):
        records = open("records.json", "r")
        data = json.load(records)
        records.close()

        for i in data["users"]:
            if i["id"] == userID:
                return True
        return False
    
    @staticmethod
    def allInfo():
        records = open("records.json", "r")
        data = json.load(records)
        records.close()
        return data

    @staticmethod
    def getInfo(userID):
        records = open("records.json", "r")
        data = json.load(records)
        records.close()

        for i in data["users"]:
            if i["id"] == userID:
                return i
        return False
    
    @staticmethod 
    def setInfo(userID, featureName, featureVal):
        data = MyClient.allInfo()

        for i in data["users"]:
            if i["id"] == userID:
                i[featureName] = featureVal
                break
        
        records = open("records.json", "w")
        records.write(json.dumps(data))
        records.close()

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author} ({message.author.id}): {message.content}')

        splitMessage = message.content.split()
        senderId = "<@" + str(message.author.id) + ">"

        if splitMessage[0] == "HD!check":
            if len(splitMessage) == 1:
                if self.searchUser(senderId):
                    await message.channel.send(f"You have {self.getInfo(senderId)['points']} points!")
                else:
                    await message.channel.send("You do not have an account! Try making one with `HD! register`")
            else:
                if self.searchUser(splitMessage[1]):
                    info = self.getInfo(splitMessage[1])
                    await message.channel.send(f"{info['alias']} has {info['points']} points!")
                else:
                    await message.channel.send("That person does not have an account!")
        
        if splitMessage[0] == "HD!register":
            senderId = "<@" + str(message.author.id) + ">"

            if self.searchUser(senderId):
                await message.channel.send("You already have an account!")
                return
            else:
                data = self.allInfo()
                records = open("records.json", "w")
                print(str(message.author).split("#")[0])
                newUser = {
                    "id": senderId,
                    "alias": str(message.author).split("#")[0], #removes tag from message author
                    "points": 100,
                    "pointsSent": 0,
                    "pointsReceived": 0
                }
                data["users"].append(newUser)
                records.write(json.dumps(data))

                await message.channel.send("Created your account! You have 100 points")
                records.close()
        
        if splitMessage[0] == "HD!leaderboard":
            data = self.allInfo()

            embed = discord.Embed(title="Leaderboard!!!!", description="This is a temporary leaderboard. The real winner of the challenge is based\non how many points they have been sent, not total points")
            for i in data["users"]:       
                embed.add_field(name=i["alias"], value=i["points"], inline=False)
            await message.channel.send("pppupu", embed=embed)
        
        if splitMessage[0] == "HD!send":
            if len(splitMessage) == 1:
                await message.channel.send("Please enter a valid user")
                return
            elif len(splitMessage) == 2:
                await message.channel.send("Please enter a valid number")
                return
            
            sender = "<@" + str(message.author.id) + ">"
            receiver = splitMessage[1]
            print(splitMessage[2])
            try:
                amount = int(splitMessage[2])
                print("Worked")
                if self.searchUser(sender):
                    if self.searchUser(receiver):
                        if amount > 0:
                            senderInfo = self.getInfo(sender)
                            receiverInfo = self.getInfo(receiver)

                            if senderInfo["points"] >= amount:

                                self.setInfo(sender, "points", senderInfo["points"] - amount)
                                self.setInfo(sender, "pointsSent", senderInfo["pointsSent"] + amount)

                                self.setInfo(receiver, "points", receiverInfo["points"] + amount)
                                self.setInfo(receiver, "pointsReceived", receiverInfo["pointsReceived"] + amount)

                                await message.channel.send(f"Sent {amount} points to {receiverInfo['alias']}!")
                            else:
                                await message.channel.send("You do not have that many points!")
                        else:
                            await message.channel.send("Please enter a positive number")
                    else:
                        await message.channel.send("Please enter a valid user")
                else:
                    await message.channel.send("You do not have an account!")
            except:
                await message.channel.send("Please enter a valid number")


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(open("key.txt", "r").read())
