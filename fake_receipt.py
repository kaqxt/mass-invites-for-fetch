import random
import string
from datetime import datetime, timedelta
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

STORES = [
    ("WALMART", "Supercenter #{}", "Always Low Prices"),
    ("TARGET", "T-{}", "Expect More. Pay Less."),
    ("KROGER", "Store #{}", "Fresh for Everyone"),
    ("CVS Pharmacy", "#{}", "Health is everything"),
    ("Walgreens", "#{}", "Trusted since 1901"),
    ("Dollar General", "#{}", "Save time. Save money."),
    ("7-ELEVEN", "#{}", "Oh Thank Heaven"),
    ("Shell", "Station #{}", "Go well"),
]

ITEMS = [
    ("BANANAS", 0.59, "lb"),
    ("MILK 1GAL", 3.49, "ea"),
    ("BREAD WHT", 2.29, "ea"),
    ("EGGS LG 12", 2.99, "ea"),
    ("CHIPS LAYS", 4.29, "ea"),
    ("SODA 12PK", 6.99, "ea"),
    ("WATER 24PK", 5.49, "ea"),
    ("CEREAL", 3.99, "ea"),
    ("YOGURT 4PK", 3.49, "ea"),
    ("CHEESE 8OZ", 2.79, "ea"),
]

def generate_receipt(out_path: str):
    store, fmt, tag = random.choice(STORES)
    store_id = fmt.format(random.randint(1000, 9999))
    dt = datetime.now() - timedelta(days=random.randint(0, 6), hours=random.randint(8, 20))
    date_str = dt.strftime("%m/%d/%Y")
    time_str = dt.strftime("%I:%M %p")

    items = random.sample(ITEMS, k=random.randint(3, 6))
    subtotal = 0.0
    lines = []
    for name, price, unit in items:
        qty = 1 if unit == "ea" else round(random.uniform(0.8, 2.2), 2)
        total = round(price * qty, 2)
        subtotal += total
        lines.append((name, qty, unit, price, total))

    tax = round(subtotal * 0.0825, 2)
    grand = round(subtotal + tax, 2)

    width, height = 380, 90 + len(lines) * 28 + 130
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 14)
        font_b = ImageFont.truetype("arialbd.ttf", 16)
        font_s = ImageFont.truetype("arial.ttf", 12)
    except:
        font = ImageFont.load_default()
        font_b = font
        font_s = font

    y = 12
    draw.text((width//2, y), store, fill="black", font=font_b, anchor="mt")
    y += 22
    draw.text((width//2, y), store_id, fill="black", font=font_s, anchor="mt")
    y += 18
    draw.text((width//2, y), tag, fill="gray", font=font_s, anchor="mt")
    y += 25
    draw.line([(20, y), (width-20, y)], fill="black")
    y += 12
    draw.text((20, y), f"{date_str}  {time_str}", fill="black", font=font_s)
    y += 20
    draw.line([(20, y), (width-20, y)], fill="black")
    y += 12

    for name, qty, unit, price, total in lines:
        draw.text((20, y), name, fill="black", font=font)
        draw.text((width-20, y), f"${total:.2f}", fill="black", font=font, anchor="rt")
        y += 18
        if unit != "ea":
            draw.text((30, y), f"{qty} {unit} @ ${price:.2f}", fill="gray", font=font_s)
            y += 16

    y += 8
    draw.line([(20, y), (width-20, y)], fill="black")
    y += 12
    draw.text((20, y), "SUBTOTAL", fill="black", font=font)
    draw.text((width-20, y), f"${subtotal:.2f}", fill="black", font=font, anchor="rt")
    y += 18
    draw.text((20, y), "TAX", fill="black", font=font)
    draw.text((width-20, y), f"${tax:.2f}", fill="black", font=font, anchor="rt")
    y += 20
    draw.text((20, y), "TOTAL", fill="black", font=font_b)
    draw.text((width-20, y), f"${grand:.2f}", fill="black", font=font_b, anchor="rt")
    y += 28
    draw.text((width//2, y), "THANK YOU", fill="black", font=font_s, anchor="mt")
    y += 16
    trans = "".join(random.choices(string.digits, k=12))
    draw.text((width//2, y), f"TRANS #{trans}", fill="gray", font=font_s, anchor="mt")

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, "PNG")