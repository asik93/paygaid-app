from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ContextTypes

# Apnar VPS server-er live WEB_APP_URL update kora holo
WEB_APP_URL = "https://66.29.134.253"

async def show_dashboard_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    
    # Screen-er moto button-er talika
    keyboard = [
        [InlineKeyboardButton("👤 Become an Agent", callback_data="menu_become_agent")],
        [InlineKeyboardButton("🔑 Agent Login", web_app=WebAppInfo(url=WEB_APP_URL))],  # Mini App URL updated to VPS IP
        [InlineKeyboardButton("📋 Program Overview", callback_data="menu_overview")],
        [InlineKeyboardButton("🛡️ Eligibility Criteria", callback_data="menu_eligibility")],
        [InlineKeyboardButton("📜 Terms & Conditions", callback_data="menu_terms")],
        [InlineKeyboardButton("❓ Frequently Asked Questions", callback_data="menu_faq")],
        [InlineKeyboardButton("🎧 Contact Support", callback_data="menu_support")],
        [InlineKeyboardButton("🌐 Change Language", callback_data="menu_change_language")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Welcome message
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
        await query.message.reply_text("📝 **Become an Agent**\n\nApplication joma dite register button-e click korun.")
    elif data == "menu_overview":
        await query.message.reply_text("📋 **Program Overview**\n\nPayGaid agent program somporke bistarito tothyo ekhane thakbe.")
    elif data == "menu_eligibility":
        await query.message.reply_text("🛡️ **Eligibility Criteria**\n\nAgent howar jogota o proyojonio tothya boli.")
    elif data == "menu_terms":
        await query.message.reply_text("📜 **Terms & Conditions**\n\nSorthaboli porun.")
    elif data == "menu_faq":
        await query.message.reply_text("❓ **Frequently Asked Questions**\n\nSadharon prosnottor.")
    elif data == "menu_support":
        await query.message.reply_text("🎧 **Contact Support**\n\nAmader support team-er sathe jogajog korun: @support_username")
    else:
        await query.message.reply_text("🚧 Kaj cholche...")