import os
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from flask import Flask, request, flash,render_template,url_for,redirect,jsonify
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn import metrics


from database import init_db, save_crop_prediction, save_soil_fertility
init_db()  # initialize database at app start


import pdfkit
from flask import render_template, make_response


# Path to wkhtmltopdf (update it according to your PC)
pdfkit_config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')

data=pd.read_csv('dataset.txt')
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('ProjectHomepage.html')
    
@app.route('/crop')
def crop():
    return render_template('crop_prediction.html') 

@app.route('/soilfertility',methods=['POST'])
def soilfertility():
    
    a0=float(request.form['0'])
    a1=float(request.form['1'])
    a2 =float(request.form['2'])
    a3 =float(request.form['3'])
    a4 =float(request.form['4'])
    a5=float(request.form['5'])
    a6=float(request.form['6'])
    a7 =float(request.form['7'])
    a8 =float(request.form['8'])
    a9 =float(request.form['9'])
    a10=float(request.form['10'])
    a11=float(request.form['11'])
    a12 =float(request.form['12'])
    a13=float(request.form['13'])


    if(a0==0 and a1==0 and a2==0 and a3==0 and a4==0 and a5==0 and a6==0 and a7==0 and a8==0 and a9==0 and a10==0 and a11==0 and a12==0 and a13==0):
        return render_template('ProjectHomepage.html',prediction_text=0)
    X, Y = data[data.columns[1:]], data['Vegetation Cover']
    dict={'NO3':[a0],'NH4':[a1],'P':[a2],'K':[a3],'SO4':[a4],'B':[a5],'Organic Matter':[a6],'pH':[a7],'Zn':[a8],'Cu':[a9],'Fe':[a10],'Ca':[a11],'Mg':[a12],'Na':[a13]}
    df1 = pd.DataFrame(dict)
    df = pd.concat([X, df1], ignore_index = True)
    df.reset_index()
    X=df
    scaler = MinMaxScaler()
    X, Y = scaler.fit_transform(X.values), scaler.fit_transform(Y.values.reshape(-1,1))
    l1=[X[408]]
    X = X[:-1]  

    X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size=0.10, random_state=43)

    forestRegressor = RandomForestRegressor(criterion='squared_error', max_depth=8, n_estimators=10, random_state=0)
    forestRegressor.fit(X_train, Y_train)
    y_pred = forestRegressor .predict(X_test)
    prediction = forestRegressor .predict(l1)
    print(l1)
    text=""
    recommendations1 = []
    recommendations2 = []
    if(prediction<90):
        if(a0<12.75 or a2<47 or a8<0.6 or a3<15 or a6<0.28 or a10<1):
            text="Your Soil is less fertile.You may try increasing these nutrients "
        if(a0<12.75):
            text=text+"NO3, "
            recommendations1.append("Ammonium-based fertilizers- These can be converted to nitrates by soil microbes. Fish emulsion- This is a quick-acting, natural nitrogen fertilizer derived from fish byproducts.Blood meal- This is a by-product of animal slaughter, rich in nitrogen. Coffee grounds- Mixing coffee grounds into the soil helps to increase the nitrogen content in the soil ")
            recommendations2.append("Urea (CH₄N₂O)-  A widely used nitrogen fertilize/ Calcium Nitrate (Ca(NO₃₂)) - Provides both calcium and nitrate/ Ammonium Nitrate (NH₄NO₃) - A fast-acting nitrogen source")
        if(a2<47):
            text=text+"P, "
            recommendations1.append("Apply Superphosphate or DAP (Di-Ammonium Phosphate)/Animal Manure/Bone Meal/Fish emulsion provides a phosphorus boost to plants with rapid results when used as a foliar spray/Compost with worm castings is an organic soil amendment that may add some phosphorus to soil, but more importantly, it frees up existing phosphorus/Lime/Rock Phosphate")
            recommendations2.append("Single Super Phosphate (SSP) - Contains water-soluble phosphorus/ Di-Ammonium Phosphate (DAP) - A high-phosphorus fertilizer/ Rock Phosphate - A slow-release, natural phosphorus source")
        if(a8<0.6):
            text=text+"Zn, "
            recommendations1.append("Add zinc sulfate: This is a common and effective way to supplement zinc in the soil. However, be cautious of over-fertilization, as excessive zinc can be toxic to plants./If your soil is acidic, applying lime can help improve zinc availability. However, be aware that excessive lime can also lead to zinc deficiency in alkaline soils. /Choose zinc-efficient crops: Planting crops that are naturally efficient in absorbing zinc, such as corn")
            recommendations2.append("Zinc Sulfate (ZnSO₄) - The most common zinc fertilizer/ Zinc Chelates (Zn-EDTA) - A highly bioavailable form of zinc/ Zinc Oxide (ZnO) - A slow-releasing zinc source")
        if(a3<15):
            text=text+"K, "
            recommendations1.append("Use Phosphorus-Rich Fertilizers: Apply balanced fertilizers with a phosphorus content (e.g., 10-20-10 NPK) according to soil test results and plant requirements./ Legumes and Cover Crops: Incorporate legumes like clover or beans, which fix atmospheric nitrogen and release phosphorus, into your crop rotation./ Incorporate compost, manure, or peat moss into the soil to release phosphorus gradually.")
            recommendations2.append("Muriate of Potash (KCl) - Most commonly used potassium fertilizer /Sulphate of Potash (K₂SO₄) - Provides both potassium and sulfur/ Potassium Nitrate (KNO₃) - Contains both potassium and nitrogen")
        if(a6<0.28):
            text=text+"Organic Matter, "
            recommendations1.append("Animal manure (FYM, poultry manure, etc.) can be used as a natural fertilizer, adding organic matter and nutrients to the soil./ Using earthworms to convert organic waste into compost (vermicomposting) is another effective method./ Biogas slurry can be used as a source of organic matter and nutrients./ Plant cover crops like legumes, grasses, or clover, which add organic matter and nutrients when incorporated into the soil.")
            recommendations2.append("Farmyard Manure (FYM) - Rich in nutrients and organic carbon/ Compost - Decomposed organic waste that enhances soil health/ Vermicompost - Nutrient-rich compost from earthworms")
        if(a10<1):
            text=text+"Fe, "
            recommendations1.append("Optimize phosphorus fertilization: Phosphorus and iron can react together to form insoluble iron phosphates, which can tie up iron./ Select iron-efficient crop varieties: Choose crop varieties that are less sensitive to iron deficiency./ Maintain Soil pH: Iron availability is affected by soil pH. Maintain a slightly acidic to neutral soil pH (around 6.0-7.0) to optimize iron uptake.")
            recommendations2.append("Ferrous Sulfate (FeSO₄) - The most common iron supplement/ Iron Chelates (Fe-EDTA, Fe-DTPA) - Highly available iron forms/ Ferric Oxide (Fe₂O₃) - A natural iron source in some soils")


    save_soil_fertility({
    'NO3': a0, 'NH4': a1, 'P': a2, 'K': a3, 'SO4': a4, 'B': a5,
    'Organic_Matter': a6, 'pH': a7, 'Zn': a8, 'Cu': a9, 'Fe': a10,
    'Ca': a11, 'Mg': a12, 'Na': a13,
    'prediction_score': float(prediction),
    'message': text
    })

    if(prediction>=90):
        text="Your soil is high fertile. Keep regular fertilization methods as of now to stand soil as it is"		
    if(prediction>0 and prediction<1):
        return render_template('Results.html',content=text,co = recommendations2, c=recommendations1, prediction_text=np.round(prediction*100).astype(int))


@app.route('/predict', methods=['POST'])
def predict():
    # Load dataset
    data = pd.read_csv('Crop.csv')

    # Encoding labels
    label1 = data.iloc[:, 7]
    label_encoder = LabelEncoder()
    encoded_crops = label_encoder.fit_transform(label1)

    # Training starts
    X = data.iloc[:, 0:7]
    y = encoded_crops

    # Train-test split
    X_train1, X_test, y_train1, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
    X_train, X_val, y_train, y_val = train_test_split(X_train1, y_train1, test_size=0.2, random_state=2022)

    # Random Forest model
    RF = RandomForestClassifier()
    RF.fit(X_train, y_train)

    # Predictions
    if request.method == 'POST':
        N = float(request.form['N'])
        P = float(request.form['P'])
        K = float(request.form['K'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])

        prediction_data = [[N, P, K, temperature, humidity, ph, rainfall]]
        prediction = RF.predict(prediction_data)
        predicted_crop = label_encoder.inverse_transform(prediction)[0]

        crop_info_detailed = {
            "rice": {
                        "days_to_harvest": 120,
                        "description": (
                            "Rice is a staple food crop widely cultivated in India, particularly in states like Maharashtra during the Kharif season. "
                            "It requires abundant water, hence is grown in areas with good rainfall or irrigation facilities. "
                            "The crop is usually transplanted in puddled fields to ensure root anchoring and weed suppression. "
                            "It thrives in a hot and humid climate with temperatures ranging between 20°C to 35°C. "
                            "Fertile alluvial or clayey loam soils with good water retention are ideal for rice. "
                            "It demands significant labor, especially during transplanting and harvesting stages. "
                            "Rice is harvested after the grains mature and turn golden yellow, typically in about 3-4 months."
                        )
                    },

            "maize": {
                        "days_to_harvest": 90,
                        "description": (
                            "Maize, also known as corn, is a versatile crop used for food, fodder, and industrial purposes. "
                            "It is cultivated across Maharashtra during the Kharif and Rabi seasons. "
                            "Maize requires well-drained loamy soil and grows best in regions receiving moderate rainfall. "
                            "The crop prefers warm weather with a temperature range of 18°C to 27°C. "
                            "It is relatively drought-resistant but benefits from proper irrigation at key growth stages. "
                            "Maize is a high-yielding crop when managed with proper fertilizers and pest control. "
                            "It is typically harvested when the husks turn brown and the kernels are hard and glossy."
                        )
                    },     

            "jute": {
                        "days_to_harvest": 150,
                        "description": (
                            "Jute is a long, soft, shiny vegetable fiber that can be spun into coarse, strong threads. "
                            "It is mainly grown in humid and warm climates, requiring a high level of rainfall (150-200 cm). "
                            "Although not commonly grown in Maharashtra, experimental cultivation has shown promise in suitable pockets. "
                            "The crop is typically sown in spring and harvested in late summer or early autumn. "
                            "It prefers well-drained alluvial soils that are rich in nutrients. "
                            "Jute is eco-friendly and used in making gunny bags, ropes, and carpets. "
                            "After harvesting, the fiber is extracted through a process called retting, where stalks are soaked in water."
                        )
                    }, 

            "cotton":{
                        "days_to_harvest": 180,
                        "description": (
                            "Cotton is a major cash crop cultivated extensively in Maharashtra, particularly in Vidarbha and Marathwada. "
                            "It requires a warm climate and is best suited for black cotton soil rich in lime, potash, and humus. "
                            "Cotton is grown during the Kharif season and thrives with 600-1000 mm of rainfall. "
                            "It is sensitive to waterlogging, so well-drained fields are essential. "
                            "The crop is prone to pests like bollworms and requires integrated pest management. "
                            "Harvesting starts when the bolls burst open, revealing white fluffy fibers. "
                            "Cotton is crucial to the textile industry and generates employment in both agriculture and industry."
                        )
                    }, 

            "coconut":{
                        "days_to_harvest": 365,
                        "description": (
                            "Coconut is a perennial tropical crop grown in coastal regions with high humidity. "
                            "In Maharashtra, it is cultivated mainly in the Konkan region. "
                            "The crop requires well-drained sandy or alluvial soil and thrives in areas with over 1500 mm rainfall annually. "
                            "It takes about a year or more for the fruits to mature for harvesting. "
                            "Regular watering, manuring, and protection from pests like rhinoceros beetles are important for good yields. "
                            "Coconuts are harvested monthly once the trees start bearing fruit after 5-6 years. "
                            "The crop is valued for its oil, water, coir, and as a key ingredient in various cuisines."
                        )
                    },


             "papaya": {
                            "days_to_harvest": 150,
                            "description": (
                                "Papaya is a fast-growing fruit crop ideal for tropical and subtropical climates. "
                                "It is cultivated in many parts of Maharashtra due to its short growth cycle and market demand. "
                                "Well-drained sandy loam soils with a pH of 6-7 are best suited for papaya. "
                                "The plant begins bearing fruit within 5-6 months after planting and continues for several years. "
                                "It requires regular irrigation and protection from frost and strong winds. "
                                "Papaya is rich in vitamins A and C and is used for both direct consumption and processing. "
                                "The crop also contains an enzyme, papain, used in meat tenderization and pharmaceuticals."
                            )
                        }, 


             "orange": {
                            "days_to_harvest": 240,
                            "description": (
                                "Orange is a popular citrus fruit widely grown in Nagpur, known as the 'Orange City'. "
                                "The crop prefers deep loamy soil and subtropical climates with moderate rainfall. "
                                "Oranges require 7-8 months from flowering to harvest. "
                                "Irrigation, proper fertilization, and pest control are critical for healthy fruit development. "
                                "Trees are pruned and managed to maintain shape and encourage better fruiting. "
                                "Oranges are a good source of Vitamin C and have high market value. "
                                "They are consumed fresh and also processed into juice and marmalade."
                            )
                        }, 

            "apple":{
                            "days_to_harvest": 180,
                            "description": (
                                "Apple is a temperate fruit crop not naturally suited to Maharashtra’s tropical climate but grown experimentally in cooler regions. "
                                "It requires chilling hours to break dormancy, hence best suited to hilly areas. "
                                "Apples grow in well-drained loamy soils with adequate organic matter. "
                                "Proper pruning and training are required to ensure sunlight penetration and air circulation. "
                                "Pollination is usually aided by bees, and cross-pollination enhances fruit set. "
                                "Apples are harvested when they attain full size and color. "
                                "They are consumed raw, used in baking, and processed into juice and cider."
                            )
                    },  


            "muskmelon": {
                            "days_to_harvest": 80,
                            "description": (
                                "Muskmelon is a warm-season fruit crop commonly grown in Maharashtra during the summer. "
                                "It requires well-drained sandy loam soil and a hot, dry climate for best growth. "
                                "Irrigation should be carefully managed, especially during flowering and fruit setting stages. "
                                "The fruit is harvested when it develops a sweet aroma and the netting on the skin is well developed. "
                                "Muskmelons are rich in vitamins and water content, making them ideal for hydration. "
                                "They are consumed fresh and are commonly used in salads and beverages. "
                                "It’s a short-duration crop giving quick returns to farmers."
                            )
                        },

            "watermelon": {
                            "days_to_harvest": 90,
                            "description": (
                                "Watermelon is a popular summer fruit grown extensively in Maharashtra under warm and dry conditions. "
                                "It prefers sandy loam soil with good drainage and full sunlight. "
                                "Water management is crucial; less water during ripening ensures sweeter fruits. "
                                "Harvesting is done when the fruit shows a yellow patch at the bottom and makes a dull sound on tapping. "
                                "It is known for its high water content and cooling properties. "
                                "Watermelons are consumed fresh or as juice and are high in antioxidants. "
                                "It’s a fast-growing vine crop ideal for short growing seasons."
                            )
                        },

            "grapes": {
                            "days_to_harvest": 140,
                            "description": (
                                "Grapes are a commercial fruit crop widely cultivated in Maharashtra, especially in Nashik. "
                                "They require a dry climate during the ripening stage and grow best in loamy, well-drained soil. "
                                "Proper canopy management and pruning are crucial for quality yield. "
                                "Irrigation must be controlled during ripening to prevent fruit cracking. "
                                "Grapes are harvested when berries are fully colored and sweet. "
                                "They are consumed fresh, dried as raisins, or used for making wine and juices. "
                                "Pest management is essential, particularly for mealybugs and fungal diseases."
                            )
                        },


            "mango": {
                        "days_to_harvest": 150,
                        "description": (
                            "Mango is the king of fruits and a major summer crop in Maharashtra, especially in Konkan and Marathwada. "
                            "It prefers well-drained lateritic or loamy soil and thrives in tropical conditions. "
                            "Mango trees require minimal irrigation once established, and flowering is triggered by dry spells. "
                            "The fruit is harvested when mature, indicated by swelling shoulders and color change. "
                            "Mangoes are used for fresh consumption, pickles, pulp, and juice. "
                            "Alphonso and Kesar are famous varieties from Maharashtra. "
                            "Regular pruning and pest control help ensure quality production."
                        )
                    }, 

            "banana": {
                            "days_to_harvest": 100,
                            "description": (
                                "Banana is a year-round fruit crop grown in Maharashtra, particularly in Jalgaon district. "
                                "It prefers warm, humid conditions and rich loamy soil with good water retention. "
                                "Banana plants need frequent irrigation and fertilization for optimal growth. "
                                "The crop is harvested when fingers are well-developed and angles are rounded. "
                                "Bananas are consumed raw, used in snacks, processed as puree and chips. "
                                "Tissue culture planting is popular for uniform growth and disease resistance. "
                                "The crop requires staking or propping to support heavy bunches."
                            )
                        },

            "pomegranate": {
                                "days_to_harvest": 100,
                                "description": (
                                    "Pomegranate is a drought-tolerant fruit crop extensively cultivated in Maharashtra, especially in Solapur and Ahmednagar. "
                                    "It grows well in light loamy to black soil with good drainage. "
                                    "The crop is highly profitable due to its high market value and export potential. "
                                    "It is pruned and irrigated systematically for flowering and fruiting control. "
                                    "Fruits are harvested when the skin turns red and the fruit gives a metallic sound. "
                                    "Pomegranates are consumed fresh, juiced, or used in syrups and medicinal extracts. "
                                    "Fruit cracking and bacterial blight are common issues requiring proper care."
                                )
                            },

            "lentil": {
                            "days_to_harvest": 100,
                            "description": (
                                "Lentil is a cool-season legume grown as a rabi crop in Maharashtra. "
                                "It prefers well-drained loamy soil with neutral to slightly alkaline pH. "
                                "It is drought-tolerant and requires minimal irrigation. "
                                "The crop is sown in November and harvested in February–March. "
                                "Lentils are a rich source of protein and are consumed in various forms like dal and sprouts. "
                                "Proper pest and weed management ensures a healthy yield. "
                                "It helps fix nitrogen in the soil, improving soil fertility."
                            )
                        },  


            "blackgram": {
                            "days_to_harvest": 90,
                            "description": (
                                "Blackgram, also known as urad dal, is a kharif or rabi pulse grown across Maharashtra. "
                                "It thrives in loamy to clayey soils with good moisture-retention capacity. "
                                "It is often grown under rainfed conditions with minimal inputs. "
                                "The plant improves soil health by fixing atmospheric nitrogen. "
                                "It is harvested when the pods turn black and dry. "
                                "Used in Indian cuisine for dals, idlis, and vadas. "
                                "It is also used as a green manure and intercrop in cotton or sugarcane fields."
                            )
                        },

            "mungbean": {
                            "days_to_harvest": 65,
                            "description": (
                                "Mungbean (moong) is a short-duration pulse widely grown in summer and kharif seasons. "
                                "It prefers well-drained loamy or sandy soils with neutral pH. "
                                "Being drought-resistant, it is suitable for dryland farming. "
                                "Mungbean requires less water and gives a quick return to farmers. "
                                "The crop is ready when pods turn brown and dry. "
                                "It is rich in protein and is used for dal, sprouts, and sweets. "
                                "It also enhances soil fertility through nitrogen fixation."
                            )
                        },

            "mothbeans": {
                            "days_to_harvest": 70,
                            "description": (
                                "Mothbeans are hardy leguminous crops suited for arid and semi-arid regions of Maharashtra. "
                                "They tolerate drought and poor soils, thriving in sandy or light loam. "
                                "They are usually grown in the kharif season under rainfed conditions. "
                                "Pods are harvested when fully matured and dried. "
                                "The beans are used in traditional dishes like matki usal and are highly nutritious. "
                                "Mothbeans are also useful as green manure and fodder. "
                                "Minimal input and early maturity make it a low-risk crop."
                            )
                        },
            
            "pigeonpeas": {
                                "days_to_harvest": 150,
                                "description": (
                                    "Pigeonpea (tur/arhar) is a major pulse crop grown in kharif season across Maharashtra. "
                                    "It grows well in black cotton soil and medium rainfall regions. "
                                    "It is deep-rooted and drought-tolerant, making it ideal for dryland farming. "
                                    "It is often intercropped with cereals or oilseeds. "
                                    "Harvested when pods turn brown and dry. "
                                    "It is a staple pulse in Indian cuisine and used in dals and curries. "
                                    "The crop also improves soil health through nitrogen fixation."
                                )
                            },

            "kidneybeans": {
                                "days_to_harvest": 110,
                                "description": (
                                    "Kidney beans (rajma) are grown in Maharashtra's cooler and higher-altitude regions. "
                                    "They require well-drained loamy soil and moderate temperatures (15°C–25°C). "
                                    "Excess moisture and waterlogging must be avoided. "
                                    "The crop is usually sown in the rabi or summer season in appropriate climates. "
                                    "Harvesting occurs when pods mature and dry. "
                                    "Kidney beans are rich in protein and fiber, used in gravies and curries. "
                                    "They require boiling or pressure cooking before consumption."
                                )
                            },

            "chickpea": {
                            "days_to_harvest": 100,
                            "description": (
                                "Chickpea (chana) is a key rabi pulse grown extensively in Maharashtra. "
                                "It thrives in black cotton soil with good moisture retention. "
                                "Cool, dry weather is ideal during flowering and pod formation. "
                                "It requires minimal irrigation and is suited for low-input farming. "
                                "Harvesting is done when plants turn brown and pods dry out. "
                                "Chickpeas are used in curries, snacks, and flour (besan). "
                                "The crop also improves soil fertility through biological nitrogen fixation."
                            )
                        },

            "coffee": {
                            "days_to_harvest": 270,
                            "description": (
                                "Coffee is not a native crop of Maharashtra but is grown in experimental farms and some cooler, shaded regions. "
                                "It requires a tropical climate with moderate temperature (15°C–30°C) and shade. "
                                "Grows best in well-drained loamy soil rich in organic matter. "
                                "Regular irrigation and mulching are necessary during dry periods. "
                                "Coffee berries are harvested once they turn bright red. "
                                "Beans are extracted through pulping, fermented, and dried before roasting. "
                                "Arabica and Robusta are the main varieties, used for preparing beverages."
                            )
                        }            
    }   
    
        if predicted_crop in crop_info_detailed:
            info = crop_info_detailed[predicted_crop]

        save_crop_prediction({
            'N': N, 'P': P, 'K': K, 'temperature': temperature, 'humidity': humidity,
            'ph': ph, 'rainfall': rainfall,
            'predicted_crop': predicted_crop,
            'days_to_harvest': info['days_to_harvest'],
            'description': info['description']
        })


        return render_template('Result2.html', details=info , predicted_crop=predicted_crop)

if __name__ == "__main__":
    app.run(debug=True)


