import re


def parse_working_hours(hours_str: str) -> dict:
    days = hours_str.split(' ')[0]
    time_parts = re.findall(r'(\d{1,2}:\d{2})\s*(ص|م)', hours_str)

    def to_24hr(time, period):
        hour, minute = map(int, time.split(':'))
        if period == 'ص' and hour == 12: hour = 0
        if period == 'م' and hour != 12: hour += 12
        return f"{hour:02d}:{minute:02d}"

    if len(time_parts) == 2:
        start_time, start_period = time_parts[0]
        end_time, end_period = time_parts[1]
        return {
            "days": days,
            "from": to_24hr(start_time, start_period),
            "to": to_24hr(end_time, end_period)
        }
    return {"days": "", "from": "", "to": ""}


def generate_note_tags(topic: str) -> list:
    topic_to_tags_map = {
        "coffee_addons": ["إضافات", "قهوة", "سعر", "بلاتينم بلند"],
        "coffee_options": ["خيارات", "قهوة", "بدون كافيين", "ديكاف"],
        "milk_addons": ["إضافات", "حليب نباتي", "سعر", "لوز", "شوفان", "جوز الهند"],
        "pricing_info": ["أسعار", "ضريبة", "معلومات"],
        "salad_addons": ["إضافات", "سلطة", "سعر", "صوص"]
    }
    return topic_to_tags_map.get(topic, [topic])
