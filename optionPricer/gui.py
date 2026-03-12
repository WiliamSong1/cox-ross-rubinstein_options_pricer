import sys
import requests

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QFormLayout,
    QVBoxLayout,
    QMessageBox,
)


API_URL = "http://127.0.0.1:5000/api/price"


class OptionPricerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Option Pricer GUI")
        self.resize(420, 350)

        self.stock_price = QLineEdit()
        self.strike_price = QLineEdit()
        self.time_to_maturity = QLineEdit()
        self.market_rate = QLineEdit()
        self.market_vol = QLineEdit()
        self.num_steps = QLineEdit()

        self.option_type = QComboBox()
        self.option_type.addItems(["Call", "Put"])

        self.price_label = QLabel("Price: ")
        self.delta_label = QLabel("Delta: ")

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate_price)

        form = QFormLayout()
        form.addRow("Stock Price:", self.stock_price)
        form.addRow("Strike Price:", self.strike_price)
        form.addRow("Time to Maturity:", self.time_to_maturity)
        form.addRow("Market Rate:", self.market_rate)
        form.addRow("Market Volatility:", self.market_vol)
        form.addRow("Number of Steps:", self.num_steps)
        form.addRow("Option Type:", self.option_type)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.calculate_button)
        layout.addWidget(self.price_label)
        layout.addWidget(self.delta_label)

        self.setLayout(layout)

    def calculate_price(self):
        try:
            payload = {
                "stockPrice": float(self.stock_price.text()),
                "strikePrice": float(self.strike_price.text()),
                "timeToMaturity": float(self.time_to_maturity.text()),
                "marketRate": float(self.market_rate.text()),
                "marketVol": float(self.market_vol.text()),
                "numOfSteps": int(self.num_steps.text()),
                "isCall": self.option_type.currentText() == "Call",
            }

            response = requests.post(API_URL, json=payload, timeout=10)

            if response.status_code != 200:
                try:
                    error_msg = response.json().get("error", "Unknown error")
                except Exception:
                    error_msg = response.text
                raise ValueError(error_msg)

            data = response.json()
            self.price_label.setText(f"Price: {data['price']}")
            self.delta_label.setText(f"Delta: {data['delta']}")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OptionPricerGUI()
    window.show()
    sys.exit(app.exec())
