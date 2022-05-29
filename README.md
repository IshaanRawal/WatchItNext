Python library Requirements to run Watch It Next

* sqlalchemy
* flask
* scipy.sparse
* sklearn.neighbors
* scipy
* csv
* numpy
* pandas
* pickle
* bcrypt
* flask_login & LoginManager
* pickle
* flask_wtf
* wtforms
* xml.dom

---------------------------------------------------------------

Important notes to run the website offline

* After downloading the files:
movies.csv, ratings.csv, final_dataset.csv, csr_data.npz, knn_model.txt included in this GitHub Repository, change the file path used in the code as per the path that these files are saved in your device. .........\MovieRec\Recommendation\* File_name *.
* This change has to be made in routes.py(ln 150,151,157,158,163) and knn.py(ln 13,14,20,24) 

----------------------------------------------------------------

To run the website, use run.py present in the MovieRec folder. Once run.py is successfully executed, visit http://127.0.0.1:5000/ in your local browser to access the website.

-----------------------------------------------------------------

Searching Movies Efficiently on Watch It Next

* The movies database contains a variety of Hollywood Movies. You can type in the movie name directly with the correct 
capitalization and get the results if the movie is present in the database and has enough reviews.

* You can also access the movies.csv file provided in the GitHub Repo to get a better idea of the movies in the database.

* YOU NEED TO ONLY SEARCH THE MOVIE NAME AS IT IS METIONED IN THE CSV FILE

For eg. Toy Story (1995) is present in the movies.csv, You could get movie recommendations by searching Toy Story on the recommender page.
