from django import template

register = template.Library()

# Mirrors EXPENSE_CATEGORIES / INCOME_CATEGORIES in the Penny Discord bot
# (github.com/tao-thewarat/penny, src/domain/entry-category.ts).
# Keys and emoji must match the bot; labels are Thai for the portal.
# category -> (Thai label, emoji, colour tone used by .tone-* classes, entry type)
CATEGORY_META = {
    # Expense
    "food_and_drink": ("อาหารและเครื่องดื่ม", "🍜", "orange", "expense"),
    "groceries": ("ของชำและของใช้ในบ้าน", "🛒", "green", "expense"),
    "transport": ("การเดินทาง", "🚗", "blue", "expense"),
    "shopping": ("ช้อปปิ้ง", "🛍️", "pink", "expense"),
    "bills_and_utilities": ("บิลและค่าสาธารณูปโภค", "💡", "amber", "expense"),
    "housing": ("ที่อยู่อาศัย", "🏠", "teal", "expense"),
    "health": ("สุขภาพ", "💊", "red", "expense"),
    "entertainment": ("ความบันเทิง", "🎮", "violet", "expense"),
    "education": ("การศึกษา", "📚", "cyan", "expense"),
    "travel": ("ท่องเที่ยว", "✈️", "sky", "expense"),
    "personal_care": ("ดูแลตัวเอง", "💇", "fuchsia", "expense"),
    "gifts_and_donations": ("ของขวัญและบริจาค", "🎁", "rose", "expense"),
    "fees_and_charges": ("ค่าธรรมเนียมและภาษี", "🏦", "slate", "expense"),
    "pets": ("สัตว์เลี้ยง", "🐶", "yellow", "expense"),
    "other": ("อื่นๆ", "📦", "slate", "expense"),
    # Income
    "salary": ("เงินเดือน", "💵", "emerald", "income"),
    "bonus": ("โบนัสและค่าคอมมิชชัน", "🎉", "lime", "income"),
    "freelance": ("งานอิสระ", "💼", "indigo", "income"),
    "business": ("ธุรกิจ", "🏪", "blue", "income"),
    "investment": ("การลงทุน", "📈", "green", "income"),
    "gift_received": ("เงินที่ได้รับ", "🧧", "rose", "income"),
    "refund": ("เงินคืน", "↩️", "sky", "income"),
    "other_income": ("รายรับอื่นๆ", "💰", "amber", "income"),
}

# Same fallback the bot uses for an unknown id ("other")
FALLBACK_ICON = "📦"
FALLBACK_TONE = "slate"


def _meta(category):
    return CATEGORY_META.get(category or "")


@register.simple_tag
def category_choices():
    """Known categories as dicts, for datalists and client-side previews."""
    return [
        {"value": key, "label": label, "icon": icon, "tone": tone, "type": entry_type}
        for key, (label, icon, tone, entry_type) in CATEGORY_META.items()
    ]


@register.filter
def category_label(category):
    meta = _meta(category)
    if meta:
        return meta[0]
    return (category or "อื่นๆ").replace("_", " ").capitalize()


@register.filter
def category_icon(category):
    meta = _meta(category)
    return meta[1] if meta else FALLBACK_ICON


@register.filter
def category_tone(category):
    meta = _meta(category)
    return meta[2] if meta else FALLBACK_TONE
