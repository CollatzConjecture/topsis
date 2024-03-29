from topsis import topsis
import pandas as pd
import numpy as np
import mcdm

from Normalization import *
from Normalized_Decision_Matrix import *
from Ideal_Solution import Ideal_Solution
from Distance_Between_Ideal_and_Alternatives import *

name= "Sample.xlsx"

Data = pd.read_excel(name)
Data.index = Data['Alternatives']
Data = Data.iloc[:, 1:]

num_criteria = Data.shape[1]
weights = [1/num_criteria] * num_criteria

PC = [1] * num_criteria

def TOPSIS(Decision_Matrix, Weights, Attribute_Type, Normalization_Method = Linear_sum):
    
    """
    TOPSIS implementation based on this publication:
        * C.-L. Hwang and K. Yoon, Multiple attribute decision making,
        ser. Lecture Notes in Economics and Mathematical Systems.
        Springer-Verlag Berlin Heidelberg, 1981, vol. 186,ethod = Normalization_Method
        ISBN: 9783540105589.
        Book Link: https://www.springer.com/gp/book/9783540105589
    """

    if len(Weights) != Decision_Matrix.shape[1]:
        raise ValueError("The number of weights must match the number of criteria.")
    if len(Attribute_Type) != Decision_Matrix.shape[1]:
        raise ValueError("The number of attribute types must match the number of criteria.")
    
    Normalizaed_Decision_matrix = Normalize_Decision_Matrix(Decision_Matrix = Decision_Matrix,
                                                            Attribute_Type=Attribute_Type,
                                                            Normal_Method=Normalization_Method)
     
    Weighted_Normalizaed_Decision_matrix = Weight_Prod(Decision_Matrix = Normalizaed_Decision_matrix, weights = Weights)
     
    Ideal_Solutions = Ideal_Solution(Weighted_Normalizaed_Decision_matrix, Attribute_Type)
    a = Euclidean_Distance(Ideal_Solutions, Weighted_Normalizaed_Decision_matrix, Attribute_Type)
    return a
 
Output = TOPSIS(Data, weights, PC,Normalization_Method = Linear_Max_Min)
#q.to_excel(path + "MyTopsis3.xlsx")

Scores=pd.DataFrame(Output[1])
Normalized_Weighted_Decision_Matrix = Output[0]
df=pd.concat([Normalized_Weighted_Decision_Matrix, Scores], axis=1)
