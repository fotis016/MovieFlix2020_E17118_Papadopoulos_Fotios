from flask import Flask, render_template, url_for, request, session, redirect, jsonify, json
from pymongo import MongoClient
import bcrypt
import os 

app = Flask(__name__)

mongodb_hostname = os.getenv("MONGO_HOSTNAME","localhost")
client = MongoClient('mongodb://'+mongodb_hostname+':27017/')
db = client['database']
users = db['users']
movies = db['movies']

@app.route('/')
def index():
	if 'email' in session:
		if session.get('category') == '1':
			return render_template('mainAdmin.html')
		else:
			return render_template('mainUser.html')

	return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    login_user = users.find_one({'email' : request.form['email']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['email'] = request.form['email']
            session['category'] = login_user['category']
            session['logged_in'] = True
            return redirect(url_for('index'))

    return 'Invalid username/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
 if session.get('logged_in') == True:
  return 'You have already logged in!'
 elif request.method == 'POST':
  existing_user = users.find_one({'email' : request.form['email']})

  if existing_user is None:
   hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
   users.insert_one({'name' : request.form['username'], 'email' : request.form['email'], 'password' : hashpass, 'category' : request.form['category'], 'comments' : [], 'rating' :[]} )
   session['email'] = request.form['email']
   session['category'] = request.form['category']
   session['logged_in'] = True
   return redirect(url_for('index'))
        
  return 'A user has already registered using this email!'

 return render_template('register.html')
 
@app.route('/mainadmin', methods=['GET'])
def mainadmin():
	if(session.get('logged_in') == True and session.get('category') == '1'):
		return render_template('mainpageAdmin.html')
		
	else:  
		return 'Please login first.'

@app.route('/mainuser', methods=['GET'])
def mainuser():
	if(session.get('logged_in') == True and session.get('category') == '0'):
		return render_template('mainpageUser.html')
		
	else:  
		return 'Please login first.'


		
@app.route('/searchmv', methods=['GET', 'POST'])		
def searchmv():
	if session.get('logged_in') == True:
		if request.method == "POST":
		 select = request.form.get('selection')
		 
		 if select == "title":
		 	movie_search = movies.find({'title': {'$regex':request.form['data']}})
		 	result = 'List of found movies:<br/>'
		 	for document in movie_search:
		 		result = result + 'Title: ' + str(document['title']) + ' Year: ' + str(document['year']) + '<br/>'
		 	return result
		 elif select == "date":
		 	movie_search = movies.find({'year': {'$regex':request.form['data']}})
		 	result = 'List of found movies:<br/>'
		 	for document in movie_search:
		 		result = result + 'Title: ' + str(document['title']) + ' Year: ' + str(document['year']) + '<br/>'
		 	return result	 	
		 elif select == "actors":
		 	movie_search = movies.find({'actors': {'$regex':request.form['data']}})
		 	result = 'List of found movies:<br/>'
		 	for document in movie_search:
		 		result = result + 'Title: ' + str(document['title']) + ' Year: ' + str(document['year']) + '<br/>'
		 	return result
	else:
	 return 'Plese login first.'		 
	return render_template('searchmovie.html')
	
	
@app.route('/displmv', methods=['GET'])
def displmv():
	if session.get('logged_in') == True:
		result = 'Printing details for all movies:<br/><br/>'
		if movies == None:
			return 'Movie list is empty.'
		else:
			movie_search = movies.find()
			for document in movie_search:
				result = result + 'Title: ' + str(document['title']) + ' Year: ' + str(document['year']) + '<br/>' + ' Description: ' + str(document['description']) + '<br/>' + ' Actors: ' +str(document['actors']) + '<br/>'  + '<br/>'  
		return result 
	else:
		return 'Please login first.'
	
@app.route('/showcomms', methods=['GET', 'POST'])
def showcomms():
	if session.get('logged_in') == True:
		if request.method == "POST":
			movie_search = movies.find({'title': {'$regex':request.form['data']}})
			if movies == None:
				return 'Movie list is empty.'
			else:
				result = 'Printing details for all comments:<br/><br/>'	
				for document in movie_search:
					result = result + 'Title: ' + str(document['title']) + '<br/>'  + ' Comments: ' + str(document['comments']) + '<br/>' + '<br/>'
				return result 
	else:
		return 'Please login first.'
	return render_template('searchcomments.html')
	

@app.route('/rate', methods=['GET', 'POST'])
def rate():
	if session.get('logged_in') == True:
		if request.method == "POST":
			if movies == None:
				return 'Movie list is empty.'
			else:
				movie_search = movies.find_one({'title': request.form['title']})
				if movie_search:
					check = movies.find_one({'title': request.form['title'], 'rating': { '$elemMatch': {'email': session['email']}}})
					if check:
						return 'You have already left a rating for this specific movie.'
					else:
						movies.update( { 'title': request.form['title']}, { '$push':{'rating': {'email': session['email'], 'rating': request.form['rating']}}})
						users.update({'email': session['email']}, { '$push':{'rating': {'title': request.form['title'], 'rating': request.form['rating']}}})
						return 'Rating has been submitted.'
				else:
					return 'Movie not found'		
	else:
		return 'Please login first.'
	return render_template('addrate.html')
												
@app.route('/removerate', methods=['GET', 'POST'])
def removerate():
	if session.get('logged_in') == True:	
		if request.method == "POST":
			if movies == None:
				return 'Movie list is empty.'
			else:
				movie_search = movies.find_one({'title': request.form['title']})
				if movie_search:
					check = movies.find_one({'title': request.form['title'], 'rating': { '$elemMatch': {'email': session['email']}}})
					if check:
						movies.update( { 'title': request.form['title']}, { '$pull':{'rating': {'email': session['email']}}})
						users.update({'email': session['email']}, { '$pull':{'rating': {'title': request.form['title']}}})
						return 'Rating was successfully removed.'
					else:
						return	'You have not rated this movie.'
				else:
					return 'Movie not found'
	else:
		return 'Please login first.'	
	return render_template('removerate.html')
	
@app.route('/inscomm', methods=['GET', 'POST'])
def inscomm():
	if session.get('logged_in') == True:	
		if request.method == "POST":
			if movies == None:
				return 'Movie list is empty.'
			else:
				movie_search = movies.find_one({'title': request.form['title']})
				if movie_search:
					movies.update( { 'title': request.form['title']}, { '$push':{'comments': {'email': session['email'], 'comment': request.form['comment']}}})
					users.update({'email': session['email']}, { '$push':{'comments': {'title': request.form['title'], 'comment': request.form['comment']}}})
					return 'Comment has been submitted.'
				else:
					return 'Movie not found'
	else:
		return 'Please login first.'
	return render_template('addcomment.html')
	
@app.route('/showallcomms', methods=['GET'])
def showallcomms():
	if session.get('logged_in') == True:
		result = 'Printing all comments for all movies:<br/><br/>'
		movie_search = users.find({'email': session['email']})
		for document in movie_search:
			result = result + str(document['comments']) + '<br/>' + '<br/>'
		return result
	else:
		return 'Please login first.'
		
@app.route('/showallrate', methods=['GET'])
def showallrate():
	if session.get('logged_in') == True:
		result = 'Printing all ratings for all movies:<br/><br/>'
		movie_search = users.find({'email': session['email']})
		for document in movie_search:
			result = result + str(document['rating']) + '<br/>' + '<br/>'
		return result
	else:
		return 'Please login first.'
		
@app.route('/delcomm', methods=['GET', 'POST'])
def delcomm():
	if session.get('logged_in') == True:
		if request.method == "POST":
			check = users.find_one({'email': session['email'], 'comments':{ '$elemMatch': {'title': request.form['title'], 'comment': request.form['comment']}}})
			if check:
				users.update({'email': session['email']}, { '$pull':{'comments':{'title': request.form['title'], 'comment': request.form['comment']}}}) 
				movies.update({'title': request.form['title']}, { '$pull':{'comments': {'email': session['email'], 'comment': request.form['comment']}}})
				return 'Comment successfully deleted'
			else:
				return 'Movie not found, you have not commented on that specific movie or you did not enter your comment correctly.'
	else:
		return 'Please login first.'
	return render_template('deletecomment.html')
	

@app.route('/delacc', methods=['GET', 'POST'])
def delacc():
	if session.get('logged_in') == True:
		if request.method == "POST":
			if request.form['confirm'] == 'Yes':
				users.remove({'email': session['email']})
				session['logged_in'] = False
				session['email'] = ''
				return 'You have successfully deleted your account'
			else:
				return 'Operation was cancelled'
	else:
		return 'Please login first.'
	return render_template('deleteaccount.html')
		
@app.route('/insmov', methods=['GET', 'POST'])
def insmov():
	if session.get('logged_in') == True:	
		if session.get('category') == '0':
			return 'You do not have admin privilidges'
		
		elif session.get('category') == '1':
			if request.method == "POST":
				existing_movie = movies.find_one({'title': request.form['title']})
				if(existing_movie):
					return 'Movie with entered title already exists in the database.'
				else:
					if(request.form['title'] == '' or request.form['actors']==''):
						return "You haven't entered movie title and/or any actors, please try again."
					else:	
						movies.insert_one({'title': request.form['title'], 'year': request.form['year'], 'description': request.form['description'], 'actors': request.form['actors'], 'rating': [], 'comments':[]})	
						return 'Movie successfully added ' 
	else:
		return 'Please login as an admin first.'
	return render_template('addmovie.html')
			
@app.route('/delmov', methods=['GET', 'POST'])
def delmov():
	if session.get('logged_in') == True:	
		if session.get('category') == '0':
			return 'You do not have admin privilidges'
		
		elif session.get('category') == '1':
			if request.method == "POST":
				search_movie = movies.find_one({'title': request.form['title']})
				if search_movie:
					movies.remove({'title': request.form['title']})
					return 'Movie has been successfully removed from the database'
				else:
					return 'Movie was not found'
	else:
		return 'Please login as an admin first.'	
	return render_template('deletemovie.html')		

@app.route('/updmov', methods=['GET', 'POST'])
def updmov():
	if session.get('logged_in') == True:	
		if session.get('category') == '0':
			return 'You do not have admin privilidges'
		
		elif session.get('category') == '1':
			if request.method == "POST":
				search_movie = movies.find_one({'title': request.form['title']})
				if search_movie:
					select = request.form.get('selection')
					if select == 'newtitle':
						movies.update( { 'title': request.form['title']}, {'$set' :{ 'title': request.form['data']}})
						return 'New movie title was set.'
					elif select == 'date'	:				
						movies.update( { 'title': request.form['title']}, {'$set' :{ 'year': request.form['data']}})
						return 'Year of release was updated.'
					elif select == 'actors':					
						movies.update( { 'title': request.form['title']}, {'$set' :{ 'actors': request.form['data']}})
						return 'Actors section has been edited.'
					else:
						movies.update( { 'title': request.form['title']}, {'$set' :{ 'description': request.form['data']}})
						return 'Plot section has been edited.'
				else:
					return 'Movie not found'
	else:
		return 'Please login as an admin first.'	
	return render_template('updatemovie.html')


@app.route('/delothcomm', methods=['GET', 'POST'])
def delothcomm():
	if session.get('logged_in') == True:	
		if session.get('category') == '0':
			return 'You do not have admin privilidges'
		
		elif session.get('category') == '1':
			if request.method == "POST":
				search_movie = movies.find_one({'title': request.form['title']})
				if search_movie:
					user = request.form['email']
					comment_exists = movies.find_one({'title': request.form['title'], 'comments':{ '$elemMatch': {'email': request.form['email'], 'comment': request.form['comment']}}})
					if comment_exists:
						movies.update({'title': request.form['title']}, { '$pull':{'comments': {'email': request.form['email'], 'comment': request.form['comment']}}})
						return 'Comment successfully deleted'	
					else:
						return 'User has not left any comments for this movie or entered comment is not correct'
				else:
					return 'Movie does not exist in the database'
	else:
		return 'Please login as an admin first.'	
	return render_template('deletecommentotherusers.html')				

@app.route('/upgusr', methods=['GET', 'POST'])
def upgusr():
	if session.get('logged_in') == True:	
		if session.get('category') == '0':
			return 'You do not have admin privilidges'
		
		elif session.get('category') == '1':
			if request.method == "POST":
				user_search = users.find_one({'email': request.form['email']})
				if user_search:
					if users.find_one({'email': request.form['email'], 'category' : '0'}):
						users.update({'email': request.form['email']}, {'$set' :{ 'category': '1'}})
						return 'Selected user was successfully promoted to admin'
					else:
						return 'Selected user already has admin privilidges'
				else:
					return 'User not found'
	else:
		return 'Please login as an admin first.'	
	return render_template('upgradeuser.html')				

@app.route('/delothacc', methods=['GET', 'POST'])
def delothacc():
	if session.get('logged_in') == True:	
		if session.get('category') == '0':
			return 'You do not have admin privilidges'
		
		elif session.get('category') == '1':
			if request.method == "POST":
				user_search = users.find_one({'email': request.form['email']})
				if user_search:
					if users.find_one({'email': request.form['email'], 'category' : '0'}):
						users.remove({'email': request.form['email']})
						return 'Selected user was successfully deleted'
					else:
						return 'Selected user has admin privilidges and cannot be deleted'
				else:
					return 'User not found'
	else:
		return 'Please login as an admin first.'	
	return render_template('deleteotheruser.html')	


				
if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True, host='0.0.0.0', port=5000)
