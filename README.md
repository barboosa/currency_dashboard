# Currency Dashboard
A Dashboard for Analyzing Currency Trends and Correlations based on Historical Events

## Installation
To install and run the currency dashboard you will need to start the backend first, and afer that the frontend. Before we begin make sure to clone the project and install all necessary requirements. You can find the required packages in the "requirements.txt" file.
```
git clone https://github.com/barboosa/currency_dashboard.git
cd currency_dashboard
pip install -r requirements.txt
```
### Backend
To run the backend execute following commands.
```
cd backend 
gunicorn app:main -b 127.0.0.1:8000
```
### Frontend
To run the frontend execute following commands.
```
cd frontend 
gunicorn app:server -b 127.0.0.1:8050
```
## Usage


## Testing

## License
Distributed under the MIT License. See LICENSE.txt for more information.