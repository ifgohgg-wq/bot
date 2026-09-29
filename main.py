import discord
from discord.ext import commands
import os

TOKEN = os.getenv("DISCORD_TOKEN")
TICKET_CATEGORY_ID = 1550873004710428742
SUPPORT_ROLE_ID = 1554440757996421170

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="إغلاق التذكرة", style=discord.ButtonStyle.red, custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.channel.delete()

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="فتح تذكرة", style=discord.ButtonStyle.green, custom_id="open_ticket", emoji="🎫")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.defer(ephemeral=True)
            guild = interaction.guild
            category = guild.get_channel(TICKET_CATEGORY_ID)
            support_role = guild.get_role(SUPPORT_ROLE_ID)
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            }
            if support_role:
                overwrites[support_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
            channel = await guild.create_text_channel(
    name=f"ticket-{interaction.user.name}".lower().replace(" ", "-")[:90],
    overwrites=overwrites,
    reason="Ticket opened"
            )

@bot.event
async def on_ready():
    bot.add_view(TicketView())
    print(f"شغال: {bot.user}")

bot.run(TOKEN)
