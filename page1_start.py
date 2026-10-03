from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# দেশ এবং দেশের স্থানীয় ভাষার তালিকা
COUNTRIES = {
    "IN": {"name": "🇮🇳 India", "currency": "INR", "native_lang": "हिन्दी (Hindi)", "lang_flag": "🇮🇳"},
    "PK": {"name": "🇵🇰 Pakistan", "currency": "PKR", "native_lang": "اردو (Urdu)", "lang_flag": "🇵🇰"},
    "NP": {"name": "🇳🇵 Nepal", "currency": "NPR", "native_lang": "नेपाली (Nepali)", "lang_flag": "🇳🇵"},
    "PH": {"name": "🇵🇭 Philippines", "currency": "PHP", "native_lang": "Tagalog", "lang_flag": "🇵🇭"},
    "BD": {"name": "🇧🇩 Bangladesh", "currency": "BDT", "native_lang": "বাংলা (Bangla)", "lang_flag": "🇧🇩"},
    "VN": {"name": "🇻🇳 Vietnam", "currency": "VND", "native_lang": "Tiếng Việt", "lang_flag": "🇻🇳"},
    "TH": {"name": "🇹🇭 Thailand", "currency": "THB", "native_lang": "ไทย (Thai)", "lang_flag": "🇹🇭"},
    "MY": {"name": "🇲🇾 Malaysia", "currency": "MYR", "native_lang": "Bahasa Melayu", "lang_flag": "🇲🇾"},
    "ID": {"name": "🇮🇩 Indonesia", "currency": "IDR", "native_lang": "Bahasa Indonesia", "lang_flag": "🇮🇩"},
    "UAE": {"name": "🇦🇪 UAE", "currency": "AED", "native_lang": "العربية (Arabic)", "lang_flag": "🇦🇪"},
    "SA": {"name": "🇸🇦 Saudi Arabia", "currency": "SAR", "native_lang": "العربية (Arabic)", "lang_flag": "🇸🇦"},
    "QA": {"name": "🇶🇦 Qatar", "currency": "QAR", "native_lang": "العربية (Arabic)", "lang_flag": "🇶🇦"},
}

async def start_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    for code, data in COUNTRIES.items():
        keyboard.append([InlineKeyboardButton(data["name"], callback_data=f"select_country_{code}")])
        
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "**Welcome**\n"
        "Select your Country & Language"
    )
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.message.edit_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")