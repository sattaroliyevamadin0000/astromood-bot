import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

TOKEN = "9138686226:AAG1zSySaPkPBAJmyDYQuNxO8fwIryxj628"

bot = Bot(token=TOKEN)
dp = Dispatcher()

class UserState(StatesGroup):
    waiting_for_name = State()
    main_menu = State()
    waiting_for_wish = State()

auras = {
    "🟢 Zumrad Zamin Auralari": "Sizning ruhiyatingiz hozir koinotning eng sokin burchagidek xotirjam. Atrofingizga yangilanish va shifo energiyasini ulashyapsiz. 🌿✨",
    "🔮 Kosmik Binafsha Aura": "Sizning tafakkuringiz bugun yulduzlararo sayohatda! O'zgacha g'oyalar, yashirin qobiliyatlar va ilhom qalbingizni qamrab olgan. 🌌🔮",
    "☀️ Quyosh Oltin Auralari": "Ichki quyoshingiz shunchalik yorqinki, u nafaqat sizni, balki yo'lingizdagi barcha soyalarni nurga to'ldiryapti! ☀️👑",
    "🌊 Sehrli Safir Moviy Aura": "Siz dunyoning barcha shovqinidan balandda — o'z qalbingiz okeanining eng tinch va sirli tubida huzur topgansiz. 🌊💎"
}

fortunes = [
    "Bugun koinot siz uchun maxsus eshikni ochadi — kutilmagan, yuragingizni quvonchga to'ldiruvchi xabar keladi! 💌✨",
    "Siz boshlagan har bir kichik qadam bugun ulkan yulduzli g'alabaning tamal toshiga aylanadi! 🏆🌠",
    "Sizdagi samimiy tabassum bugun kimningdir og'ir kunini nurga to'ldiradi. Siz olam uchun mo'jizasisiz! 💫",
    "Yulduzlar pichirlaydi: bugun o'zingiz istagan eng go'zal orzu haqida o'ylab, osmonga boqing — u amalga oshish yo'lini boshladi! 🌙💡"
]

astro_photos = [
    {
        "title": "🌌 Yulduzli Tungi Osmon va Galaktika",
        "photo": "https://images.unsplash.com/photo-1506703719100-a0f3a48c0f86?w=800",
        "desc": "Koinotning cheksiz sukunati va yulduzlar jilosi."
    },
    {
        "title": "🌙 Sehrli Oy Nuridagi Istaklar",
        "photo": "https://images.unsplash.com/photo-1532693322450-cb65e5ae0149?w=800",
        "desc": "Tun sukunati va qalbdagi eng ezgu niyatlar."
    },
    {
        "title": "✨ Kosmik Tulki va Yulduzlar",
        "photo": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800",
        "desc": "Sehrli ertaklar olami va iliq nurlar."
    },
    {
        "title": "🌠 Olam va Ichki Orom",
        "photo": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800",
        "desc": "Yulduzlararo sayohat va cheksiz ilhom."
    },
    {
        "title": "🪐 Saturn va Yulduzlar Jilosi",
        "photo": "https://images.unsplash.com/photo-1614728894747-a83421e2b9c9?w=800",
        "desc": "Koinotning sirli sayyoralari va cheksizlik."
    },
    {
        "title": "💫 Sehrli Koinot Nur Guldasi",
        "photo": "https://images.unsplash.com/photo-1507499739999-097706ad8914?w=800",
        "desc": "Qalbingizni yorug'lik va iliqlikka to'ldiruvchi manzara."
    }
]

teas = [
    "🌿 **Yalpizli Ko'k Choy + Qora Shokolad:** Fikrlaringizni jamlab, miyangizga tiniqlik baxsh etuvchi sehrli tanlov.",
    "🍋 **Limonli Za'faron Choyi + Asalli Pechene:** Kayfiyatingizni bir zumda quyoshdek yorqin qiladi.",
    "☕ **Sutli Vanil Latte + Issiq Kruassan:** Ertalabki ilhom, shinamlik va quvvat manbai!",
    "🍓 **Atirgulli Muzdek Oq Choy + Makaron shirinligi:** Nafis ta'm va yengil kayfiyat ulashadi.",
    "🍫 **Issiq Shokolad + Marshmallow + Krem:** Qalbingizni isituvchi va ertaknamo muhit yaratuvchi tanlov."
]

affirmations = [
    "✨ \"Men o'z hayotining ilhomlantiruvchi rassomiman va har bir kunimni mo'jizaga boyitaman.\"",
    "💫 \"Menda barcha to'siqlarni yengib, yulduzlarga erishish uchun ulkan kuch bor.\"",
    "🌟 \"Men har soniyada baxtga, xotirjamlikka va ulkan muvaffaqiyatga loyiqman.\"",
    "🌠 \"Koinot doimo mening foydamga ishlaydi va menga eng yaxshi imkoniyatlarni taqdim etmoqda.\""
]

magic_advices = [
    "🔮 *Sehrli Shar sirlashadi:* Bugun o'zingizga qattiq talab qo'ymang. Ba'zan eng buyuk kashfiyotlar shunchaki derazadan tashqariga qarab, iliq choy xo'plaganda tug'iladi. 🍵✨",
    "🔮 *Sehrli Shar pichirlaydi:* Atrofdagilarning fikri — bu shunchaki fon musiqasi. Sizning qalbingizda esa o'zingizning betakror simfoniyangiz yangramoqda. Uni tinglang! 🎶💫",
    "🔮 *Sehrli Shar ko'rsatmoqda:* Bugun kutilmagan bir inson sizga iliq so'z aytadi yoki tabassum hadya qiladi. Unga yuragingizni oching! 🌠💛",
    "🔮 *Sehrli Shar maslahati:* Agar qalbingiz charchasa, telefondan biroz uzoqlashib, osmonga boqing. Koinot sizga o'z sukunatidan kuch beradi. 🌌🕊️"
]

star_portals = [
    "🌌 **Yulduzlar Portali:** Bugun koinot sizga o'zining yashirin energiyasini yo'llamoqda. Tasavvur qiling: siz ulkan yulduz turkumining markazidasiz va barcha istaklaringiz osonlikcha amalga oshmoqda. ✨",
    "🌠 **Kosmik Portal siri:** Bugungi kuningiz yulduzlar xaritasida 'Yangi imkoniyatlar' uyida joylashgan. Qo'rqmasdan yangi narsalarni boshlang! 🚀",
    "💫 **Sehrli Portal:** Qalbingizdagi har bir ezgu tilak koinotga yuborildi. U yerda u yorug' nurga aylanib, tez orada hayotingizga qaytadi. 🌟"
]

aroma_guides = [
    "🌿 **Lavanda va Vanil hidi:** Bugun xonangizga lavanda yoki vanil atirini tarqating. Bu sizdagi barcha stressni bir zumda eritib, chuqur xotirjamlik olib keladi. 🕯️✨",
    "🍋 **Sitrus va Apelsin energiyasi:** Agar kayfiyatingiz biroz tushkun bo'lsa, apelsin yoki limonoviy hidlardan foydalaning. Ular tetiklik va quvonch baxsh etadi! ☀️🍊",
    "🍃 **Yalpiz va Evkalipt tozaligi:** Fikrlaringizni jamlash, diqqatni qaratish va toza nafas olish uchun yalpiz moyi yoki choyidan foydalaning. 🌬️💫"
]

def main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌟 🎨 Aura Testi", callback_data="aura"),
         InlineKeyboardButton(text="✨ 🔮 Koinot Sadosi", callback_data="fortune")],
        [InlineKeyboardButton(text="🖼️ ✨ Estetik Kosmik Rasmlar", callback_data="photo_list"),
         InlineKeyboardButton(text="💫 ☕ Shirinlik Menusi", callback_data="tea")],
        [InlineKeyboardButton(text="🧠 🌠 Kun Affirmatsiyasi", callback_data="affirmation"),
         InlineKeyboardButton(text="🔮 ✨ Sehrli Maslahat", callback_data="advice")],
        [InlineKeyboardButton(text="🌌 🌠 Yulduzlar Portali", callback_data="portal"),
         InlineKeyboardButton(text="🌿 🕯️ Aromaterapiya Gid", callback_data="aroma")],
        [InlineKeyboardButton(text="⭐ 🌠 Tilaklar Yulduzi", callback_data="wish_start")]
    ])
    return keyboard

def back_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Orqaga (Asosiy Menyu)", callback_data="back_to_menu")]
    ])

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(UserState.waiting_for_name)
    welcome_text = (
        "🌌✨ **Salom! AstroMood olamiga xush kelibsiz.** ✨🌌\n\n"
        "<i>Bu yer — qalbingizga orom, xayollaringizga qanot beruvchi kichik yulduzli maskan.</i> 🌠\n\n"
        "Tanishishimiz uchun ismingizni yozib yuboring:"
    )
    await message.answer(welcome_text, parse_mode="HTML")

@dp.message(UserState.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    user_name = message.text
    await state.update_data(name=user_name)
    await state.set_state(UserState.main_menu)
    
    await message.answer(
        f"Xush kelibsiz, **{user_name}**! 🌟 Siz bilan tanishganimdan judayam xursandman.\n\n"
        "Quyidagi sehrli menyudan o'zingizga yoqqan bo'limni tanlang:",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.main_menu)
    data = await state.get_data()
    name = data.get("name", "Do'stim")
    
    try:
        await callback.message.edit_text(
            f"🌟 **Asosiy Menyu**, {name}:\nQuyidagi bo'limlardan birini tanlang:",
            reply_markup=main_menu(),
            parse_mode="Markdown"
        )
    except Exception:
        await callback.message.delete()
        await callback.message.answer(
            f"🌟 **Asosiy Menyu**, {name}:\nQuyidagi bo'limlardan birini tanlang:",
            reply_markup=main_menu(),
            parse_mode="Markdown"
        )
    await callback.answer()

@dp.callback_query(F.data == "aura")
async def process_aura(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get("name", "Do'stim")
    aura_name, aura_desc = random.choice(list(auras.items()))
    
    text = (
        f"🌟 <b>{name}, sizning bugungi aurangiz:</b>\n"
        f"<b>{aura_name}</b>\n\n"
        f"<i>{aura_desc}</i>\n\n"
        f"✨✨✨✨✨✨✨✨✨"
    )
    await callback.message.edit_text(text, reply_markup=back_menu_kb(), parse_mode="HTML")

@dp.callback_query(F.data == "fortune")
async def process_fortune(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get("name", "Do'stim")
    text = random.choice(fortunes)
    
    response = (
        f"🌌 <b>{name} uchun Koinot Sadosi:</b>\n\n"
        f"<i>\"{text}\"</i>\n\n"
        f"💫💫💫💫💫💫💫💫💫"
    )
    await callback.message.edit_text(response, reply_markup=back_menu_kb(), parse_mode="HTML")

@dp.callback_query(F.data == "photo_list")
async def process_photo_list(callback: types.CallbackQuery, state: FSMContext):
    keyboard_buttons = []
    for i, p in enumerate(astro_photos):
        keyboard_buttons.append([InlineKeyboardButton(text=f"🖼️ {p['title']}", callback_data=f"show_photo_{i}")])
    
    keyboard_buttons.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_menu")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    
    try:
        await callback.message.edit_text(
            "🖼️ **Estetik Kosmik Rasmlar Galeriyasi:**\n"
            "Quyidagi ro'yxatdan o'zingizga yoqqan mavzuni tanlang — u tanlangan oynada ochiladi:",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    except Exception:
        await callback.message.delete()
        await callback.message.answer(
            "🖼️ **Estetik Kosmik Rasmlar Galeriyasi:**\n"
            "Quyidagi ro'yxatdan o'zingizga yoqqan mavzuni tanlang — u tanlangan oynada ochiladi:",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

@dp.callback_query(F.data.startswith("show_photo_"))
async def show_selected_photo(callback: types.CallbackQuery):
    photo_index = int(callback.data.split("_")[2])
    p = astro_photos[photo_index]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🖼️ Boshqa rasm tanlash", callback_data="photo_list")],
        [InlineKeyboardButton(text="⬅️ Orqaga (Asosiy Menyu)", callback_data="back_to_menu")]
    ])
    
    try:
        await callback.message.delete()
    except Exception:
        pass
        
    await callback.message.answer_photo(
        photo=p["photo"],
        caption=f"🌌 **{p['title']}**\n💡 _{p['desc']}_\n\n✨ _AstroMood Esthetic Vibe_",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "tea")
async def process_tea(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get("name", "Do'stim")
    rec = random.choice(teas)
    
    response = (
        f"☕ <b>{name} uchun Kayfiyat va Shirinlik Tavsiyasi:</b>\n\n"
        f"{rec}\n\n"
        f"🌟🌟🌟🌟🌟🌟🌟🌟🌟"
    )
    await callback.message.edit_text(response, reply_markup=back_menu_kb(), parse_mode="HTML")

@dp.callback_query(F.data == "affirmation")
async def process_affirmation(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get("name", "Do'stim")
    aff = random.choice(affirmations)
    
    response = (
        f"🧠 <b>{name} uchun Kunning Kuchli Affirmatsiyasi:</b>\n\n"
        f"{aff}\n\n"
        f"✨💫✨💫✨💫✨💫✨"
    )
    await callback.message.edit_text(response, reply_markup=back_menu_kb(), parse_mode="HTML")

@dp.callback_query(F.data == "advice")
async def process_advice(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get("name", "Do'stim")
    adv = random.choice(magic_advices)
    
    response = (
        f"🔮 <b>Sehrli Shar pichirlaydi, {name}:</b>\n\n"
        f"{adv}\n\n"
        f"✨🌠✨🌠✨🌠✨🌠✨"
    )
    await callback.message.edit_text(response, reply_markup=back_menu_kb(), parse_mode="HTML")

@dp.callback_query(F.data == "portal")
async def process_portal(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get("name", "Do'stim")
    portal_text = random.choice(star_portals)
    
    response = (
        f"🌌 <b>{name} uchun Yulduzlar Portali:</b>\n\n"
        f"{portal_text}\n\n"
        f"✨🌌✨🌌✨🌌✨🌌✨"
    )
    await callback.message.edit_text(response, reply_markup=back_menu_kb(), parse_mode="HTML")

@dp.callback_query(F.data == "aroma")
async def process_aroma(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get("name", "Do'stim")
    aroma_text = random.choice(aroma_guides)
    
    response = (
        f"🌿 <b>{name} uchun Aromaterapiya Gid:</b>\n\n"
        f"{aroma_text}\n\n"
        f"🕯️🌿🕯️🌿🕯️🌿🕯️🌿"
    )
    await callback.message.edit_text(response, reply_markup=back_menu_kb(), parse_mode="HTML")

# --- ⭐ TILAKLAR YULDUZI BO'LIMI ---
@dp.callback_query(F.data == "wish_start")
async def process_wish_start(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.waiting_for_wish)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Orqaga (Asosiy Menyu)", callback_data="back_to_menu")]
    ])
    
    await callback.message.edit_text(
        "⭐ **Tilaklar Yulduzi Kosmik Kapsulasiga xush kelibsiz!**\n\n"
        "O'z orzungiz yoki bugungi muhim maqsadingizni yozib yuboring, biz uni koinotga uchiramiz: ✨",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@dp.message(UserState.waiting_for_wish)
async def process_user_wish(message: types.Message, state: FSMContext):
    wish_text = message.text
    await state.set_state(UserState.main_menu)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌟 Asosiy Menyu", callback_data="back_to_menu")]
    ])
    
    await message.answer(
        f"🌠 **Tilagingiz qabul qilindi va yulduzlarga uchirildi!**\n\n"
        f"<i>\"{wish_text}\"</i>\n\n"
        f"✨ Koinot bu tilagingizni eshitdi va u tez orada amalga oshish yo'lini boshlaydi! 💫",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

async def main():
    logging.basicConfig(level=logging.INFO)
    print("Bot muvaffaqiyatli ishga tushdi va xabarlarni kutmoqda...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())