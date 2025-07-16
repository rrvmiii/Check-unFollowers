"""
Instagram Follow Analyzer - v1.0
BY @rrvmiii
GitHub: https://github.com/rrvmiii
Instagram: https://instagram.com/rrvmiii
"""

import json
import os

# أسماء الملفات (يُفترض وجودها في نفس مجلد السكربت)
FOLLOWING_FILE = "following.json"
FOLLOWERS_FILE = "followers.json"
REQUESTS_FILE = "requests.json"

# تحميل بيانات من ملف JSON بطريقة آمنة
def load_json_file(filename, key):
    if not os.path.exists(filename):
        print(f"❌ الملف غير موجود: {filename}")
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get(key, [])
    except json.JSONDecodeError:
        print(f"❌ خطأ في تنسيق JSON في الملف: {filename}")
        return []
    except Exception as e:
        print(f"❌ حدث خطأ أثناء قراءة الملف {filename}:\n{e}")
        return []

# تحميل بيانات following
following_data = load_json_file(FOLLOWING_FILE, "relationships_following")
following_list = [
    acc["value"]
    for item in following_data
    for acc in item.get("string_list_data", [])
]

# تحميل بيانات followers
followers_data = load_json_file(FOLLOWERS_FILE, "relationships_followers")
followers_list = [
    acc["value"]
    for item in followers_data
    for acc in item.get("string_list_data", [])
]

# تحميل بيانات requests
requests_data = load_json_file(REQUESTS_FILE, "relationships_follow_requests_sent")
requests_list = [
    acc["value"]
    for item in requests_data
    for acc in item.get("string_list_data", [])
]

# مقارنة: من تتابعهم ولا يتابعونك
followers_set = set(followers_list)
not_following_back = [user for user in following_list if user not in followers_set]

# طباعة النتائج
print("✅ الحسابات اللي مش متابعينك باك:")
for user in not_following_back:
    print("-", user)

print("\n✅ الحسابات اللي الريكوست عندهم معلق:")
for user in requests_list:
    print("-", user)

# حفظ النتائج في ملفات نصية
try:
    with open("not_following_back.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(not_following_back))
    with open("pending_requests.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(requests_list))
    print("\n✨ الملفات اتعملت: not_following_back.txt و pending_requests.txt")
except Exception as e:
    print(f"❌ فشل حفظ النتائج في الملفات:\n{e}")
