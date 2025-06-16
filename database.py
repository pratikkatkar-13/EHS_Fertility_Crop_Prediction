import sqlite3

def init_db():
    conn = sqlite3.connect('agriculture.db')
    cursor = conn.cursor()

    # Create table for crop prediction
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crop_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            N REAL, P REAL, K REAL,
            temperature REAL, humidity REAL, ph REAL, rainfall REAL,
            predicted_crop TEXT,
            days_to_harvest INTEGER,
            description TEXT,
            prediction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create table for soil fertility
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS soil_fertility (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            NO3 REAL, NH4 REAL, P REAL, K REAL, SO4 REAL, B REAL,
            Organic_Matter REAL, pH REAL, Zn REAL, Cu REAL, Fe REAL,
            Ca REAL, Mg REAL, Na REAL,
            prediction_score REAL,
            message TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()


def save_crop_prediction(data):
    conn = sqlite3.connect('agriculture.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO crop_predictions (
            N, P, K, temperature, humidity, ph, rainfall,
            predicted_crop, days_to_harvest, description
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['N'], data['P'], data['K'], data['temperature'], data['humidity'], data['ph'], data['rainfall'],
        data['predicted_crop'], data['days_to_harvest'], data['description']
    ))

    conn.commit()
    conn.close()


def save_soil_fertility(data):
    conn = sqlite3.connect('agriculture.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO soil_fertility (
            NO3, NH4, P, K, SO4, B, Organic_Matter, pH, Zn, Cu, Fe, Ca, Mg, Na, prediction_score, message
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['NO3'], data['NH4'], data['P'], data['K'], data['SO4'], data['B'],
        data['Organic_Matter'], data['pH'], data['Zn'], data['Cu'], data['Fe'],
        data['Ca'], data['Mg'], data['Na'], data['prediction_score']*100, data['message']
    ))

    conn.commit()
    conn.close()
