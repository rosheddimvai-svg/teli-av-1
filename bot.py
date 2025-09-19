import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, Bot
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    CallbackContext,
    ConversationHandler
)

# আপনার বট টোকেন এবং চ্যানেল আইডি এখানে দিন।
BOT_TOKEN = "8197222627:AAGjX1XrAqlNnpMYpjSKjA4yOisfeTJbQEk"
MAIN_CHANNEL_ID = -1002323042564 # মূল প্রাইভেট চ্যানেল
ADMIN_NOTIFY_CHANNEL_ID = -1002787846366 # অ্যাডমিন নোটিফিকেশনের জন্য দ্বিতীয় চ্যানেল

# অ্যাডমিনের ইউজারনেম, ওপেন হ্যাক ওয়েবসাইটের লিঙ্ক এবং ভিআইপি গ্রুপের লিঙ্ক
ADMIN_USERNAME = "rs_rezaul_99"
HACK_WEBSITE_URL = "https://as-official-channel.netlify.app/"
VIP_GROUP_LINK = "https://t.me/+WBrUuuuIn2IwMjg1"
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
        # যদি ব্যবহারকারী চ্যানেলের সদস্য না হয়, তবে এই বার্তাটি দেখাবে।
        keyboard = [
            [InlineKeyboardButton("যোগাযোগ করুন", url=f"https://t.me/{ADMIN_USERNAME}")],
            [InlineKeyboardButton("UID পাঠান", callback_data="send_uid")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"🚫 **ACCESS DENIED!**\n\nআপনি আমাদের ভিআইপি কমিউনিটির সদস্য নন। এই বটটি শুধুমাত্র আমাদের **DKWIN** টিমের সদস্যদের জন্য তৈরি করা হয়েছে।\n\nআপনি যদি আমাদের রেফারে অ্যাকাউন্ট তৈরি করেও আমাদের টিমে যুক্ত হননি, তাহলে আপনার ইউআইডি পাঠাতে নিচের বাটনে ক্লিক করুন।",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return

    # যদি ব্যবহারকারী চ্যানেলের সদস্য হয়, তবে এই বার্তাটি এবং মেনু দেখাবে।
    keyboard = [
        [InlineKeyboardButton("ওপেন হ্যাক", url=HACK_WEBSITE_URL)],
        [InlineKeyboardButton("Rules", callback_data="show_rules")],
        [InlineKeyboardButton("Tutorials", callback_data="show_tutorials")],
        [InlineKeyboardButton("এডমিনের সাথে যোগাযোগ করুন", url=f"https://t.me/{ADMIN_USERNAME}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"💎 স্বাগতম, {user.first_name}!\n\nআপনি **DKWIN** টিমের একজন সম্মানিত ভিআইপি সদস্য। আপনার সুবিধার জন্য নিচের অপশনগুলো থেকে বেছে নিন।",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def start_uid_submission(update: Update, context: CallbackContext) -> int:
    """
    UID পাঠানোর প্রক্রিয়া শুরু করে।
    """
    await update.callback_query.message.reply_text(
        "অনুগ্রহ করে আপনার **DKWIN** ইউআইডিটি পাঠান।"
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
        text=f"**নতুন UID সাবমিশন**\n\nব্যবহারকারী: {user.first_name} (@{user.username})\nUID: `{user_uid}`",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    
    await update.message.reply_text(
        "আপনার ইউআইডি পাঠানো হয়েছে। অ্যাডমিনের অনুমোদনের জন্য অপেক্ষা করুন। আপনার অনুরোধটি প্রক্রিয়া করা হলে আপনাকে জানানো হবে।"
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
    
    # ব্যবহারকারীকে ব্যক্তিগতভাবে বার্তা পাঠাতে
    try:
        if action == "confirm":
            await context.bot.send_message(
                chat_id=user_id,
                text=f"✅ **অভিনন্দন!**\n\nআপনার **DKWIN** অ্যাকাউন্টের অ্যাক্সেস অনুমোদিত হয়েছে। আপনি এখন **DKWIN** টিমের একজন ভিআইপি সদস্য। আমাদের ভিআইপি গ্রুপে যোগ দিতে নিচের লিঙ্কে ক্লিক করুন:\n\n{VIP_GROUP_LINK}",
                parse_mode='Markdown'
            )
            await query.edit_message_text(f"✅ অনুমোদিত। ইউআইডি: {query.data.split('_')[2]}।")
        
        elif action == "reject":
            await context.bot.send_message(
                chat_id=user_id,
                text=f"❌ **দুঃখিত!**\n\nআপনার অ্যাক্সেস প্রত্যাখ্যান করা হয়েছে। আপনার অ্যাকাউন্টটি আমাদের রেফারের মাধ্যমে তৈরি করা হয়নি। দয়া করে নিচের লিংকের মাধ্যমে একটি নতুন অ্যাকাউন্ট তৈরি করুন:\n\n{REFERRAL_LINK}",
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
        "📜 **DKWIN বট ব্যবহারের নিয়মাবলী:**\n\n"
        "১. এই বটটি শুধুমাত্র **DKWIN** টিমের সদস্যদের জন্য।\n"
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

    # বিভিন্ন হ্যান্ডলার যোগ করা।
    application.add_handler(CommandHandler("start", start))
    application.add_handler(uid_handler)
    application.add_handler(CallbackQueryHandler(show_rules, pattern="^show_rules$"))
    application.add_handler(CallbackQueryHandler(show_tutorials, pattern="^show_tutorials$"))
    application.add_handler(CallbackQueryHandler(handle_admin_action, pattern="^(confirm|reject)_"))

    application.run_polling()

if __name__ == "__main__":
    main()