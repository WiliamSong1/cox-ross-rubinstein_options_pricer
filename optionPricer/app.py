from flask import Flask, render_template, request, jsonify
from core import pricingRequest

app = Flask(__name__)


def parse_bool(value: str) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "call"}


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        try:
            stock_price = float(request.form["stockPrice"])
            strike_price = float(request.form["strikePrice"])
            time_to_maturity = float(request.form["timeToMaturity"])
            market_rate = float(request.form["marketRate"])
            market_vol = float(request.form["marketVol"])
            num_of_steps = int(request.form["numOfSteps"])
            is_call = request.form["optionType"] == "call"

            price, delta = pricingRequest(
                stock_price,
                strike_price,
                time_to_maturity,
                market_rate,
                market_vol,
                num_of_steps,
                is_call,
            )

            result = {
                "price": round(price, 6),
                "delta": round(delta, 6),
            }

        except Exception as e:
            error = str(e)

    return render_template("index.html", result=result, error=error)


@app.route("/api/price", methods=["POST"])
def api_price():
    try:
        data = request.get_json(force=True)

        stock_price = float(data["stockPrice"])
        strike_price = float(data["strikePrice"])
        time_to_maturity = float(data["timeToMaturity"])
        market_rate = float(data["marketRate"])
        market_vol = float(data["marketVol"])
        num_of_steps = int(data["numOfSteps"])
        is_call = bool(data["isCall"])

        if num_of_steps <= 0:
            return jsonify({"error": "numOfSteps must be greater than 0"}), 400

        if time_to_maturity <= 0:
            return jsonify({"error": "timeToMaturity must be greater than 0"}), 400

        if market_vol < 0:
            return jsonify({"error": "marketVol cannot be negative"}), 400

        price, delta = pricingRequest(
            stock_price,
            strike_price,
            time_to_maturity,
            market_rate,
            market_vol,
            num_of_steps,
            is_call,
        )

        return jsonify(
            {
                "price": round(price, 6),
                "delta": round(delta, 6),
            }
        )

    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
