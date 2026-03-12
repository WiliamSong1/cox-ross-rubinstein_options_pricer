from core import pricingRequest
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class BinomialPricerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Binomial Options Pricer")
        self.resize(460, 420)

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)

        input_group = QGroupBox("Inputs")
        form = QFormLayout()
        input_group.setLayout(form)

        self.stock_input = QLineEdit("100")
        self.strike_input = QLineEdit("100")
        self.maturity_input = QLineEdit("1")
        self.rate_input = QLineEdit("0.05")
        self.vol_input = QLineEdit("0.2")
        self.steps_input = QLineEdit("100")

        self.option_type = QComboBox()
        self.option_type.addItems(["Call", "Put"])

        form.addRow("Stock Price:", self.stock_input)
        form.addRow("Strike Price:", self.strike_input)
        form.addRow("Time to Maturity (years):", self.maturity_input)
        form.addRow("Market Rate:", self.rate_input)
        form.addRow("Market Volatility:", self.vol_input)
        form.addRow("Number of Steps:", self.steps_input)
        form.addRow("Option Type:", self.option_type)

        main_layout.addWidget(input_group)

        button_layout = QHBoxLayout()
        self.price_button = QPushButton("Price Option")
        self.clear_button = QPushButton("Clear")
        button_layout.addWidget(self.price_button)
        button_layout.addWidget(self.clear_button)
        main_layout.addLayout(button_layout)

        result_group = QGroupBox("Results")
        result_layout = QFormLayout()
        result_group.setLayout(result_layout)

        self.price_label = QLabel("-")
        self.delta_label = QLabel("-")
        self.status_label = QLabel("Ready")
        self.status_label.setWordWrap(True)

        result_layout.addRow("Option Price:", self.price_label)
        result_layout.addRow("Delta:", self.delta_label)
        result_layout.addRow("Status:", self.status_label)

        main_layout.addWidget(result_group)
        main_layout.addStretch()

        self.price_button.clicked.connect(self.calculate_price)
        self.clear_button.clicked.connect(self.clear_results)

    def calculate_price(self):
        try:
            stock_price = float(self.stock_input.text())
            strike_price = float(self.strike_input.text())
            time_to_maturity = float(self.maturity_input.text())
            market_rate = float(self.rate_input.text())
            market_vol = float(self.vol_input.text())
            num_steps = int(self.steps_input.text())
            is_call = self.option_type.currentText() == "Call"

            if num_steps <= 0:
                raise ValueError("Number of steps must be greater than 0.")
            if time_to_maturity <= 0:
                raise ValueError("Time to maturity must be greater than 0.")
            if stock_price <= 0 or strike_price <= 0:
                raise ValueError("Stock price and strike price must be greater than 0.")
            if market_vol < 0:
                raise ValueError("Market volatility cannot be negative.")

            result = pricingRequest(
                stock_price,
                strike_price,
                time_to_maturity,
                market_rate,
                market_vol,
                num_steps,
                is_call,
            )

            
            if isinstance(result, tuple) and len(result) >= 2:
                price, delta = result[0], result[1]
                self.price_label.setText(f"{price:.6f}")
                self.delta_label.setText(f"{delta:.6f}")
                self.status_label.setText("Success")
            elif isinstance(result, (int, float)):
                self.price_label.setText(f"{float(result):.6f}")
                self.delta_label.setText("Not returned by function")
                self.status_label.setText("Success")
            else:
                self.price_label.setText("-")
                self.delta_label.setText("-")
                self.status_label.setText(
                    "The pricing function ran, but it did not return a value. "
                    "Add `return price, delta` at the end of pricingRequest."
                )

        except Exception as exc:
            QMessageBox.critical(self, "Input Error", str(exc))
            self.status_label.setText("Error")

    def clear_results(self):
        self.price_label.setText("-")
        self.delta_label.setText("-")
        self.status_label.setText("Ready")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BinomialPricerWindow()
    window.show()
    sys.exit(app.exec())
