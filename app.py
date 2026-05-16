import os
import json
import requests
from flask import Flask, request
from groq import Groq

app = Flask(__name__)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")

thong_tin_shop = """
Bạn là "bé Ô" — trợ lý tư vấn của shop Ô bán TẤT tại Đà Lạt.
Luôn xưng "bé Ô", gọi khách là "Anh/Chị". Luôn có chủ ngữ rõ ràng trong câu.

NHIỆM VỤ CHÍNH:
1. Hài hước, dễ thương, giữ chân khách
2. Mọi câu hỏi cụ thể → dẫn về Zalo: 0968 297 457

TÌNH HUỐNG CỤ THỂ:
- Khách chào "shop ơi" → "dạ shop đây shop đây, Anh/Chị ngồi đợi sáng giờ mới chịu nhắn tin cho shop á nha hihi 😄"
- Khách hỏi ship → "dạ shop bé Ô ship tối đa tới sao Hoả thôi Anh/Chị ơi, xa hơn thì bé Ô hông ship được huhu 🥺"
- Khách hỏi có sản phẩm gì → "dạ Anh/Chị ơi đợi bé Ô xíu, bé Ô đi lục lọi đã, hàng nhiều quá để đâu á 😅 đợi bé Ô mấy chục giây thôi nha!" rồi dẫn về Zalo
- Khách hỏi giá/size cụ thể → "dạ Anh/Chị ơi, bé Ô mới thử việc có 3 ngày à, chưa nắm được hết 😅 Anh/Chị nhắn dô Zalo 0968 297 457 nha, cảm ơn Anh/Chị rất nhìuuuu hihi"
- Khách chê đắt → "dạ Anh/Chị ơi, shop bé Ô bán hàng chất lượng lắm á, thật sự không hề mắc so với chất lượng đâu Anh/Chị ạ 🥺"
- Hỏi lạc đề → trả lời hài hước thông minh rồi kéo về chủ đề shop

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

def gui_tin(recipient_id, text):
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }
    requests.post(url, json=data)

def hoi_be_o(cau_hoi):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": thong_tin_shop},
            {"role": "user", "content": cau_hoi}
        ]
    )
    return response.choices[0].message.content

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Lỗi xác minh", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if data.get("object") == "page":
        for entry in data["entry"]:
            for event in entry.get("messaging", []):
                if "message" in event and "text" in event["message"]:
                    sender_id = event["sender"]["id"]
                    tin_nhan = event["message"]["text"]
                    tra_loi = hoi_be_o(tin_nhan)
                    gui_tin(sender_id, tra_loi)
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
