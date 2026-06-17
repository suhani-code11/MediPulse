from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def predict_risk(heart_rate, spo2, temperature):
    if heart_rate > 120 or spo2 < 90 or temperature > 39:
        return "High"
    elif heart_rate > 100 or spo2 < 95 or temperature > 38:
        return "Medium"
    else:
        return "Low"

@app.route('/check', methods=['POST'])
def check():
    heart_rate = float(request.form['heart_rate'])
    spo2 = float(request.form['spo2'])
    temperature = float(request.form['temperature'])

    abnormal = []
    tips = []

    if not (60 <= heart_rate <= 100):
        abnormal.append(f"Heart Rate: {heart_rate} bpm")
        tips.append("Try to rest and breathe deeply if heart rate is high; see a doctor if very high or very low.")
    if not (95 <= spo2 <= 100):
        abnormal.append(f"SpO₂: {spo2}%")
        tips.append("Ensure proper oxygen; sit upright and breathe deeply; seek help if below 90%.")
    if not (36.1 <= temperature <= 37.2):
        abnormal.append(f"Temperature: {temperature} °C")
        tips.append("Stay hydrated and cool down if feverish; seek medical care if very high or low.")

    if abnormal:
        status = "Abnormal"
    else:
        status = "Normal"

    risk = predict_risk(heart_rate, spo2, temperature)

    return render_template(
        "results.html",
        status=status,
        abnormal=abnormal,
        tips=tips,
        risk=risk,
        heart_rate=heart_rate,
        spo2=spo2,
        temperature=temperature
    )
@app.route('/tips')
def tips():
    general_tips = [
        "Stay hydrated by drinking at least 8 glasses of water per day.",
        "Exercise regularly — at least 30 minutes of moderate activity daily.",
        "Eat a balanced diet rich in fruits, vegetables, and whole grains.",
        "Get at least 7–8 hours of sleep each night.",
        "Manage stress with deep breathing, meditation, or hobbies.",
        "Avoid smoking and limit alcohol consumption."
    ]
    return render_template("tips.html", tips=general_tips)




if __name__ == '__main__':
    app.run(debug=True)
