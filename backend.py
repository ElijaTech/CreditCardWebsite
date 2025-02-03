from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

def is_valid_credit_card(card_number):
    card_number = ''.join(filter(str.isdigit, card_number))

    if len(card_number) != 16:
        return False

    total = 0
    reverse_digits = card_number[::-1]

    for i, digit in enumerate(reverse_digits):
        num = int(digit)
        if i % 2 == 1:
            num *= 2
            if num > 9:
                num -= 9

        total += num
    return total % 10 == 0

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check_card", methods=["POST"])
def check_card():
    card_number = request.form.get("cardNumber")

    if card_number and is_valid_credit_card(card_number):
        return redirect(url_for('valid'))
    else:
        return redirect(url_for('invalid'))

@app.route("/valid")
def valid():
    return render_template("valid.html")

@app.route("/invalid")
def invalid():
    return render_template("invalid.html")

if __name__ == "__main__":
    app.run(debug=True)
