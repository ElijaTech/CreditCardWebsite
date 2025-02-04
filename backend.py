from flask import Flask, request, render_template

app = Flask(__name__)

def luhn_check(card_number):
    card_number = card_number.replace(" ", "")
    if not card_number.isdigit():
        return False

    digits = [int(d) for d in card_number]
    checksum = 0
    double = False

    for i in range(len(digits) - 1, -1, -1):
        num = digits[i]
        if double:
            num *= 2
            if num > 9:
                num -= 9
        checksum += num
        double = not double

    return checksum % 10 == 0

def get_card_type(card_number):
    card_number = card_number.replace(" ", "")

    if card_number.startswith("4"):
        return "Visa"
    elif card_number.startswith(("51", "52", "53", "54", "55")):
        return "MasterCard"
    elif card_number.startswith(("34", "37")):
        return "American Express"
    elif card_number.startswith("6011") or card_number[:3] in ["644", "645", "646", "647", "648", "649"] or card_number.startswith("65"):
        return "Discover"
    else:
        return "Unknown"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check_card", methods=["POST"])
def check_card():
    card_number = request.form.get("cardNumber")

    if luhn_check(card_number):
        card_type = get_card_type(card_number)
        return render_template("valid.html", card_type=card_type)
    else:
        return render_template("invalid.html")

if __name__ == "__main__":
    app.run(debug=True)
