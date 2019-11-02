from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import pandas as pd
import modelTraining as mt
import commonFunctions as cf

def bestModel(modelDict,f):
    if len(modelDict)==0:
        f.writelines("\n      No model to satisfy this dataset")
        return ["No model to satisfy this dataset"]
    accr = 70
    models = []
    for model in modelDict:
        if accr<=modelDict[model]:
            accr = modelDict[model]
    for model in modelDict:
        if accr == modelDict[model]:
            models.append(model)

    return models if len(models)>0 else ["No decent model to satisfy this dataset"]

def prepAndSplit1(data, target, column_names, f):
    # read data
    column_names.pop(column_names.index(target))
    f.writelines("\nStep 3: Spliting the target column from the dataset")
    X = data.reindex(columns = column_names)
    X = preprocessing.StandardScaler().fit(X).transform(X.astype(float))
    f.writelines("\nStep 4: Preprocessing using sklearn package")

    # Assign the target column to a variable
    Y = data[target]

    # Split the datase into training and testing dataset
    f.writelines("\nStep 5: Spliting the training and testing data in 80:20 ratio")
    X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(X, Y, data.index, test_size=0.2,
                                                                                     random_state=0)
    return X_train,X_test,y_train,y_test

def prepAndSplit2(data,target,column_names,f):
    column_names.pop(column_names.index(target))
    X = data.reindex(columns=column_names)
    Y = data[target]
    X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(X, Y, data.index, test_size=0.2,
                                                                                     random_state=0)
    return X_train, X_test, y_train, y_test

def modelSelInteraction(path,target):
    data = pd.read_csv(path, sep=',', header=0)
    data2, column_names, cat_flag = cf.preprocessS1(data,target)
    if column_names==[]:
        return data2
    f = open("modelSelectionProcess.txt", "w")
    f.writelines(
        "\nThe following is the process the bot performed to arrived at the best model for the provided dataset.")
    f.writelines("\n***************************MODEL SELECTION PROCESS**********************")
    f.writelines("\nThe file name is: "+str(path.split("/")[-1]))
    f.writelines("\nStep 1: Check if the target is present in the column names of the dataset")
    f.writelines("\nStep 2: Check if the columns are numerical or categorical. If categorical, factorize.")
    if cat_flag == 0:
        f.writelines("\n      The dataset is of type - Numerical")
    else:
        f.writelines("\n      The dataset is of type - Categorical")
    f.writelines("\n      The dataset contains column names (after pre-processing stage 1): "+str(column_names))
    f.writelines(data2.head())
    X_train, X_test, y_train, y_test = prepAndSplit1(data2,target,column_names,f)
    f.writelines("\nStep 6: Training and testing with various models")
    models = mt.modelTraining(X_train, X_test, y_train, y_test, f);
    f.writelines("\nStep 7: Finding the best model:")
    bestMod = bestModel(models, f)
    if bestMod == ["No decent model to satisfy this dataset"]:
        f.writelines("\n      No decent model to satisfy this dataset. All the accuracies are below 70%")
    else:
        f.writelines("\n      Best Model(s):")
        for i in bestMod:
            f.writelines("\n          "+str(i))
    if cat_flag == 1:
        f.writelines("\n***Performing n-gram feature classification on each Categorical column to check if there is scope of better accuracy model***")
        cf.ngram(data,target,f)

    f.close()
    return bestMod
