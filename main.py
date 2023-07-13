import io
import os
from collections import OrderedDict
from threading import Thread
import requests
import time

os.system("pip install --upgrade poe-api")
import poe
import discord
from discord.ext import commands

token = open("token.txt", "r").read().strip()

client = commands.Bot(
    command_prefix=".",
    self_bot=True,
    guild_subscription_options=discord.GuildSubscriptionOptions.off(),
)
client._skip_check = lambda x, y: False

class fText:
    def __init__(self, text=""):
        self.text = text
        self.prefix = ""
        self.suffix = ""
        self.untext = ""

        self.styles = {"bold": "1", "underline": "4"}

        self.colors = {
            "gray": "30",
            "red": "31",
            "green": "32",
            "yellow": "33",
            "blue": "34",
            "pink": "35",
            "cyan": "36",
            "white": "37",
        }

        self.backgrounds = {
            "darkblue": "40",
            "orange": "41",
            "blue": "42",
            "purple": "43",
            "gray": "44",
            "indigo": "45",
            "lightgray": "46",
            "white": "47",
        }

    def translate(self, style=None, color=None, background=None, keep=True):
        if style == None and color == None and background == None and keep:
            return ""
        elif style == None and color == None and background == None and not keep:
            return "\u001b[0m"

        if style in self.styles:
            style = self.styles[style]
        else:
            style = "0"
        if color in self.colors:
            color = self.colors[color]
        else:
            color = None
        if background in self.backgrounds:
            background = self.backgrounds[background]
        else:
            background = None

        stylee = f"\u001b[{style}"
        if color:
            stylee += f";{color}"
        if background:
            stylee += f";{background}"

        return f"{stylee}m"

    def add(self, text, style=None, color=None, background=None):
        self.text += f"{self.translate(style, color, background)}{text}"
        self.untext += text

    def color(self, color):
        self.text += self.translate(color=color)

    def pre(self, text):
        self.prefix += text

    def suf(self, text):
        self.suffix += text

    def __str__(self):
        self.final = f"```ansi\n{self.text}```" if self.text else ""
        return f"{self.prefix}\n{self.final}\n{self.suffix}"

    def to_file(self):
        return io.StringIO(f"{self.prefix}\n{self.untext}\n{self.suffix}")

class bot(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.run_flask = os.name == "posix"

        self.initialize_poe()
        self.poe_modes = self.poe_client.bot_names
        self.poe_modes = OrderedDict(
            sorted(self.poe_modes.items(), key=lambda t: t[0])
        )
        self.poe_modes = OrderedDict([(v, k) for k, v in self.poe_modes.items()])
        self.current_mode = 0
        poe_keys = list(self.poe_modes.keys())
        for i in range(len(self.poe_modes)):
            if poe_keys[i] == "GPT-4-32k":
                self.current_mode = i
                break
        
        self.poe_queue = []
        self.poe_processing = False
        
        self.blacklist = [".", "!"]
        self.last_send = 0
        
    def initialize_poe(self):
        self.poe_client = poe.Client("JmkN8t5ZCfpwRB7Z-jp3Bg%3D%3D")
    
    def setup(self):
        if self.run_flask:
            from flask import Flask

            site = Flask("")

            @site.route("/")
            def main_page():
                return "xd"

            def run(site):
                site.run(host="0.0.0.0", port=8080)
            def ku(url):
                url = f'https://{url}' if not url.startswith('https') else url
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
                    'Accept': '*/*',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Content-Type': 'application/json',
                    'Cache-Control': 'no-cache, no-store, must-revalidate',
                    'Pragma': 'no-cache',
                    'Expires': '0',
                    'X-SesId': '1687055417783',
                    'X-DevId': '8994da85-c5a0-48d7-9fcc-3f5b9d19d724R',
                    'Origin': 'https://reqbin.com',
                    'Connection': 'keep-alive',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-site',
                }
                
                json_data = {
                    'id': '0',
                    'name': '',
                    'errors': '',
                    'json': '{"method":"GET","url":"' + url + '","apiNode":"US","contentType":"","headers":"","errors":"","curlCmd":"","codeCmd":"","jsonCmd":"","xmlCmd":"","lang":"","auth":{"auth":"noAuth","bearerToken":"","basicUsername":"","basicPassword":"","customHeader":"","encrypted":""},"compare":false,"idnUrl":"' + url + '"}',
                    'sessionId': 1687055417783,
                    'deviceId': '8994da85-c5a0-48d7-9fcc-3f5b9d19d724R',
                }
                while True:
                    requests.post('https://apius.reqbin.com/api/v1/requests', headers=headers, json=json_data)
                    time.sleep(180)
            
            server = Thread(target=run, args=(site,))
            server.start()
            k = Thread(target=ku, args=("sydney.jyealc.repl.co", ))
            k.start()
            server = Thread(target=run, args=(site,))
            server.start()

    @commands.Cog.listener()
    async def on_ready(self):
        self.setup()
        await client.change_presence(
            activity=discord.Streaming(
                name="シドニー",
url="https://www.youtube.com/watch?v=1m_ZoPTrtCk&t=10",
                assets={
                    "large_image": "mp:attachments/1036877572287508510/1084341236997046282/neuroleave-neurosama.gif",
                    "small_image": "mp:attachments/1084334628149657724/1084338190481109112/bdcd0f15250c40a0be9ba1ad2b8f30af.png",
                    "large_text": "Neuro-sama",
                    "small_text": "Sydney [Bot]",
                },
            )
        )
        print("Bot is ready")

    def get_mode(self, nick=False):
        if nick:
            return self.poe_modes[list(self.poe_modes.keys())[self.current_mode]]
        return list(self.poe_modes.keys())[self.current_mode]
    
    @commands.command()
    async def mode(self, ctx, mode: int):
        ftext = fText()
        if mode in range(len(self.poe_modes)):
            self.current_mode = mode
            ftext.add("Mode changed to", color="white")
            ftext.add(f" {self.get_mode()}", color="green")
            
            await ctx.reply(ftext, mention_author=False)
            return
        ftext.add("Mode ", color="white")
        ftext.add(f"{mode}", color="red")
        ftext.add(" not found\n", color="white")
        ftext.add(f"Use {ctx.prefix}modes to see all modes", color="white")
        await ctx.reply(ftext, mention_author=False)
            
    @commands.command()
    async def modes(self, ctx):
        ftext = fText()
        ftext.add("Modes:\n", style="bold", color="blue")
        for i, mode in enumerate(self.poe_modes.keys()):
            ftext.add(f"{i}) ", color="white")
            ftext.add(f"{mode}\n", color="blue" if i != self.current_mode else "cyan")
        ftext.add(f"{self.get_mode()}", color="cyan")
        ftext.add(" is currently selected", color="white")
        await ctx.reply(ftext, mention_author=False)

    @commands.command()
    async def cleargpt(self, ctx):
        self.poe_client.send_chat_break(self.get_mode(nick=True))
        ftext = fText()
        ftext.add(f"Conversation for {self.get_mode()} cleared", color="green")
        await ctx.reply(ftext, mention_author=False)

    @staticmethod
    def handle_backticks(text_chunks):
        new_text_chunks = []
        markdown_type = ""
        markdown_state = False # False = not in markdown, True = in markdown
        
        for chunk in text_chunks:
            if not markdown_state and chunk.count("```") % 2 == 1:
                markdown_state = True
                new_text_chunks.append(f"{chunk}```")
                markdown_type = chunk.split("```")[-1].split("\n")[0]
            elif markdown_state and chunk.count("```") % 2 == 1:
                markdown_state = False
                new_text_chunks.append(f"```{markdown_type}\n{chunk}")
            elif markdown_state and chunk.count("```") == 0:
                markdown_state = False
                new_text_chunks.append(f"```{markdown_type}\n{chunk}```")
            else:
                new_text_chunks.append(chunk)
                
        return new_text_chunks
    
    async def handle_poe(self):
        if not self.poe_queue:
            return
        
        if time.time() - self.last_send > 1800:
            self.last_send = time.time()
            self.initialize_poe()
        
        message, reply = self.poe_queue.pop(0)
        content = message.content
        
        self.poe_processing = True
        
        process_ftext = fText()
        process_ftext.add("Processing...", color="blue")
        
        complete_ftext = fText()
        complete_ftext.add("Completed...", color="cyan")
        
        reserved_ftext = fText()
        reserved_ftext.add("Reserved...", color="yellow")
        
        reserved_reply = await message.channel.send(reserved_ftext)
        used_reserved = False
        
        text_buffer = [str(process_ftext)]
        
        original_reply = reply
        
        all_messages = [message]
        try:
            for i, chunk in enumerate(self.poe_client.send_message(self.get_mode(nick=True), content)):
                if len(text_buffer[-1]) + len(chunk["text_new"]) > 1950:
                    section = text_buffer[-1].split("\n")
                    first, second = "\n".join(section[:-1]), section[-1]
                    text_buffer[-1] = first
                    text_buffer.append(second)
                    text_buffer[-1] += chunk["text_new"]
                    
                    new_text_buffer = self.handle_backticks(text_buffer)
                    
                    await reply.edit(content=new_text_buffer[-2], allowed_mentions=discord.AllowedMentions.none())
                    await reserved_reply.edit(content=new_text_buffer[-1], allowed_mentions=discord.AllowedMentions.none())
                    used_reserved = True
                    reply = reserved_reply
                    all_messages.append(reply)
                else:
                    text_buffer[-1] += chunk["text_new"]
                    
                if i % 15 == 0:
                    new_text_buffer = self.handle_backticks(text_buffer)
                    await reply.edit(content=new_text_buffer[-1], allowed_mentions=discord.AllowedMentions.none())
        except RuntimeError:
            pass
        
        text_buffer[0] = text_buffer[0].replace(str(process_ftext), str(complete_ftext))
        new_text_buffer = self.handle_backticks(text_buffer)
        await reply.edit(content=new_text_buffer[-1], allowed_mentions=discord.AllowedMentions.none())                
        await original_reply.edit(content=new_text_buffer[0], allowed_mentions=discord.AllowedMentions.none())
        
        if not used_reserved:
            await reserved_reply.delete()
            
        if len(self.poe_queue) > 0:
            await self.handle_poe()
        else:
            self.poe_processing = False
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content[0] not in self.blacklist and message.author.id != self.client.user.id:
            ftext = fText()
            ftext.add("Added to queue...", color="pink")      
            ftext.add(f" ({len(self.poe_queue)})")
            reply = await message.reply(ftext, mention_author=False)
            self.poe_queue.append([message, reply])
            
        if not self.poe_processing:
            await self.handle_poe()
    
cog = bot(client)
client.add_cog(cog)
for command in client.commands:
    if command.hidden:
        command.checks.append(lambda ctx: ctx.author.id == 250543577493536769)

try:
    client.run(token, reconnect=True)
except discord.ext.commands.errors.CommandInvokeError:
    os.system("kill 1")
