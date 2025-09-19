import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, Bot, WebAppInfo
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    CallbackContext,
    ConversationHandler
)

# আপনার বট টোকেন এবং চ্যানেল আইডি
BOT_TOKEN = "8245233994:AAHkeQIHd1M3yjJmfiW6iu_vTq5s4o3HovY"
MAIN_CHANNEL_ID = -1002460901479 # মূল প্রাইভেট চ্যানেল
ADMIN_NOTIFY_CHANNEL_ID = -1002787846366 # অ্যাডমিন নোটিফিকেশনের জন্য দ্বিতীয় চ্যানেল

# অ্যাডমিনের ইউজারনেম, ওয়েবসাইটের লিঙ্ক এবং ভিআইপি গ্রুপের লিঙ্ক
ADMIN_USERNAME = "rs_rezaul_99"
HACK_WEBSITE_URL = "https://zesty-kelpie-7f5595.netlify.app/"
VIP_GROUP_LINK = "vip group link"
REFERRAL_LINK = "https://dkwin12.com/#/register?invitationCode=82626111964"

# ConversationHandler এর জন্য স্টেট
AWAITING_UID = 1

# লগিং কনফিগারেশন
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

async def check_member(user_id: int, bot: Bot) -> bool:
    """
    যাচাই করে যে ব্যবহারকারী মূল চ্যানেলের সদস্য কিনা।
    """
    try:
        member = await bot.get_chat_member(chat_id=MAIN_CHANNEL_ID, user_id=user_id)
        return member.status in ['member', 'creator', 'administrator']
    except Exception as e:
        logging.error(f"Error checking channel member: {e}")
        return False

async def start(update: Update, context: CallbackContext) -> None:
    """
    যখন ব্যবহারকারী /start কমান্ড ব্যবহার করবে।
    """
    user = update.effective_user
    is_member = await check_member(user.id, context.bot)

    if not is_member:
        # যদি ব্যবহারকারী চ্যানেলের সদস্য না হয়
        keyboard = [
            [InlineKeyboardButton("রেজিস্ট্রেশন করুন", url=REFERRAL_LINK)],
            [InlineKeyboardButton("UID পাঠান", callback_data="send_uid")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"🚫 **ACCESS DENIED!**\n\nআপনি আমাদের **𝑨𝑺 𝑶𝑭𝑭𝑰𝑪𝑰𝑨𝑳 𝑪𝑯𝑨𝑵𝑵𝑬𝑳** এর একজন ভিআইপি সদস্য নন, তাই এই বটটি আপনার জন্য নয়।\n\nযদি আপনি আমাদের রেফারে অ্যাকাউন্ট খুলে থাকেন কিন্তু এখনও টিমে যুক্ত না হয়ে থাকেন, তাহলে আপনার **UID** পাঠিয়ে যাচাই করে নিতে পারেন।",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return

    # যদি ব্যবহারকারী চ্যানেলের সদস্য হয়
    keyboard = [
        [InlineKeyboardButton("ওপেন হ্যাক", web_app=WebAppInfo(url=HACK_WEBSITE_URL))],
        [InlineKeyboardButton("Rules", callback_data="show_rules")],
        [InlineKeyboardButton("Tutorials", callback_data="show_tutorials")],
        [InlineKeyboardButton("এডমিনের সাথে যোগাযোগ করুন", url=f"https://t.me/{ADMIN_USERNAME}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"💎 স্বাগতম, {user.first_name}!\n\nআপনি **𝑨𝑺 𝑶𝑭𝑭𝑰𝑪𝑰𝑨𝑳 𝑪𝑯𝑨𝑵𝑵𝑬𝑳** টিমের একজন বিশেষ সদস্য। আপনার সুবিধার জন্য নিচে কিছু গুরুত্বপূর্ণ অপশন দেওয়া হলো। আশা করি, আপনি আমাদের সাথে কাজ করে আনন্দ পাবেন।",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def start_uid_submission(update: Update, context: CallbackContext) -> int:
    """
    UID পাঠানোর প্রক্রিয়া শুরু করে।
    """
    await update.callback_query.message.reply_text(
        "অনুগ্রহ করে আপনার **𝑨𝑺 𝑶𝑭𝑭𝑰𝑪𝑰𝑨𝑳 𝑪𝑯𝑨𝑵𝑵𝑬𝑳** অ্যাকাউন্টের UID নম্বরটি দিন।"
    )
    return AWAITING_UID

async def receive_uid(update: Update, context: CallbackContext) -> int:
    """
    ব্যবহারকারীর পাঠানো UID গ্রহণ করে এবং অ্যাডমিনকে নোটিফিকেশন পাঠায়।
    """
    user_uid = update.message.text
    user = update.effective_user
    
    # অ্যাডমিন চ্যানেলে নোটিফিকেশন পাঠানো।
    keyboard = [
        [InlineKeyboardButton("✅ Confirm", callback_data=f"confirm_{user.id}_{user_uid}"),
         InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(
        chat_id=ADMIN_NOTIFY_CHANNEL_ID,
        text=f"**নতুন সদস্যের অনুরোধ**\n\nব্যবহারকারী: {user.first_name} (@{user.username})\nপ্রদত্ত UID: `{user_uid}`",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    
    await update.message.reply_text(
        "আপনার UID পাঠানো হয়েছে! আমাদের টিম দ্রুত এটি যাচাই করে আপনাকে জানাবে।"
    )
    
    return ConversationHandler.END

async def cancel_uid_submission(update: Update, context: CallbackContext) -> int:
    """
    UID সাবমিশন প্রক্রিয়া বাতিল করে।
    """
    await update.message.reply_text("ইউআইডি সাবমিশন বাতিল করা হয়েছে।")
    return ConversationHandler.END

async def handle_admin_action(update: Update, context: CallbackContext) -> None:
    """
    অ্যাডমিন Confirm বা Reject বাটনে ক্লিক করলে এই ফাংশনটি কাজ করবে।
    """
    query = update.callback_query
    await query.answer()

    action = query.data.split('_')[0]
    user_id = int(query.data.split('_')[1])
    
    try:
        if action == "confirm":
            await context.bot.send_message(
                chat_id=user_id,
                text=f"✅ **অনুমোদিত!**\n\nঅভিনন্দন! আপনার **𝑨𝑺 𝑶𝑭𝑭𝑰𝑪𝑰𝑨𝑳 𝑪𝑯𝑨𝑵𝑵𝑬𝑳** অ্যাকাউন্টের যাচাই সম্পন্ন হয়েছে। আপনি এখন আমাদের টিমের একজন ভিআইপি সদস্য। এই লিঙ্কে ক্লিক করে এখনই আমাদের ভিআইপি গ্রুপে যুক্ত হয়ে যান: {VIP_GROUP_LINK}",
                parse_mode='Markdown'
            )
            await query.edit_message_text(f"✅ অনুমোদিত। ইউআইডি: {query.data.split('_')[2]}।")
        
        elif action == "reject":
            await context.bot.send_message(
                chat_id=user_id,
                text=f"❌ **অনুমোদন বাতিল!**\n\nদুঃখিত! আপনার **UID** আমাদের টিমের রেফারেল থেকে তৈরি হয়নি। অনুগ্রহ করে এই লিঙ্ক ব্যবহার করে একটি নতুন অ্যাকাউন্ট তৈরি করুন: {REFERRAL_LINK}",
                parse_mode='Markdown'
            )
            await query.edit_message_text("❌ প্রত্যাখ্যান করা হয়েছে।")

    except Exception as e:
        logging.error(f"Error sending message to user {user_id}: {e}")
        await query.edit_message_text("❌ ব্যবহারকারীকে বার্তা পাঠানো যায়নি।")

async def show_rules(update: Update, context: CallbackContext) -> None:
    """
    ব্যবহারকারী যখন 'Rules' বাটনে ক্লিক করবে।
    """
    query = update.callback_query
    await query.answer()
    
    rules_text = (
        "📜 **𝑨𝑺 𝑶𝑭𝑭𝑰𝑪𝑰𝑨𝑳 𝑪𝑯𝑨𝑵𝑵𝑬𝑳 টিমের নিয়মাবলী:**\n\n"
        "১. এই বটটি শুধুমাত্র **𝑨𝑺 𝑶𝑭𝑭𝑰𝑪𝑰𝑨𝑳 𝑪𝑯𝑨𝑵𝑵𝑬𝑳** টিমের সদস্যদের জন্য।\n"
        "২. বটের কোনো অপশন অপব্যবহার করা যাবে না।\n"
        "৩. কোনো সমস্যা হলে এডমিনের সাথে যোগাযোগ করুন।\n"
        "৪. বটের মাধ্যমে প্রাপ্ত যেকোনো তথ্য বা টুলস ব্যক্তিগত ব্যবহারের জন্য এবং গোপন রাখতে হবে।"
    )
    await query.message.reply_text(rules_text, parse_mode='Markdown')

async def show_tutorials(update: Update, context: CallbackContext) -> None:
    """
    ব্যবহারকারী যখন 'Tutorials' বাটনে ক্লিক করবে।
    """
    query = update.callback_query
    await query.answer()
    
    await query.message.reply_text("এখানে টিউটোরিয়াল বা শিক্ষামূলক রিসোর্স সম্পর্কিত তথ্য থাকবে।")

def main() -> None:
    """
    বটটি শুরু করার জন্য মূল ফাংশন।
    """
    application = Application.builder().token(BOT_TOKEN).build()

    # ConversationHandler তৈরি করা
    uid_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_uid_submission, pattern="^send_uid$")],
        states={
            AWAITING_UID: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_uid)]
        },
        fallbacks=[CommandHandler("cancel", cancel_uid_submission)]
    )

    # বিভিন্ন হ্যান্ডলার যোগ করা
    application.add_handler(CommandHandler("start", start))
    application.add_handler(uid_handler)
    application.add_handler(CallbackQueryHandler(show_rules, pattern="^show_rules$"))
    application.add_handler(CallbackQueryHandler(show_tutorials, pattern="^show_tutorials$"))
    application.add_handler(CallbackQueryHandler(handle_admin_action, pattern="^(confirm|reject)_"))

    application.run_polling()

if __name__ == "__main__":
    main()

