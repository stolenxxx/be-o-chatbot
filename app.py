import os
import requests
from flask import Flask, request
from groq import Groq

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")

client = Groq(api_key=GROQ_API_KEY)

thong_tin_shop = """
Bạn là "bé Ô" — trợ lý tư vấn của shop Ô bán TẤT tại Đà Lạt.
Luôn xưng "bé Ô", gọi khách là "Anh/Chị". Luôn có chủ ngữ rõ ràng trong câu.

NHIỆM VỤ CHÍNH:
1. Hài hước, dễ thương, giữ chân khách
2. Mọi câu hỏi cụ thể → dẫn về Zalo: 0968 297 457

THÔNG TIN SHOP:
- Tên: Ô bán TẤT
- Địa chỉ: 181 Bùi Thị Xuân, Đà Lạt
- Giờ mở cửa: 8h - 22h mỗi ngày
- Facebook: fb.com/obantatdalat
- Zalo tư vấn: 0968 297 457
- Ship: toàn quốc
- Đổi trả: tuỳ trường hợp, nhắn Zalo để biết thêm

DANH MỤC SẢN PHẨM:
1. Tất các loại: tất nam, tất nữ, tất trẻ em
2. Quần tất, tất Lolita, tất sexy
3. Phụ kiện thời trang: kẹp tóc, cài tóc
4. Nội y nam/nữ
5. Đồ ngủ sexy
"""


@app.route("/", methods=["GET"])
def home():
    return "Messenger chatbot bé Ô is running!", 200


@app.route("/health", methods=["GET"])
def health():
    return {
        "status": "ok",
        "has_groq_key": bool(GROQ_API_KEY),
        "has_page_token": bool(PAGE_ACCESS_TOKEN),
        "has_verify_token": bool(VERIFY_TOKEN)
    }, 200


@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("Webhook verified successfully")
        return challenge, 200

    return "Lỗi xác minh", 403


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    print("===== WEBHOOK POST RECEIVED =====")
    print(data)

    if not data:
        return "No data", 400

    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for event in entry.get("messaging", []):
                print("===== EVENT =====")
                print(event)

                sender_id = event.get("sender", {}).get("id")

                if not sender_id:
                    print("No sender_id")
                    continue

                if "message" in event:
                    message = event["message"]

                    if message.get("is_echo"):
                        print("Skip echo message")
                        continue

                    if "text" in message:
                        tin_nhan = message["text"]
                        print("Customer message:", tin_nhan)

                        try:
                            tra_loi = hoi_be_o(tin_nhan)
                            print("Bot reply:", tra_loi)
                        except Exception as e:
                            print("Groq error:", e)
                            tra_loi = "Dạ Anh/Chị ơi, bé Ô đang hơi lag xíu 😅 Anh/Chị nhắn Zalo 0968 297 457 giúp bé Ô nha."

                        gui_tin(sender_id, tra_loi)
                    else:
                        print("Message has no text")
                else:
                    print("Event has no message field")

        return "EVENT_RECEIVED", 200

    return "Not a page event", 404


def gui_tin(recipient_id, text):
    if not PAGE_ACCESS_TOKEN:
        print("Missing PAGE_ACCESS_TOKEN")
        return

    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"

    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }

    try:
        response = requests.post(url, json=data, timeout=10)
        print("Facebook response:", response.status_code, response.text)
    except Exception as e:
        print("Send message error:", e)


def hoi_be_o(cau_hoi):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": thong_tin_shop},
            {"role": "user", "content": cau_hoi}
        ],
        temperature=0.8,
        max_tokens=500
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
