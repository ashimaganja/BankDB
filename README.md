
## Technologies Used

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+.
- **Python**: The programming language used for developing the application.
- **pandas**: A powerful data manipulation and analysis library used for handling the CSV files.
- **CSV**: Data storage format used to store transaction records.

## Installation

1. **Clone the repository:**

```bash
   git clone https://github.com/aiwhoo/FraudServer.git
   cd FraudServer
```

2. **Create and activate a virtual environment:**
```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install the required dependencies**

```bash
    pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
    Create a .env file in the root directory of the project and add the following line, replacing your_secret_key with a strong secret key:
    SECRET_KEY=your_secret_key
```

5. **Run the application:**
```bash 
    python main.py
```

6. **open your browser and navigate to:**
    
    http://127.0.0.1:8000


## Usage

1. **Viewing Transactions:**
    - Viewing the all the transactions is currently only availabe to the admin i.e. if you have the secret id
    - Each transaction record includes details such as transaction ID, credit card ID, vendor name, amount, date and zipcode.

2. **Reporting Fraudulent Transactions:**
    - Reporting Fradulent transaction is through a Report Fraud page


## Project Structure
FraudServer/
├──main.py
├──README.md
├──requirements.txt
├──utils.py
├───data
├───routers
│   ├──db_access.py
│   └───__pycache__
│          ├── db_access.cpython-311.pyc
│
├───static
│   └───css
│         ├── bank_profile.css
│         ├── customer_info.css
│         ├── fraud_input.css
│         ├── home_css.css
│         ├── network_of_banks.css
│         ├── spooky.css
│         ├── transaction_css.css
│
├───templates
│       ├──bank.html.j2
│       ├──credit_card.html.j2
│       ├──demographic.html.j2
│       ├──fraud.html.j2
│       ├──home.html.j2
│       ├──transaction.html.j2
│       ├──wrongPass.html.j2
|
└───__pycache__
        utils.cpython-311.pyc
    
- **main.py** : Entry point of the application. 
- **routers/db_access.py**: Database access and request and response validation.
- **utils.py** : Utility functions.
- **static/**: Directory for static files like CSS.
- **templates**: Directory for html templates

## Contributing
1. **Fork the repository**.

2. **Create a new branch:**

```bash
    git checkout -b feature-branch
    Make your changes. 
```

3. **Commit your changes:**

```bash
    git commit -m 'Add some feature'
```

3. **Push to the branch:**

```bash 
git push origin feature-branch
Open a pull request.

```
