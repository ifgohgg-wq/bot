import discord
from discord.ext import commands
from discord import app_commands
import os
import json

if interaction.user.id!= OWNER_ID:1522144542927622149 = 1522144542927622149 # <-- حط الايدي حقك هنا

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# تخزين الردود
if not os.path.exists("data.json"):
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump({"auto_reply": [], "mirror_rooms": {}}, f, ensure_ascii=False)

def load_data():
    with open("data.json", "r", encoding="utf-8") as f:
        return json.load(f)
def save_data(d):
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

# ===== حماية البوت نفسه =====
@bot.check
async def is_not_blocked(ctx):
    return True

# ===== نظام الحماية للسيرفر =====
spam = {}
@bot.event
async def on_message(message):
    if message.author.bot: return

    # حماية سبام بسيطة
    uid = message.author.id
    # (نطورها بعدين)

    data = load_data()

    # 1. نظام الروم المرآة: اي رسالة في روم محدد يرد البوت بنفسها
    if str(message.channel.id) in data["mirror_rooms"]:
        reply_text = data["mirror_rooms"][str(message.channel.id)]
        await message.channel.send(reply_text)
        return

    # 2. الرد التلقائي المتطور
    for rule in data["auto_reply"]:
        content = message.content
        target = rule["trigger"]
        mode = rule["mode"] # contains, exact, starts
        matched = False
        if mode == "contains" and target in content: matched = True
        if mode == "exact" and target == content: matched = True
        if mode == "starts" and content.startswith(target): matched = True
        if matched:
            await message.channel.send(rule["response"])
            break

    await bot.process_commands(message)

# ===== سلاش: تحديد روم مرآة =====
@bot.tree.command(name="تحديد-روم", description="خلي البوت يرد برساله ثابته في روم معين")
@app_commands.describe(روم="اختر الروم", رسالة="الرسالة اللي يرد فيها")
async def mirror(interaction: discord.Interaction, روم: discord.TextChannel, رسالة: str):
    if if interaction.user.id!= OWNER_ID:1522144542927622149= OWNER_ID:
        await interaction.response.send_message("مو مسموح لك", ephemeral=True); return
    data = load_data()
    data["mirror_rooms"][str(روم.id)] = رسالة
    save_data(data)
    await interaction.response.send_message(f"تم! اي احد يكتب في {روم.mention} برد عليه: {رسالة}", ephemeral=True)

# ===== سلاش: رد تلقائي متطور =====
@bot.tree.command(name="رد-تلقائي", description="اضافة رد تلقائي")
@app_commands.describe(الكلمة="الكلمة المحفزة", الرد="رد البوت", النوع="طريقة المطابقة")
@app_commands.choices(النوع=[
    app_commands.Choice(name="يحتوي الكلمة", value="contains"),
    app_commands.Choice(name="الكلمة بالضبط", value="exact"),
    app_commands.Choice(name="يبدأ بالكلمة", value="starts"),
])
async def autoreply(interaction: discord.Interaction, الكلمة: str, الرد: str, النوع: app_commands.Choice[str]):
    if interaction.user.id!= interaction.user.id:1522144542927622149
        await interaction.response.send_message("مو مسموح لك", ephemeral=True); return
    data = load_data()
    data["auto_reply"].append({"trigger": الكلمة, "response": الرد, "mode": النوع.value})
    save_data(data)
    await interaction.response.send_message(f"تم اضافة رد: اذا كتب `{الكلمة}` ({النوع.name}) ارد `{الرد}`", ephemeral=True)

# ===== اوامر ميمز =====
@bot.tree.command(name="نكتة", description="نكتة عشوائية")
async def joke(interaction: discord.Interaction):
    import random
    jokes = ["مرة واحد اشترى مظلة... ليش؟ عشان يمشي تحت المطر وهو مرتاح", "ليش الكمبيوتر زعلان؟ عشان انضرب فيروس"]
    await interaction.response.send_message(random.choice(jokes))

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"شغال: {bot.user}")

bot.run(os.getenv("TOKEN"))
