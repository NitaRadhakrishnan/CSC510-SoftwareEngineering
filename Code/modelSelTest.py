# Python code to demonstrate working of unittest using mock
import operator
import unittest
import json
import modelSelection

with open("data.json") as json_file:
    data = json.load(json_file)
libraries = data["libraries"]
columnNames = data["columnNames"]
modelDict = data["listModels"]
wrngColEx = data["wrongTargetColumnException"]
parameters_to_be_counted = int(data["parameters_to_be_counted"])
target = data["target"]
wrong_target = data["wrong_target"]
path_to_csv_file_case1_case2 = data["path_to_csv_file_case1_case2"]
filename = data["path_for_usecase2"]

# USECASE 1
def best_models():
    ls = []
    accr = 0
    for models in modelDict:
        if accr<modelDict[models]:
            accr = modelDict[models]
    for model in modelDict:
        if accr == modelDict[model]:
            ls.append(model)
    return ls

class TestStringMethods(unittest.TestCase):
    # usecase 1 - happy flow
    def test_modelsel(self):
        ls = best_models()
        bestMod = modelSelection.modelSelInteraction(path_to_csv_file_case1_case2, target)
        flag = 0
        for model in ls:
            if model not in bestMod:
                flag = 1
                break
        self.assertEquals(flag,0) and self.assertEquals(len(ls),len(bestMod))

    # usecase 1 - alternate flow
    def test_modelsel2(self):
       self.assertEqual(modelSelection.modelSelInteraction(path_to_csv_file_case1_case2, wrong_target), wrngColEx)

    def test_modelsel3(self):
        self.assertIsNotNone(modelSelection.modelSelInteraction("Crime1.csv","Category"))

if __name__ == '__main__':
    unittest.main()