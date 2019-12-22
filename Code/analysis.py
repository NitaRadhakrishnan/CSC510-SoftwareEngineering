""" Python program for Usecase 2 - Analysis """
import pandas as pd
from scipy.stats import shapiro
from scipy.stats import normaltest
from scipy.stats import anderson
from tabulate import tabulate
import commonFunctions


def correlations(data, method, columns, f_name):
    """ FUNCTION TO FIND CORRELATION BETWEEN ALL VARIABLES IN THE DATASET """
    corr_var = data[data.columns].corr(method=method)
    for i in range(len(columns) - 1):
        for j in range(i + 1, len(columns)):
            if abs(corr_var[columns[i]][columns[j]]) < 0.5:
                f_name.writelines("\nColumns " + columns[i] + " and " + columns[j] +
                                  " have low correlation between them. The correlation value is " +
                                  str(corr_var[columns[i]][columns[j]]))
            elif abs(corr_var[columns[i]][columns[j]]) > 0.98:
                f_name.writelines("\nColumns " + columns[i] + " and " + columns[j] +
                                  " have very high correlation between them. "
                                  "The correlation value is " +
                                  str(corr_var[columns[i]][columns[j]]))
            else:
                f_name.writelines("\nColumns " + columns[i] + " and " + columns[j] +
                                  " have strong correlation between them. "
                                  "The correlation value is "
                                  + str(corr_var[columns[i]][columns[j]]))
    f_name.writelines(
        "\n---------------------------------------------------------------------------"
        "---------------------------------"
        "---------------------------")


def analysis(f_name, data, target, columns):
    """ FUNCTION TO WRITE ALL EDA RESULTS TO FILE AND RETURN FILE """
    # Exploratory data analysis:
    f_name.writelines("\nEXPLORATORY DATA ANALYSIS:")
    # Checking for Value counts if dataset is categorical
    for col in columns:
        if not (data[col].dtypes == 'float64' or data[col].dtypes == 'int64'):
            value_counts(f_name, data, col)
    # Writes the type of the data set (Categorical/Numerical) in the text file
    data, columns, cat_flag = commonFunctions.checkAndConvertIfCategorical(data, target)
    if cat_flag == 0:
        f_name.writelines("\n      The dataset is of type - Numerical")
    else:
        f_name.writelines("\n      The dataset is of type - Categorical")
    # Details about the datset - writes summary statistics and other information about the dataset
    data_info(f_name, data)
    # Mean, Median and Mode - writes the mean, median and mode for each column of the dataset
    mean_median_mode(f_name, data, columns)
    # Correlation - writes the correlation between variables
    f_name.writelines("\n\nCorrelation:\n")
    f_name.writelines("\nPearson Correlation test:")
    correlations(data, 'pearson', columns, f_name)

    f_name.writelines("\n\nSpearman's rank Correlation test:")
    correlations(data, 'spearman', columns, f_name)

    f_name.writelines("\n\nKendall's rank Correlation test:")
    correlations(data, 'kendall', columns, f_name)

    # Normality Tests -  checks for normality of the data set provided by the user
    normality(f_name, data, target, columns)


def data_info(f_name, data):
    """ FUNCTION TO DISPLAY INFORMATION ABOUT DATASET """
    f_name.writelines("\n\nDATA INFORMATION\n\n")
    # number of null values per column
    f_name.writelines("\n\nNo. of nulls in the columns:\n")
    f_name.write(str(data.isnull().sum()))
    # Information about the data:
    f_name.writelines("\nInformation about the data:")
    f_name.writelines("\n\nType of the data: " + str(type(data)))
    f_name.writelines("\n\nSummary statistics of the data\n\n")
    f_name.writelines(str(data.describe()))
    f_name.writelines("\n-----------------------------------------"
                      "-------------------------------------------"
                      "---------------------------------------------------")


def mean_median_mode(f_name, data, columns):
    """ FUNCTION TO FIND MEAN, MEDIAN, MODE OF EVERY COLUMN """
    # Mean, median and mode of each column:
    f_name.writelines("\n\nMEAN, MEDIAN AND MODE:")
    for col in columns:
        f_name.writelines("\n" + col)
        f_name.writelines("\nMean= " + str(data[col].mean()))
        f_name.writelines("     Median= " + str(data[col].median()))
        f_name.writelines("     Mode= " + str(mode) for mode in data[col].mode())
    f_name.writelines("\n-------------------------------------------------------"
                      "---------------------------------------------------------"
                      "-----------------------")


def value_counts(f_name, data, target):
    """ FUNCTION TO CALCULATE VALUE COUNTS OF CATEGORICAL COLUMNS """
    # To view summary aggregates
    f_name.writelines("\n\nVALUE COUNTS:\n\n")
    data_f = pd.DataFrame(list(zip(data[target].value_counts().index, data[target].value_counts())),
                          columns=['Column', 'counts'])
    f_name.write(tabulate(data_f, tablefmt="grid", headers="keys", showindex=False))
    f_name.writelines("\n--------------------------------------------"
                      "----------------------------------------------"
                      "---------------------------------------------")


def normality(f_name, data, target, columns):
    """ FUNCTION TO TEST NORMALITY OF THE DATASET """
    # Normality Test
    f_name.writelines("\n\nNormality Tests:")
    # Shapiro-Wilk test
    shapiro_wilk_test(f_name, data, target, columns)
    # D'Agostino's K^2 Test
    agostino(f_name, data, target, columns)
    # Anderson-Darling Test
    anderson_darling_test(f_name, data, target, columns)


def shapiro_wilk_test(f_name, data, target, columns):
    """ Shapiro Wilk Test """
    f_name.writelines("\nShapiro-Wilk test - Gaussian distribution test\n")
    f_name.writelines("Tests whether a data sample has a Gaussian distribution.\n")
    f_name.writelines("Hypothesis: the sample has a Gaussian distribution\n")
    temp_list = []
    for col in columns:
        if col == target:
            continue
        stat, prob = shapiro(data[col])
        if prob > 0.05:
            result = "Accepted"
        else:
            result = "Rejected"
        temp_list.append([col, stat, prob, result])
    data_f = pd.DataFrame(temp_list, columns=["Column", "Test Statistics", "p-Value",
                                              "Null Hypothesis"])
    f_name.write(tabulate(data_f, tablefmt="grid", headers="keys", showindex=False))
    f_name.writelines(
        "\n---------------------------------------------------------"
        "-----------------------------------------------------------"
        "-------------------")


def agostino(f_name, data, target, columns):
    """ agostino k^2 test """
    f_name.writelines("\n\nD'Agostino's K^2 Test - Gaussian distribution test\n")
    f_name.writelines("Tests whether a data sample has a Gaussian distribution.\n")
    f_name.writelines("Hypothesis: the sample has a Gaussian distribution\n")
    temp_list = []
    for col in columns:
        if col == target:
            continue
        stat, prob = normaltest(data[col])
        if prob > 0.05:
            result = "Accepted"
        else:
            result = "Rejected"
        temp_list.append([col, stat, prob, result])
    data_f = pd.DataFrame(temp_list, columns=["Column", "Test Statistics", "p-Value",
                                              "Null Hypothesis"])
    f_name.write(tabulate(data_f, tablefmt="grid", headers="keys", showindex=False))
    f_name.writelines(
        "\n--------------------------------------------------"
        "----------------------------------------------------"
        "---------------------------------")


def anderson_darling_test(f_name, data, target, columns):
    """ anderson darling test """
    f_name.writelines("\n\nAnderson-Darling Test - Gaussian distribution test\n")
    f_name.writelines("Tests whether a data sample has a Gaussian distribution.\n")
    f_name.writelines("Hypothesis: the sample has a Gaussian distribution\n")
    for col in columns:
        if col == target:
            continue
        result = anderson(data[col])
        f_name.writelines('\n' + col + ':\nStatistic: ' + str(result.statistic) + '\n')
        for j in range(len(result.critical_values)):
            sig_lev, critical_val = result.significance_level[j], result.critical_values[j]
            if result.statistic < result.critical_values[j]:
                f_name.writelines(str(sig_lev) + ':' + str(critical_val) +
                                  ' Null Hypothesis - Accepted\n')
            else:
                f_name.writelines(str(sig_lev) + ':' + str(critical_val) +
                                  ' Null Hypothesis - Rejected\n')

    f_name.writelines(
        "\n---------------------------------------------------"
        "-----------------------------------------------------"
        "-------------------------------")


def analysis_interaction(path, target):
    """ Interactive function """
    f_name = open("Analysis.txt", "w")
    data = pd.read_csv(path, sep=',', header=0)
    columns = list(data.columns)
    flag = commonFunctions.targetCheck(target, columns)
    if flag != 1:
        return str(flag)
    analysis(f_name, data, target, columns)
    f_name.close()
    return "Analysis.txt"
