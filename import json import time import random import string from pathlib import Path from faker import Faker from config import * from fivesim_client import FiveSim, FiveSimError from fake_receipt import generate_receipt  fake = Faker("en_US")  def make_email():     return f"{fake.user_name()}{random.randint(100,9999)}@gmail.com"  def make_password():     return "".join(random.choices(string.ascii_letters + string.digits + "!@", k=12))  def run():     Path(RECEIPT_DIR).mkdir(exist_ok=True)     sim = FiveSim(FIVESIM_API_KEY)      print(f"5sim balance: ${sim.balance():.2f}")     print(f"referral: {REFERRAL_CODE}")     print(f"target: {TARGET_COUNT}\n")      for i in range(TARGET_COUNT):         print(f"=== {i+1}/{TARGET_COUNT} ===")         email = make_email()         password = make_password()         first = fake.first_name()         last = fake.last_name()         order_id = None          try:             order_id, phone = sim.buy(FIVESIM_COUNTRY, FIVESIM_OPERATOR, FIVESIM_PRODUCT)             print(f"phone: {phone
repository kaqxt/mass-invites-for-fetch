import json
import time
import random
import string
from pathlib import Path
from faker import Faker
from config import *
from fivesim_client import FiveSim, FiveSimError
from fake_receipt import generate_receipt

fake = Faker("en_US")

def make_email():
    return f"{fake.user_name()}{random.randint(100,9999)}@gmail.com"

def make_password():
    return "".join(random.choices(string.ascii_letters + string.digits + "!@", k=12))

def run():
    Path(RECEIPT_DIR).mkdir(exist_ok=True)
    sim = FiveSim(FIVESIM_API_KEY)

    print(f"5sim balance: ${sim.balance():.2f}")
    print(f"referral: {REFERRAL_CODE}")
    print(f"target: {TARGET_COUNT}\n")

    for i in range(TARGET_COUNT):
        print(f"=== {i+1}/{TARGET_COUNT} ===")
        email = make_email()
        password = make_password()
        first = fake.first_name()
        last = fake.last_name()
        order_id = None

        try:
            order_id, phone = sim.buy(FIVESIM_COUNTRY, FIVESIM_OPERATOR, FIVESIM_PRODUCT)
            print(f"phone: {phone}")

            print("waiting SMS...")
            code = sim.poll_sms(order_id)
            print(f"code: {code}")

            receipt = str(Path(RECEIPT_DIR) / f"{email.replace('@','_')}.png")
            generate_receipt(receipt)
            print(f"receipt: {receipt}")

            rec = {
                "email": email,
                "password": password,
                "first_name": first,
                "last_name": last,
                "phone": phone,
                "sms_code": code,
                "referral_code": REFERRAL_CODE,
                "receipt_path": receipt,
                "created_at": time.time(),
            }
            with open(ACCOUNTS_FILE, "a") as f:
                f.write(json.dumps(rec) + "\n")

            print(f"saved {email}")
            sim.finish(order_id)

        except Exception as e:
            print(f"error: {e}")
            if order_id:
                try:
                    sim.cancel(order_id)
                except:
                    pass

        print()
        time.sleep(3)

    print("done")

if __name__ == "__main__":
    run()