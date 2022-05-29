#This file deals with training our K Nearest Neighbors Model

import csv
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from scipy import sparse
import pickle

#The commands below would load our pre filtered datafile to be used by the k nearest neighbor data

final_dataset = pd.read_csv(r"C:\Python\MovieRec\Recommendation\final_dataset_csv.csv")
csr_data = sparse.load_npz('C:\Python\MovieRec\Recommendation\csr_data.npz')


#The knn model is defined below. It would use the cosine distance metric to compute the distance between 2 movies. It would filter
#the 25 closest movies based on the searched movies and then return the top 10.

knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=25, n_jobs=-1)
knn.fit(csr_data)

#The pickle command would help us to save our trained model and make it easier for future use.
pickle.dump(knn, open("C:\Python\MovieRec\Recommendation\knn_model.txt", 'wb'))