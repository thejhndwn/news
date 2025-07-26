from twitchio.ext import commands

class TwitchBot(commands.Bot):
    def __init__(self, token: str, client_id:str, bot_nick: str, prefix: str, channel: str):
        super().__init__(
                token,
                prefix,
                initial_channels=[channel])
        # connect to twitch 
        self.donations = []
        self.ongoing_story = ""
        self.story_upvote = 0
        self.story_downvote = 0
        self.voice_upvote = 0
        self.voice_downvote = 0
        
        pass

    async def event_ready(self):
        print(f" Logged in as | {self.nick}")
    async def event_message(self, message):
        if message.echo: return
        await self.handle_commands(message)
    
    @commands.command(name="expression")
    async def expression(self, ctx):
        args = ctx.message.content.split()
        if len(args) >= 2:
            expression_name = args[1]
            # TODO: add expression verification
            print(f"{ctx.author.name} wants expression: {expression_name}")

    @commands.command(name="animation")
    async def animation(self, ctx):
        args = ctx.message.content.split()
        if len(args) >= 2:
            animation_name = args[1]
            # TODO: add animation verification
            print(f"{ctx.author.name} wants animation: {animation_name}")

    @commands.command(name="likeystory")
    async def likeystory(self, ctx):
        self.story_upvote +=1

    @commands.command(name="nolikeystory")
    async def dislikeystory(self, ctx):
        self.story_downvote -=1

    @commands.command(name="likeyvoice")
    async def likeyvoice(self, ctx):
        self.voice_update +=1

    @commands.command(name="dislikeyvoice")
    async def dislikeyvoice(self, ctx):
        self.story_update +=1

    @commands.command(name="suggest")
    async def suggest_story(self, ctx):
        args = ctx.message.content.split()
        if len(args) >= 2:
            story_url= args[1]
            # TODO: add animation verification
            print(f"{ctx.author.name} wants story with url: {story_url}")

    def run(self):
        self.bot.run()

    def get_donations(self):
        return self.donations

    def add_donation(self, user:str, amt: str, msg:str):
        self.donations.append((user, amt, msg))

    def clear_donations(self):
        self.donations.clear()


