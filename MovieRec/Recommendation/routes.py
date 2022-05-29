# The routes.py will handle all the different pages that the website has. It will guide the code to go to a specific
# page on certain actions. 


from sqlalchemy import true
from Recommendation import app
from flask import flash, render_template, redirect, url_for, flash
from Recommendation.model import user
from Recommendation.forms import RegisterForm, LoginForm, SearchForm
from Recommendation import db
from flask_login import login_required, login_user, logout_user
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from scipy import sparse

import csv
import numpy as np
import pandas as pd
import pickle



# Defined below is the route to the website's homepage. 
# /home and only / will lead to the same path, Home page.
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')



# Defined below is the route to the website's about section. 
# This section contains certains items that will be displayed on the website in a table format. 
@app.route('/about')
def about_page():
    return render_template('about.html')



# Defined below is the route to the registeration page. 
# The registeration page would take certain information from the user as input and hence it contains form elements.
@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()

    if form.validate_on_submit(): #This condtition will check if the user has pressed the submit button.

        user_to_create = user(username=form.username.data, 
                              email_address=form.email_address.data, 
                               password_hash=form.password1.data)  #This command will retrieve the information given by the user in the form.

        db.session.add(user_to_create) #This command would add the collected details of the user into our database.
        db.session.commit()            #This command would commit the details of the new user to our database.
         

        login_user(user_to_create)      #This command would log in the user. It will help us while navigating certain routes 
                                        #to know if the user is logged in or not


        flash(f'Account created successfully! You are now logged in as: {user_to_create.username}', category='success') 
        #The command above would flash a banner to the user stating that their account is created  and they've successfully logged in
        

        # The command below would redirect the user to the recommendation page where 
        # they can search for the movie they like and get recommendations 
        return redirect(url_for('recommender_page'))  



    if form.errors != {}:      #This condition will check if there are any errors in the data filled in the form

        #The for loop will run for the total number of errors present
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger' )
            #The above command would flash the kind of error the user has made while creating the acount
            #The errors include : 1. Invalid email ID. 2. UserName already exists 3. Password and Confirm Password do not match.


    #The command below would again render the register.html template and the user could try registering again if any error occurs.       
    return render_template('register.html', form=form) 




# Defined below is the route to the login page. 
# It contains a form as well as returning users would log in using their registered credentials.
@app.route('/login', methods=['GET','POST'])
def login_page(): 
    form = LoginForm()
    
    if form.validate_on_submit(): #This condition checks if the user has pressed the submit button

        attempted_user = user.query.filter_by(username=form.username.data).first() #This command would store the username attempted by the user
        attempted_password=form.password.data                                      # Would store the password submitted by the user
        
        try:
            if attempted_user.get_pwd() == attempted_password: #It would check if the password submitted by the user is the same as the password corresponding 
                                                           # to the username in the databae
            
                login_user(attempted_user) #It would log in the user

                flash(f'Success! You are logged in as: {attempted_user.username}', category='success') # This command would flash a banner and let the user know
                                                                                                   # they are logged in 
            
                return redirect(url_for('recommender_page'))    #It would redirect the user to the recommender page.

            else:
                flash('Username and Password do not match! Please try again!', category='danger') 
                #The above warning will be flashed if the attempted password and username do not match with the ones in the database

                return render_template('login.html', form=form)
       
        
        except:
            flash('No user found! Register instead?', category='danger')
            #The above warning will be flashed if the username mentioned by the user doesn't exist in the database

    return render_template('login.html', form=form) #This would render the login page again if there is any error in logging in the user


# Defined below is the route to logout the user
@app.route('/logout')
def logout_page():

    logout_user() #This simple command will log out the user. They would no longer be able to access the paths that require a user to be logged in


    flash("You have been logged out!", category='info' ) # This would flash an info banner letting the user know they've been logged out
    
    
    return redirect(url_for('home_page')) # This would redirect the user to the home page after logging out.



#Defined below is the route to the recommender page. The page contains a search bar for the users to search the movie.
@app.route('/recommender', methods=['GET','POST'])


@login_required  #This would check if the user is logged in. The users who aren't logged in would be redirected to the login page


def recommender_page():
    form = SearchForm()
    if form.validate_on_submit():            #This would confirm that the user has pressed on the submit button.


        searched_movie=form.movie_name.data  # The movie searched by the user would be stored in a variable for us to work upon.
        
        #The commands below would import our dataset in the .csv format and store it in variables for easy access.
        movies = pd.read_csv(r"C:\Python\MovieRec\Recommendation\movies.csv")     
        ratings = pd.read_csv(r"C:\Python\MovieRec\Recommendation\ratings.csv")


        #The command below would import the final_dataset csv and the csr_data(compressed sparse rows) that is the refined data based on the raw data.
        #It has been pregenerated by me and saved for future use using the file knn.py

        final_dataset = pd.read_csv(r"C:\Python\MovieRec\Recommendation\final_dataset_csv.csv")
        csr_data = sparse.load_npz('C:\Python\MovieRec\Recommendation\csr_data.npz')


        #The "K Nearest Neighbors" model has been trained using the data above and saved using knn.py
        #The trained model is loaded into our variable knn to avoid training it everytime and thus save time.
        knn = pickle.load(open("C:\Python\MovieRec\Recommendation\knn_model.txt", 'rb'))


        #Defined below is the actual movie recommending fuction!

        def get_movie_recommendation(movie_name):
            n_movies_to_recommend = 10         
        
            movie_list = movies[movies['title'].str.contains(movie_name)] #This will check if the movie searched by the user is present in our raw csv data.

            
            
            if len(movie_list):  # If the length of the movie_list zero = It implies that the movie searched is not in our data
                                 # If the length is non zero, the condition confirms that the movie is present and we can work ahead.


                movie_idx = movie_list.iloc[0]['movieId'] #This will retrieve the movie id of the searched movie from the csv file

                try:
                    movie_idx = final_dataset[final_dataset['movieId'] == movie_idx].index[0]
                    distances, indices = knn.kneighbors(csr_data[movie_idx], n_neighbors=n_movies_to_recommend+1)
                    #The command above would run the trained knn model on the csr_matrix data corresponding to the movie id of the
                    #movie searched by the user.


                    rec_movie_indices = sorted(list(zip(indices.squeeze().tolist(),distances.squeeze().tolist())),key=lambda x: x[1])[:0:-1]
                    #The command would store the indices and the distances to the searched movie in a sorted order.


                    recommend_frame = []
                    #We are declaring a variable that would later store the recommended movies


                    for val in rec_movie_indices:      
                        #The loop runs for all the indices of the movies stored in the rec_movie_indices

                        movie_idx = final_dataset.iloc[val[0]]['movieId']
                        idx = movies[movies['movieId'] == movie_idx].index
                        
                        #The command above would retrieve and store the recommended movie title and corresponding id

                        recommend_frame.append({'':movies.iloc[idx]['title'].values[0]})   
                        #For every iteration of the for loop, a recommended movie would be added to this list. 
 

                    df = pd.DataFrame(recommend_frame, index=range(1,n_movies_to_recommend+1))
                    #This would store the recommended movies in dataframe format. This format would be easier to return

                    return df
        
                except:
                    #This is for error handling. It would identify the edge case that the movie searched
                    #by the user is present in the raw data but due to less amount of reviews,
                    #could not be filtered into the final data
                    return "Not enough reviews"

            else:
                return "No movies found. Please check your input" 

    
        global finaldf 

        finaldf = get_movie_recommendation(searched_movie)
        #This would enter the movie searched by the user into our recommendation function.


        return redirect(url_for('results_page'))
        #This would redirect the user to the results page where the recommendations would be displayed.

    return render_template('recommender.html',form=form)
    #This would occur when the movie is not present in the dataset, or the movie has less reviews.
    #The recommender.html would be rendered again and the user would be asked to search again. 



#Defined below is the route to the final results page

@app.route('/results')
def results_page():
    
    res = finaldf #We'll store the dataframe in a variable to perform certain necessary checks ahead.


    if(isinstance(res, str)): 
        #This condition will check for the case if the final dataframe returned by the recommender page is a string.
        #If it's a string, it would imply that recommendations could not be retrieved for the searched movie.


        flash(res, category='danger')
        #This command would flash the respective statement in the res variable if the recommendations could not be produced.

        #If recommendations could not be produced, the user would be redirected to the recommender page where they'll have to search another movie.
        return redirect(url_for('recommender_page'))
        
    
    return render_template('results.html', tables=[res.to_html(classes=' table table-dark table-hover table-sm ', header="true") ]) 
    #This return function will be called when the res variable is an actual dataframe implying that the recommendations have been generated.
    #The command would then convert the dataframe to an html table and display the same on the results.html page.s