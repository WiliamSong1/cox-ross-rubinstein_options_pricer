# Binomial Option Pricer

A Python application that prices European call and put options using a **binomial tree model**.
The project includes both a **Flask web interface** and a **PySide6 desktop GUI** that interact with the same pricing engine.

This application computes:

* **Option price**
* **Delta (hedge ratio)**

using a discrete-time binomial lattice.

---

# Features

* Binomial option pricing implementation in Python
* Calculates **option value and delta**
* **Flask web interface** for browser-based usage
* **PySide6 desktop GUI** for local application use
* JSON API endpoint for programmatic access
* Modular architecture separating pricing logic from UI

---

# Project Structure

```
option_pricer/
│
├── app.py              # Flask web application
├── gui.py              # PySide6 desktop GUI
├── pricing.py          # Binomial pricing algorithm
├── requirements.txt    # Python dependencies
│
└── templates/
    └── index.html      # Web interface template
```

---

# Pricing Model

The application uses a **binomial option pricing model**, which approximates option prices by modeling possible future asset prices over discrete time steps.

Key parameters:

| Parameter         | Description                    |
| ----------------- | ------------------------------ |
| Stock Price       | Current underlying asset price |
| Strike Price      | Option strike                  |
| Time to Maturity  | Time until expiration          |
| Market Rate       | Risk-free interest rate        |
| Market Volatility | Annualized volatility          |
| Number of Steps   | Depth of binomial tree         |
| Option Type       | Call or Put                    |

The model calculates:

* **Risk-neutral probability**
* **Backward induction of option value**
* **Delta hedge ratio**

---

# Installation

Clone the repository:

```bash
git clone https://github.com/WiliamSong1/cox-ross-rubinstein_options_pricer.git
cd cox-ross-rubinstein_options_pricer
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Dependencies include:

* Flask
* NumPy
* PySide6
* requests

---

# Running the Application

## Start the Flask Server

```bash
python app.py
```

Open the web interface:

```
http://127.0.0.1:5000
```

---

## Launch the Desktop GUI

In another terminal:

```bash
python gui.py
```

The GUI sends requests to the Flask API running locally.

---



