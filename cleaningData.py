import pandas as pd
import numpy as np
import sklearn
import matplotlib.pyplot as plt

#Cleaning data
def cleanEthnicity(df):
    df.replace(r'AIAN','American Indian or Alaska Native',inplace=True, regex=True)
    df.replace(r'AfricanAm','Black or African American',inplace=True, regex=True)
    df.replace(r'Latino','Hispanic or Latino',inplace=True, regex=True)
    df.replace(r'NHOPI','Native Hawaiian or Other Pacific Islander',inplace=True, regex=True)
    return df

def p_cleanData(df, removeColList):
    # remove discovered useless columns
    df.drop(removeColList, axis=1, inplace=True)
    
    # removing single value columns
    columnNames = list(df.columns.values)
    for i in columnNames:
        col_contains = df[i].unique()
        if len(col_contains) == 1:
            df.drop([i], axis=1, inplace=True)  
    
    # removing unnecesary rows
    df.dropna(subset=['Poverty'], inplace=True)  #where Poverty= NaN, rest of the cols are empty
    
    # fixing abbreviation 
    df = cleanEthnicity(df)
    return df

def p_extractUsefulInfo(name, df, removeColList):
    print("Started {} Data with shape = {}".format(name, df.shape))
    df = p_cleanData(df, removeColList)
    print("After cleaning, NEW {} data shape = {}\n\n".format(name, df.shape))
    print(list(df.columns.values))
    return df


def u_cleanData(df, removeColList):
    # remove discovered useless columns
    df.drop(removeColList, axis=1, inplace=True)
    
    # removing single value columns
    columnNames = list(df.columns.values)
    for i in columnNames:
        col_contains = df[i].unique()
        if len(col_contains) == 1:
            df.drop([i], axis=1, inplace=True)  
    
    # removing unnecesary rows
    df.dropna(subset=['Unemployment'], inplace=True)  
    
    # fixing abbreviation 
    df = cleanEthnicity(df)
    return df

def u_extractUsefulInfo(name, df, removeColList):
    print("Started {} Data with shape = {}".format(name, df.shape))
    df = u_cleanData(df, removeColList)
    print("After cleaning, NEW {} data shape = {}\n\n".format(name, df.shape))
    print(list(df.columns.values))
    return df
