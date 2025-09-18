from .metadata import parse_working_hours, generate_note_tags

def format_menu_chunk(item: dict, item_id: int) -> dict:
    price_lines = [f"- {size}: {item['sizes'][size]} جنيه" for size in item['sizes']]
    prices_str = "\n".join(price_lines)
    page_content = (
        f"[Menu Item]\n"
        f"اسم الصنف: {item['item_name_ar']} ({item['item_name']})\n"
        f"الفئة: {item['category']}\n"
        f"الأسعار:\n{prices_str}"
    )

    prices_metadata = ', '.join([f"{size}:{item['sizes'][size]}" for size in item['sizes']])
    metadata = {
        "source": "menu",
        "item_id": f"menu_{item_id:03d}",
        "category": item['category'],
        "item_name": item['item_name'],
        "item_name_ar": item['item_name_ar'],
        "prices": prices_metadata,
        "currency": "EGP",
        "lang": "ar"
    }
    return {"page_content": page_content, "metadata": metadata}


def format_branch_chunk(branch: dict, branch_id: int) -> dict:
    phone = branch.get('phone_number')
    if isinstance(phone, list):
        phone_str = ', '.join(phone)
    elif isinstance(phone, str):
        phone_str = phone
    else:
        phone_str = ""

    wh = parse_working_hours(branch['working_hours'])
    working_hours_str = f"{wh['days']} {wh['from']}-{wh['to']}" if wh['from'] else branch['working_hours']

    page_content = (
        f"[Branch]\n"
        f"اسم الفرع: cilantro فرع {branch['branch_name']}\n"
        f"العنوان: {branch['address']}\n"
        f"رقم التليفون: {phone_str if phone_str else 'غير متوفر'}\n"
        f"مواعيد العمل: {working_hours_str}"
    )

    metadata = {
        "source": "branches",
        "branch_id": f"branch_{branch_id:03d}",
        "branch_name": branch['branch_name'],
        "area": branch['branch_name'].split(' - ')[0],
        "address": branch['address'],
        "phone_number": phone_str,
        "working_hours": working_hours_str
    }
    return {"page_content": page_content, "metadata": metadata}


def format_note_chunk(note: dict, note_id: int) -> dict:
    tags_list = generate_note_tags(note['topic'])
    tags_str = ', '.join(tags_list)  

    page_content = (
        f"[Note]\n"
        f"الموضوع: {note['topic']}\n"
        f"المحتوى: {note['note_ar']}"
    )
    metadata = {
        "source": "notes",
        "note_id": f"note_{note_id:03d}",
        "topic": note['topic'],
        "lang": "ar",
        "tags": tags_str
    }
    return {"page_content": page_content, "metadata": metadata}
