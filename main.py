import os
import telebot
import random
from PIL import Image
from moviepy.editor import VideoFileClip

# --- الإعدادات ---
# ضع التوكن الخاص بك بين العلامتين '' في السطر التالي
CH_TOKEN = '8605234517:AAFOhiU8v5zjbyB5CJYccyMQvZmguAOLGLY' 
bot = telebot.TeleBot(CH_TOKEN)

FILTER_WORDS = {"الرابط": "رابط", "دماء": "دم", "قـ.ـتل": "قتال", "صـ.ـوت": "صوت"}
TAGS = ["#اكسبلور", "#تويتر", "#ترند"]

def optimize_text(text):
    for word, rep in FILTER_WORDS.items():
        text = text.replace(word, rep)
    return f"{text}\n\n✨ محتوى يستحق التأمل ✨\n{' '.join(random.sample(TAGS, 2))}"

@bot.message_handler(content_types=['text'])
def text_msg(m):
    final = optimize_text(m.text)
    bot.send_message(m.chat.id, f"✅ **جاهز للنسخ:**\n\n```{final}```", parse_mode="Markdown")

@bot.message_handler(content_types=['photo'])
def handle_photo(m):
    file_info = bot.get_file(m.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("i.jpg", "wb") as f:
        f.write(downloaded_file)
    
    # تغيير البصمة الرقمية للصورة
    img = Image.open("i.jpg").convert("RGB")
    img.save("o.jpg", "JPEG", quality=93)
    
    cap = optimize_text(m.caption if m.caption else "صورة حصرية")
    with open("o.jpg", "rb") as f:
        bot.send_photo(m.chat.id, f, caption=f"✅ **بصمة جديدة**\n\n{cap}", parse_mode="Markdown")
    os.remove("i.jpg")
    os.remove("o.jpg")

@bot.message_handler(content_types=['video'])
def handle_video(m):
    bot.send_message(m.chat.id, "⏳ جاري معالجة الفيديو وضغطه لتجاوز القيود...")
    file_info = bot.get_file(m.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("vi.mp4", "wb") as f:
        f.write(downloaded_file)

    # معالجة الفيديو: ضغط الحجم وتغيير البصمة
    clip = VideoFileClip("vi.mp4")
    new_clip = clip.subclip(0, clip.duration - 0.1) # تغيير بسيط جداً في الوقت لتغيير البصمة
    
    # السطر التالي هو المسؤول عن حل مشكلة "File too big" عبر تحديد جودة الإرسال
    new_clip.write_videofile("vo.mp4", codec="libx264", bitrate="1200k", audio_codec="aac")
    
    cap = optimize_text(m.caption if m.caption else "فيديو حصري")
    with open("vo.mp4", "rb") as f:
        bot.send_video(m.chat.id, f, caption=f"✅ **تم الضغط والفلترة**\n\n{cap}", parse_mode="Markdown")
    
    clip.close()
    new_clip.close()
    os.remove("vi.mp4")
    os.remove("vo.mp4")

print("🚀 البوت يعمل الآن...")
bot.polling(none_stop=True)
