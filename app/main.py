import streamlit as strlit
import pandas as pandy
import pickle as pickle
import plotly.graph_objects as go
import numpy as numpy

def get_fixed_data():
    data = pandy.read_csv("data/wdbc.csv")

    # return n header of data( default limit of n is 5)
    data = data.drop(['id', 'Unnamed: 32'], axis = 1)

    # column 'diagnosis', give value for: M = 1, B = 0
    # M = Malignancy (ác tính), B = Benigancy (lành tính)
    data['diagnosis'] = data['diagnosis'].map({'M': 1, 'B': 0})
    # print(data.head()) # checking first 5 rows, columns
    # print(data.info()) # checking rows
    return data


def sidebar():
    strlit.sidebar.header("Cell Nuclei Details")
    data = get_fixed_data()

    slide_labels = [
        ("Radius (mean)", "radius_mean"),
        ("Texture (mean)", "texture_mean"),
        ("Perimeter (mean)", "perimeter_mean"),
        ("Area (mean)", "area_mean"),
        ("Smoothness (mean)", "smoothness_mean"),
        ("Compactness (mean)", "compactness_mean"),
        ("Concavity (mean)", "concavity_mean"),
        ("Concave points (mean)", "concave points_mean"),
        ("Symmetry (mean)", "symmetry_mean"),
        ("Fractal dimension (mean)", "fractal_dimension_mean"),
        ("Radius (se)", "radius_se"),
        ("Texture (se)", "texture_se"),
        ("Perimeter (se)", "perimeter_se"),
        ("Area (se)", "area_se"),
        ("Smoothness (se)", "smoothness_se"),
        ("Compactness (se)", "compactness_se"),
        ("Concavity (se)", "concavity_se"),
        ("Concave points (se)", "concave points_se"),
        ("Symmetry (se)", "symmetry_se"),
        ("Fractal dimension (se)", "fractal_dimension_se"),
        ("Radius (worst)", "radius_worst"),
        ("Texture (worst)", "texture_worst"),
        ("Perimeter (worst)", "perimeter_worst"),
        ("Area (worst)", "area_worst"),
        ("Smoothness (worst)", "smoothness_worst"),
        ("Compactness (worst)", "compactness_worst"),
        ("Concavity (worst)", "concavity_worst"),
        ("Concave points (worst)", "concave points_worst"),
        ("Symmetry (worst)", "symmetry_worst"),
        ("Fractal dimension (worst)", "fractal_dimension_worst"),
    ]

    input_collection = {}

    for label, key in slide_labels:
       input_collection[key] = strlit.sidebar.slider(
            label = label,
            min_value= float(0),

            # Ascociate the data with the key
            max_value= float(data[key].max()),

            # set default value = average of that category
            value= float(data[key].mean())
        )
    return input_collection

# return the dictionary between 0 and 1
def get_scaled_val(input_dictionary):
    data = get_fixed_data()
    predictors = data.drop(['diagnosis'], axis=1)

    scaled_dictionary = {}

    for key, val in input_dictionary.items():
        max_val = predictors[key].max()
        min_val = predictors[key].min()

        # We set set range at get_radar_chart = [0,1] so:
        scaled_val = (val - min_val) / (max_val - min_val)

        scaled_dictionary[key] = scaled_val

    return scaled_dictionary


def get_radar_chart(data):
    
    data = get_scaled_val(data)

    categories = ['Radius', 'Texture', 'Perimeter', 'Area', 'Smoothness', 'Compactness', 'Concavity', 'Concave Points','Symmetry', 'Fractal Dimension']

    fig = go.Figure()

    # data = input_data in MAIN => input_data = sidebar()
    # Chart 1
    fig.add_trace(go.Scatterpolar(
        # default chart number of a catogory
        r=[
            data['radius_mean'], data['texture_mean'], data['perimeter_mean'],data['area_mean'], data['smoothness_mean'], data['compactness_mean'],
            data['concavity_mean'], data['concave points_mean'], data['symmetry_mean'], data['fractal_dimension_mean']
        ],
        theta=categories,
        fill='toself',
        name='Mean Value'
    ))
    # Chart 2
    fig.add_trace(go.Scatterpolar(
        r=[ data['radius_se'], data['texture_se'], data['perimeter_se'], data['area_se'],data['smoothness_se'], 
            data['compactness_se'], data['concavity_se'],data['concave points_se'], data['symmetry_se'],data['fractal_dimension_se']],
        theta=categories,
        fill='toself',
        fillcolor='rgba(0, 255, 0, 0.5)',  # Specify the fill color (red with 50% opacity)
        line_color='rgba(0, 100, 0, 0.5)',  # Specify the line color (red)
        name='Standard Error'
    ))
    # Chart 3
    fig.add_trace(go.Scatterpolar(
        r=[
          data['radius_worst'], data['texture_worst'], data['perimeter_worst'],data['area_worst'], 
          data['smoothness_worst'], data['compactness_worst'],data['concavity_worst'], 
          data['concave points_worst'], data['symmetry_worst'],data['fractal_dimension_worst']
        ],
        theta=categories,
        fill='toself',
        name='Worst Value'
    ))

    fig.update_layout(
    polar=dict(
        radialaxis=dict(
        visible=True,
        range=[0, 1]
        )),
    showlegend=True
    )
    return fig

# importing TRAINED model (not trainning model while using app) into our app.
def add_predictions(data):
    # read binary file
    model = pickle.load(open("model/model.pkl", "rb")) 
    scaler = pickle.load(open("model/scaler.pkl", "rb"))

    # CONVERT data from our input => single array with val
    inputArr = numpy.array(list(data.values())).reshape(1, -1)

    # Scaler => makes the default numbers to be 0, as 0 is the MEASURING LINE.
    inputArr_scaled = scaler.transform(inputArr)
    # strlit.write(inputArr_scaled)

    # Make prediction based on the numbers
    prediction = model.predict(inputArr_scaled)
    # strlit.write(prediction)

    strlit.subheader("Cell cluster prediction")
    # strlit.subheader("Dự đoán cụm tế bào:")

    if prediction[0] == 0:
        strlit.write("<span class='diagnosis benign'>Benign/ Lành tính</span>", unsafe_allow_html= True)
    else:
        strlit.write("<span class='diagnosis malicious'>Malicious/ Ác tính</span>", unsafe_allow_html= True)

    strlit.write(f"Probaility of being benign: ", model.predict_proba(inputArr_scaled)[0][0]*100, "%")
    strlit.write("Probaility of being malicious: ", model.predict_proba(inputArr_scaled)[0][1]*100, "%")
    # strlit.write("Probability of being benign: {:.2f}%".format(model.predict_proba(inputArr_scaled)[0][0]*100))
    # strlit.write("Probability of being malignant: {:.2f}%".format(model.predict_proba(inputArr_scaled)[0][1]*100))
    strlit.write("Help assisting professionals in diagnosing Breast Cancer in patients.")
    strlit.write("\u26A0️ NOTE: NOT a subtitute for professional diagnosis.")

def main():
    strlit.set_page_config(
        page_title="Breast Cancer Predictor",
        page_icon=":female_doctor:",
        layout="wide",
        initial_sidebar_state="expanded",
        )
    # strlit.markdown(f"<h1 style='text-align: center;'>{}</h1>", unsafe_allow_html=True)
    
    # css
    with open("style/style.css") as file:
        strlit.markdown("<style>{}<style>".format(file.read()), unsafe_allow_html= True)

    input_data = sidebar()
    # TESTING: strlit.write(input_data) 

    # streamlit.container = <div>
    with strlit.container():
        # create header
        strlit.title("Breast Cancer Prediction")
        strlit.write("An app help diagnose breast cancer through tissue sample. This app predicts using a machine learning model whether a breast mass is benign or malignant based on the measurements it received. Can be used by either plug it into the machine doing the measurements or do it by hand.")
        strlit.write(" NOTE: The data is from Wincosin")
        
    column1, column2 = strlit.columns([3,1])

    with column1:
        # strlit.write("Column 1")
        # Injecting the data into our radar chart
        chart = get_radar_chart(input_data)

        # Injecting chart into streamlit app
        strlit.plotly_chart(chart)
    with column2:
        # strlit.write("Column 2")
        add_predictions(input_data)

if __name__ == '__main__':
    main()