from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ContextTypes

# আপনার GitHub Pages-এর লাইভ URL
WEB_APP_URL = "https://asik93.github.io/paygaid-app/"

async def show_dashboard_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    
    # স্ক্রিনশটের মতো বাটনের তালিকা
    keyboard = [
        [InlineKeyboardButton("👤 Become an Agent", callback_data="menu_become_agent")],
        [InlineKeyboardButton("🔑 Agent Login", web_app=WebAppInfo(url=WEB_APP_URL))],  # ২ নম্বর অপশনে মিনি অ্যাপ
        [InlineKeyboardButton("📋 Program Overview", callback_data="menu_overview")],
        [InlineKeyboardButton("🛡️ Eligibility Criteria", callback_data="menu_eligibility")],
        [InlineKeyboardButton("📜 Terms & Conditions", callback_data="menu_terms")],
        [InlineKeyboardButton("❓ Frequently Asked Questions", callback_data="menu_faq")],
        [InlineKeyboardButton("🎧 Contact Support", callback_data="menu_support")],
        [InlineKeyboardButton("🌐 Change Language", callback_data="menu_change_language")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # স্ক্রিনশটের মতো ওয়েলকাম মেসেজ
    dashboard_text = (
        "**Welcome to PayGaid**\n\n"
        "Your trusted Payment Gateway & E-Wallet Agent Platform.\n\n"
        "Explore our program, check requirements, or submit your application."
    )
    
    if query:
        await query.edit_message_text(dashboard_text, reply_markup=reply_markup, parse_mode="Markdown")
    elif update.message:
        await update.message.reply_text(dashboard_text, reply_markup=reply_markup, parse_mode="Markdown")


async def handle_dashboard_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "menu_change_language":
        from page2_language import show_language_page
        await show_language_page(update, context)
    elif data == "menu_become_agent":
        await query.message.reply_text("📝 **Become an Agent**\n\nঅ্যাপ্লিকেশন জমা দিতে রেজিস্টার বাটনে ক্লিক করুন।")
    elif data == "menu_overview":
        await query.message.reply_text("📋 **Program Overview**\n\nPayGaid এজেন্ট প্রোগ্রাম সম্পর্কে বিস্তারিত তথ্য এখানে থাকবে।")
    elif data == "menu_eligibility":
        await query.message.reply_text("🛡️ **Eligibility Criteria**\n\nএজেন্ট হওয়ার যোগ্যতা ও প্রয়োজনীয় তথ্যাবলী।")
    elif data == "menu_terms":
        await query.message.reply_text("📜 **Terms & Conditions**\n\nশর্তাবলী পড়ুন।")
    elif data == "menu_faq":
        await query.message.reply_text("❓ **Frequently Asked Questions**\n\nসাধারণ প্রশ্নোত্তর।")
    elif data == "menu_support":
        await query.message.reply_text("🎧 **Contact Support**\n\nআমাদের সাপোর্ট টিমের সাথে যোগাযোগ করুন: @support_username")
    else:
        await query.message.reply_text("🚧 কাজ চলছে...")