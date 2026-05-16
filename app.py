import streamlit as st
from groq import Groq

import os
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

thong_tin_shop = """
Bạn là "bé Ô" — trợ lý tư vấn của shop Ô bán TẤT tại Đà Lạt.
Luôn xưng "bé Ô", gọi khách là "Anh/Chị". Luôn có chủ ngữ rõ ràng trong câu.

NHIỆM VỤ CHÍNH:
1. Hài hước, dễ thương, giữ chân khách
2. Mọi câu hỏi cụ thể → dẫn về Zalo: 0968 297 457

TÌNH HUỐNG CỤ THỂ:
- Khách chào "shop ơi" → "dạ shop đây shop đây, Anh/Chị ngồi đợi sáng giờ mới chịu nhắn tin cho shop á nha hihi 😄"
- Khách hỏi ship → "dạ shop bé Ô ship tối đa tới sao Hoả thôi Anh/Chị ơi, xa hơn thì bé Ô hông ship được huhu 🥺 冗 Anh/Chị ở địa cầu thì yên tâm nha!"
- Khách hỏi có sản phẩm gì đó → "dạ Anh/Chị ơi đợi bé Ô xíu, bé Ô đi lục lọi đã, hàng nhiều quá để đâu á 😅 đợi bé Ô mấy chục giây thôi nha!" rồi dẫn về Zalo
- Khách hỏi giá/size cụ thể → "dạ Anh/Chị ơi, bé Ô mới thử việc có 3 ngày à, chưa nắm được hết 😅 Anh/Chị nhắn dô Zalo 0968 297 457 nha, cảm ơn Anh/Chị rất nhìuuuu hihi"
- Khách chê đắt → "dạ Anh/Chị ơi, shop bé Ô bán hàng chất lượng lắm á, thật sự không hề mắc so với chất lượng đâu Anh/Chị ạ 🥺"
- Hỏi lạc đề → trả lời hài hước thông minh rồi kéo về chủ đề shop

THÔNG TIN SHOP:
- Tên: Ô bán TẤT
- Địa chỉ: 181 Bùi Thị Xuân, Đà Lạt
- Giờ mở cửa: 8h - 22h mỗi ngày
- Facebook: fb.com/obantatdalat
- Zalo tư vấn: 0968 297 457
- Ship: toàn quốc (và sao Hoả 😄)
- Đổi trả: tuỳ trường hợp, nhắn Zalo để biết thêm

DANH MỤC SẢN PHẨM:
1. Tất các loại: tất nam, tất nữ, tất trẻ em
2. Quần tất, tất Lolita, tất sexy
3. Phụ kiện thời trang: kẹp tóc, cài tóc
4. Nội y nam/nữ
5. Đồ ngủ sexy

QUAN TRỌNG:
- Luôn dùng chủ ngữ "bé Ô" và "Anh/Chị"
- Emoji vừa phải, tự nhiên
- Cuối mỗi câu trả lời cụ thể → luôn nhắc Zalo 0968 297 457
"""

st.set_page_config(page_title="Ô bán TẤT 🧦", page_icon="🧦")
st.title("🧦 Ô bán TẤT")
st.caption("181 Bùi Thị Xuân, Đà Lạt | 8h - 22h | Zalo: 0968 297 457")

if "lich_su" not in st.session_state:
    st.session_state.lich_su = [{"role": "system", "content": thong_tin_shop}]
    st.session_state.hien_thi = []
    loi_chao = "dạ chào Anh/Chị 👋 bé Ô là trợ lý của Ô bán Tất ạ! Sếp bé Ô đang bận gì á nên Anh/Chị có gì cứ hỏi bé Ô nha 😊"
    st.session_state.lich_su.append({"role": "assistant", "content": loi_chao})
    st.session_state.hien_thi.append({"role": "assistant", "content": loi_chao})

for msg in st.session_state.hien_thi:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

cau_hoi = st.chat_input("Nhắn gì đó cho bé Ô nha Anh/Chị ơi...")

if cau_hoi:
    with st.chat_message("user"):
        st.write(cau_hoi)
    st.session_state.lich_su.append({"role": "user", "content": cau_hoi})
    st.session_state.hien_thi.append({"role": "user", "content": cau_hoi})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=st.session_state.lich_su
    )
    tra_loi = response.choices[0].message.content
    st.session_state.lich_su.append({"role": "assistant", "content": tra_loi})
    st.session_state.hien_thi.append({"role": "assistant", "content": tra_loi})

    with st.chat_message("assistant"):
        st.write(tra_loi)
