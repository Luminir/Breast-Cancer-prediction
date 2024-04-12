# pip install pandas
import pandas as pandy
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import pickle as pickle

# Adjusting the data
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

def create_model(data):
    # predictors and target variables
    predictors = data.drop(['diagnosis'], axis = 1)
    targetVariables = data['diagnosis'] # just 'diagnosis' column

    # Scale the data
    scaler = StandardScaler()
    predictors = scaler.fit_transform(predictors)

    # Split the data
    predictors_train, predictors_test, targetVariables_train, targetVariables_test = train_test_split(
        # test_size = 20% / random_state = 42 becuz a lot of people use that for it
        predictors, targetVariables, test_size = 0.2, random_state=42
    )

    # Train model
    model = LogisticRegression()
    # fit the model to the data
    model = model.fit(predictors_train, targetVariables_train)
    
    # Test the model
    targetVariables_predict = model.predict(predictors_test)
    print("Accuracy of ML is ", accuracy_score(targetVariables_test, targetVariables_predict) )
    print("Classification report: \n", classification_report(targetVariables_test, targetVariables_predict))
    # Accuracy score of the model
    return model, scaler

# main content, clean data, debug
def main():
    # get data
    data = get_fixed_data()
    
    # train a machine learning model
    model, scaler = create_model(data)

    # WE DO NOT WANT them TO RUN CODES = TRAIN ML AGAIN & AGAIN
    # ==> WASTE storage
    # INSTEAD, WE DO THIS
    # BUILD THE MODEL ==> EXPORT as an already TRAINED file ==> FETCH TO your APP
    # save time and capacity
    with open('model/model.pkl', 'wb') as file:
        pickle.dump(model, file)
    with open('model/scaler.pkl', 'wb') as file:
        pickle.dump(scaler, file)

#Code run here
# Prevent run accidentally or run wrong file
if __name__ == '__main__':
    main()