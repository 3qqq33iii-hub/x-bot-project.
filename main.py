import os, telebot, random
from PIL import Image
from moviepy.editor import VideoFileClip

# --- الإعدادات ---
TELEGRAM_TOKEN = '8605234517:AAFOhiU8v5zjbyB5CJYccyMQvZmguAOLGLY' 
bot = telebot.TeleBot(TELEGRAM_TOKEN)

FILTER_WORDS = {"موت": "مـ.ـوت", "قتل": "قـ.ـتل", "دم": "د.ماء", "رابط": "الرابط 🔗"}
TAGS = ["#ترند", "#تويتر", "#اكسبلور"]

def optimize_text(text):
    for word, rep in FILTER_WORDS.items(): text = text.replace(word, rep)
    return f"{text}\n\n📍 محتوى يستحق التأمل.. ✨\n{' '.join(random.sample(TAGS, 2))}"

@bot.message_handler(content_types=['text'])
def h_text(m):
    final = optimize_text(m.text)
    bot.send_message(m.chat.id, f"✅ **جاهز للنسخ:**\n\n```\n{final}\n```", parse_mode="Markdown")

@bot.message_handler(content_types=['photo'])
def h_photo(m):
    f_info = bot.get_file(m.photo[-1].file_id)
    with open("i.jpg", "wb") as f: f.write(bot.download_file(f_info.file_path))
    with Image.open("i.jpg") as img: img.convert("RGB").save("o.jpg", quality=93)
    cap = optimize_text("صورة حصرية")
    with open("o.jpg", "rb") as f: bot.send_photo(m.chat.id, f, caption=f"✅ بصمة جديدة!\n`{cap}`", parse_mode="Markdown")
    os.remove("i.jpg"); os.remove("o.jpg")

@bot.message_handler(content_types=['video'])
def h_video(m):
    wait = bot.reply_to(m, "🎥 معالجة وضغط الفيديو...")
    f_info = bot.get_file(m.video.file_id)
    with open("vi.mp4", "wb") as f: f.write(bot.download_file(f_info.file_path))
    clip = VideoFileClip("vi.mp4")
    new = clip.subclip(0, clip.duration - 0.2)
    # ضغط الحجم لضمان الإرسال (حل مشكلة file is too big)
    new.write_videofile("vo.mp4", codec="libx264", bitrate="1200k", audio_codec="aac", logger=None)
    clip.close(); new.close()
    cap = optimize_text("فيديو حصري")
    with open("vo.mp4", "rb") as f: bot.send_video(m.chat.id, f, caption=f"✅ تم الضغط والفلترة!\n`{cap}`", parse_mode="Markdown")
    os.remove("vi.mp4"); os.remove("vo.mp4")

print("🚀 يعمل!")
bot.polling(none_stop=True)
