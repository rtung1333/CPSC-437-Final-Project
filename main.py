import sqlite3
import sys
import computations
import config

def initdb():
	con = sqlite3.connect('db/restaurantPredictions.db')
	cur = con.cursor()
	return con

def sign_in(cur):
	print('Welcome! (A) Sign In (B) Register')
	try:
		next = raw_input()
	except EOFError:
		exit()

	if (next == 'A'):
		'''
		Grab the username from input
		'''
		print('What is your name?')
		try:
			username = raw_input()
		except EOFError:
			exit()
		print('Signing in as ' + username)

		cur.execute('SELECT * FROM Users WHERE Name=?', [username])
		me = cur.fetchall()
		if (len(me) == 0):
			print('User does not exist')
			return -1
		return me[0]

		print('UserId: {}').format(UserId)

def finished():
	print('Eat up!')
	exit()

def main():
	con = initdb()
	cur = con.cursor()

	result = sign_in(cur)
	while (result == -1):
		result = sign_in(cur)

	for attr in result:
		print(attr)

	UserId = result[0]
	Name = result[1]
	Age = result[2]
	Gender = result[3]

	# computations.compute_recs(username)
	actions(UserId, Name, Age, Gender, con, cur)

def output(places):
	i = 1
	for place in places:
		if place:
			print('{}.' + place[1] + '\n\t Price: {}\n\t Rating: {}').format(i, place[2], place[5])
			i += 1

def actions(userid, name, age, gender, con, cur):
	while(True):
		try:
			print('What now?\n\t(A) Recommend restaurants\n\t(B) List my favorites\n\t(C) List my friends\n\t(D) Add a favorite\n\t(E) Add a friend\n\t(F) Done!')
			action = raw_input()
			if (action == 'A'):
				print('Check out these places:')
				'''Get restaurant recommendation based on favorites'''
				recs = get_recommendations(userid, con, cur)
				output(recs)

			elif (action == 'B'):
				print('Here are you favorites:')
				'''Query DB for favorites based on username'''
				favorites = get_favorites(userid, con, cur)
				output(favorites)

			elif (action == 'C'):
				print('Here are you friends:')
				'''Query DB for friends based on username'''
				friends = get_friends(userid, con, cur)
				i = 1
				for friend in friends:
					print('{}. ' + friend).format(i)
					i += 1

			elif (action == 'D'):
				print('Which restaurant would you like to favorite?')
				try:
					rest_name = raw_input()
				except EOFError:
					finished()

				'''Add restaurant as favorite for username'''
				add_favorite(userid, rest_name)

			elif (action == 'E'):
				print('Who would you like to friend?')
				'''Add friend as friend of user'''
				try:
					friend_name = raw_input()
				except EOFError:
					finished()
				add_friend(userid, friend_name)

			elif (action == 'F'):
				finished()

			else:
				print('Please choose A, B, C, D, E, or F.')
		except EOFError:
			finished()


def get_recommendations(userid, con, cur, which=0):
	if which == 0:
		personal = True
		ageGender = False
		friends = False
	elif which == 1:
		personal = False
		ageGender = True
		friends = False
	elif which == 2:
		personal = False
		ageGender = False
		friends = True
	recs = computations.compute_personal_recs(userid, 5, con, cur, personal, ageGender, friends)[which]
	return recs

def get_favorites(userid, con, cur):
	cur.execute("SELECT * FROM Restaurants, Favorites WHERE Restaurants.RestaurantId=Favorites.RestaurantId and UserId=?", [userid])
	fav = cur.fetchall()
	return fav;

def add_favorite(userid, con, cur, rest_name):
	# rows = cur.execute("SELECT RestaurantId FROM Restaurants WHERE Name=?", rest_name)
	# if (len(rows) == 0):
	# 	print("Uh oh, we've never heard of " + rest_name)
	# 	return
	# cur.execute("INSERT INTO Favorites(UserId, RestaurantId) VALUES (?, ?)", username, rows[0][0])
	print(rest_name + " favorited!")

def add_friend(userid, con, cur, friend):
	# rows = cur.execute("SELECT * FROM Users WHERE UserId=?", friend)
	# if (len(rows) == 0):
	# 	print("Uh oh, we've never heard of " + rest_name)
	# 	return
	# cur.execute("INSERT INTO Friends(UserId1, UserId2) VALUES (?, ?)", username, friend)
	print(friend + " added as friend!")

def get_friends(userid, con, cur):
	friends = list()
	others = cur.execute("SELECT Name FROM Users, Friends WHERE UserId1=? and UserId2=UserId", [userid])
	for people in others:
		friends.append(people[0])
	return friends

if __name__ == "__main__":
	main()
