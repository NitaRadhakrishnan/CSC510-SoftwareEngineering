""" USECASE 2 TESTING """
import unittest
import json
import analysis

with open("/home/CSC510-23/Code/data.json") as json_file:
    DATA = json.load(json_file)
LIBRARIES = DATA["libraries"]
COLUMN_NAMES = DATA["columnNames"]
WRONG_COL_EX = DATA["wrongTargetColumnException"]
PARA_COUNT_CAT = 5
PARA_COUNT_NUM = 4


def contentcheck_categorical():
    """ Checks the lines in the file if the dataset given by user is categorical """
    filename = "Analysis.txt"
    temp_line = ""
    count = 0
    for line in open(filename, 'r'):
        temp_line = temp_line + line
    if "VALUE COUNTS" in temp_line:
        count = count + 1
    if "DATA INFORMATION" in temp_line:
        count = count + 1
    if "MEAN, MEDIAN AND MODE:" in temp_line:
        count = count + 1
    if "Correlation" in temp_line:
        count = count + 1
    if "Normality Tests" in temp_line:
        count = count + 1
    return count


def contentcheck_numerical():
    """ Checks the lines in the file if the dataset given by user is numerical """
    filename = "Analysis.txt"
    temp_line = ""
    count = 0
    for line in open(filename, 'r'):
        temp_line = temp_line + line
    if "DATA INFORMATION" in temp_line:
        count = count + 1
    if "MEAN, MEDIAN AND MODE:" in temp_line:
        count = count + 1
    if "Correlation" in temp_line:
        count = count + 1
    if "Normality Tests" in temp_line:
        count = count + 1
    return count


class TestyAnalysisMethods(unittest.TestCase):
    """ TEST CASES """
    # Use case 2 happy flow - to check the contents of the file produced after performing the EDA
    def test_analysis_categorical(self):
        """ Check if categorical """
        analysis.analysis_interaction("Datasets/Crime1.csv", "Category")
        count_cat = contentcheck_categorical()
        self.assertEqual(count_cat, PARA_COUNT_CAT)

    def test_analysis_numerical(self):
        """ Check if numerical """
        analysis.analysis_interaction("Datasets/Wine.csv", "Class")
        count_cat = contentcheck_numerical()
        self.assertEqual(count_cat, PARA_COUNT_NUM)

    # usecase 2 - alternate flow - if the wrong target column is provided
    def test_analysis_target_cat(self):
        """ Test the wrong column given scenario """
        self.assertEqual(analysis.analysis_interaction("Datasets/Crime1.csv", "test"), WRONG_COL_EX)

    def test_analysis_target_num(self):
        """ Test the wrong column given scenario """
        self.assertEqual(analysis.analysis_interaction("Datasets/Wine.csv", "test"), WRONG_COL_EX)

    # Checks if the result of execution of the call to Use case 2 is not empty
    def test_analysis_result_cat(self):
        """ Test the categorical data set """
        self.assertIsNotNone(analysis.analysis_interaction("Datasets/Crime1.csv", "Category"))

    def test_analysis_result_num(self):
        """ Test the numerical data set """
        self.assertIsNotNone(analysis.analysis_interaction("Datasets/Wine.csv", "Class"))

    # Checks if the file has been created after executing use case 2
    def test_file_creation(self):
        """ Test file creation"""
        self.assertIsNotNone(open("Analysis.txt", "r"))


if __name__ == '__main__':
    unittest.main()
