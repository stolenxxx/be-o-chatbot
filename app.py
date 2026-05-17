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

    print("Not page object")
    return "Not a page event", 404
