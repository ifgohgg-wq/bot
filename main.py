import discord
import os
from discord.ext import commands
from discord import app_commands
TOKEN = os.getenv("DISCORD_TOKEN")
TICKET_CATEGORY_ID = 1550873035744088064  # حط ايدي الكاتقوري هنا
SUPPORT_ROLE_ID = 1554440757996421170      # حط ايدي رتبة الدعم هنا

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="فتح تذكرة", style=discord.ButtonStyle.green, emoji="🎫", custom_id="open_ticket")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
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
        channel = await guild.create_text_channel(f"ticket-{interaction.user.name}", category=category, overwrites=overwrites)
        await channel.send(f"{interaction.user.mention} تم فتح تذكرتك!", view=CloseView())
        await interaction.followup.send(f"تم فتح تذكرتك: {channel.mention}", ephemeral=True)
    embed = discord.Embed(title="الدعم الفني", description="اضغط الزر لفتح تذكرة", color=discord.Color.blue())
    await ctx.send(embed=embed, view=TicketView())

@bot.event
async def on_ready():
    bot.add_view(TicketView())
    bot.add_view(CloseView())
    print(f"شغال: {bot.user}")

bot.run(os.getenv("DISCORD_TOKEN"))
