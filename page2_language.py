from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from page1_start import COUNTRIES

async def show_language_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    
    selected_code = context.user_data.get('country_code', 'BD')
    country_info = COUNTRIES.get(selected_code, COUNTRIES['BD'])
    
    keyboard = [
        [InlineKeyboardButton(f"{country_info['lang_flag']} {country_info['native_lang']}", callback_data="select_lang_native")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="select_lang_en")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        "**Select Language**\n"
        "Choose your preferred operating language"
    )
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def handle_language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    selected_code = context.user_data.get('country_code', 'BD')
    country_info = COUNTRIES.get(selected_code, COUNTRIES['BD'])
    
    if data == "select_lang_native":
        context.user_data['selected_language'] = country_info['native_lang']
    elif data == "select_lang_en":
        context.user_data['selected_language'] = "English"
        
    # ভাষা নির্বাচন শেষে সরাসরি ৩ নম্বর ড্যাশবোর্ড পেজে পাঠাবে
    from page3_dashboard import show_dashboard_page
    await show_dashboard_page(update, context)