from flask import Flask, render_template,request,jsonify
from module import *
from swipe import *

app = Flask(__name__)



#To autnethicate and signin the user
@app.route('/login', methods=['POST'])
def user_login():
    if request.headers['Content-Type'] == 'application/json':
        creds = request.get_json()
        email = creds.get('email', '')
        password = creds.get('password', '')
        
        result = check_password(email, password) 
        return result



#To create prpfile based on form data
@app.route('/signup', methods=['POST'])
def user_signup():
    details=request.get_json()
    email=details.get('email', '')
    query = {"Email": email}
    check_email = collection.find_one(query)
    if(check_email):
        return jsonify({'signup': 'exists'})
    password=details.get('password','')
    password_repeat=details.get('password_repeat','')
    if(password!=password_repeat):
        return jsonify({'signup': 'mismatch'})
    password=hash_password(password)
    name=details.get('name','')
    profession=details.get('profession','')
    year=details.get('year','')
    interest=details.get('interest','')
    collaboration=details.get('collaboration','')
    topic=details.get('topic','')
    skills=details.get('skills','')
    experience=details.get('experience','')
    dict={"Name":name,"Email":email,"profession":profession,"Year":year,"interest":interest,"collaboration":collaboration,"Topic":topic,"Skills":skills,"experience":experience,"password":password}
    x = collection.insert_one(dict)
    update_data()
    return jsonify({'signup': 'success'})



#To get data using email as argument
@app.route('/get_data', methods=['POST'])
def get_data():
    try:
        data = request.get_json()
        email = data['email']
        
        result = collection.find_one({'Email': email}, {'_id': 0, 'password': 0})

        if result:
            return jsonify(result)
        else:
            return jsonify({'data': 'Data not found for the given email'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400 



#To get recommendations
@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    try:
        data = request.get_json()
        email = data.get('email')

        if email:
            final_recommendation = profile_recommender(email)
            final_recommendation = final_recommendation.loc[final_recommendation['email'] != email, ['email']]
            return jsonify(final_recommendation.to_dict(orient='records'))
        else:
            return jsonify({'error': 'Email not provided in the request'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400 
    
    
#To get swipe data
@app.route('/swipe', methods=['POST'])
def swipe():
    data = request.get_json()
    user1 = data.get('user1')
    user2 = data.get('user2')
    status1 = data.get('status1')
    status2 = data.get('status2')
    
    existing_document = swipe_collection.find_one({'user1': user1, 'user2': user2})

    if existing_document:
        
        swipe_collection.update_one(
            {'user1': user1, 'user2': user2},
            {'$set': {'status1': status1, 'status2': status2}}
        )
        message = 'Swipe updated successfully'
    else:
        
        document = {'user1': user1, 'user2': user2, 'status1': status1, 'status2': status2}
        swipe_collection.insert_one(document)
        message = 'Swipe added successfully'

    return jsonify({'message': message})

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=10000)