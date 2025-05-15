# QuickBooks Analytics Dashboard

A modern, responsive dashboard for visualizing your QuickBooks financial data with interactive charts and detailed reports.

![Dashboard Preview](https://via.placeholder.com/800x450?text=QuickBooks+Dashboard+Preview)

## Features

- **Real-time Analytics**: Connect directly to QuickBooks API for live data
- **Financial Overview**: Track revenue, expenses, and profit metrics at a glance
- **Invoice Management**: View, filter, and manage all your invoices
- **Customer Insights**: Analyze customer spending patterns and relationships
- **Product Performance**: Monitor top-selling products and inventory
- **Interactive Charts**: Visualize your business data with beautiful charts
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Installation

```bash
# Clone the repository
git clone https://github.com/BANADDA/quickbooks-dashboard.git
cd quickbooks-dashboard

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Setup

1. Create a database directory:
```bash
mkdir -p data
```

2. Initialize the database:
```bash
python pipeline.py
```

3. Start the Flask server:
```bash
python app.py
```

4. Access the dashboard at http://localhost:5000

## QuickBooks API Integration

To connect with your QuickBooks account:

1. Create a developer account at [Intuit Developer](https://developer.intuit.com/)
2. Create a new app and get your Client ID and Client Secret
3. Create a `config.py` file with your credentials:

```python
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
REDIRECT_URI = "http://localhost:5000/callback"
ENVIRONMENT = "sandbox"  # Use "production" for real data
```

4. Uncomment the QuickBooks API packages in `requirements.txt`:
```
intuit-oauth
quickbooks-python
```

5. Install the additional dependencies:
```bash
pip install -r requirements.txt
```

6. Click the "Connect to QuickBooks" button on the dashboard

## Project Structure

```
quickbooks-dashboard/
├── app.py                   # Flask application
├── pipeline.py              # Data pipeline
├── database.py              # Database operations
├── quickbooks_extractor.py  # QuickBooks API integration
├── data_processor.py        # Data processing functions
├── data/                    # Database files
├── static/                  # Static assets
│   ├── css/                 # CSS stylesheets
│   │   └── styles.css       # Main stylesheet
│   └── js/                  # JavaScript files
│       └── dashboard.js     # Dashboard functionality
└── templates/               # HTML templates
    ├── base.html            # Base template
    ├── dashboard.html       # Main dashboard
    ├── customers.html       # Customers page
    ├── invoices.html        # Invoices page
    └── products.html        # Products page
```

## Dependencies

- Flask: Web framework
- SQLAlchemy: Database ORM
- Pandas: Data processing
- Chart.js: Interactive charts
- Intuit OAuth: QuickBooks authentication
- QuickBooks Python SDK: QuickBooks API integration

## Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [QuickBooks API](https://developer.intuit.com/)
- [Chart.js](https://www.chartjs.org/)
- [Font Awesome](https://fontawesome.com/) for icons
- [Inter Font](https://fonts.google.com/specimen/Inter) by Google Fonts 