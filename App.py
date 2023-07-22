from flask import Flask, render_template, request
import joblib
from sklearn.preprocessing import StandardScaler
import numpy as np

app = Flask(__name__)

# Load the trained model
model = joblib.load('fraud_model.pkl')

# Load the scaler
scaler = joblib.load('st_scaler.pkl')

# Define the home route
@app.route('/')
def home():
    return render_template('index.html')

# Define the prediction route
@app.route('/predict', methods=['POST'])
def predict():
    # Get the input values from the form
    transaction_amount = float(request.form['transaction_amount'])
    declines_per_day = int(request.form['declines_per_day'])
    is_foreign_transaction = int(request.form['is_foreign_transaction'])
    is_high_risk_country = int(request.form['is_high_risk_country'])
    daily_chargeback_avg_amt = float(request.form['daily_chargeback_avg_amt'])
    six_month_avg_chbk_amt = float(request.form['six_month_avg_chbk_amt'])
    six_month_chbk_freq = int(request.form['six_month_chbk_freq'])
    total_transaction_amount = float(request.form['total_transaction_amount'])
    declines_level = int(request.form['declines_level'])

    # Create a feature array for scaling
    features = [
        transaction_amount, declines_per_day, daily_chargeback_avg_amt,
        six_month_avg_chbk_amt, six_month_chbk_freq,
        total_transaction_amount
    ]

    unscaled = [
is_foreign_transaction,is_high_risk_country,declines_level

    ]

    # Apply StandardScaler to the features
    scaled_features = scaler.transform([features])

    # Concatenate scaled and unscaled features
    all_features = np.concatenate((scaled_features, [unscaled]), axis=1)

    # Perform prediction using the loaded model
    prediction = model.predict(all_features)[0]

    # Set the prediction message based on the result
    if prediction == 1:
        prediction_message = "This transaction is fraudulent."
    else:
        prediction_message = "This transaction is not fraudulent."

    # Render the prediction result template
    return render_template('result.html', prediction=prediction_message)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
