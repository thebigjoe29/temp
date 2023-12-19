from flask import Flask, render_template,request,jsonify
import module
from module import check_password, update_data

app = Flask(__name__)




@app.route('/login', methods=['POST'])
def user_login():
    if request.headers['Content-Type'] == 'application/json':
        creds = request.get_json()
        email = creds.get('email', '')
        password = creds.get('password', '')
        
        result = check_password(email, password) 
        return result




@app.route('/signup', methods=['POST'])
def user_signup():
    details=request.get_json()
    email=details.get('email', '')
    query = {"Email": email}
    check_email = collection.find_one(query)
    if(check_email):
        return jsonify({'message': 'Email already exists'})
    password=details.get('password','')
    password_repeat=details.get('password_repeat','')
    if(password!=password_repeat):
        return jsonify({'message': 'Passwords do not match'})
    password=hash_password(password)
    name=details.get('name','')
    profession=details.get('profession','')
    year=details.get('year','')

    #what does the user want to do?
    #options- research, projects
    interest=details.get('interest','')
    collaboration=details.get('collaboration','')
    topic=details.get('topic','')
    skills=details.get('skills','')
    experience=details.get('experience','')
    dict={"Name":name,"Email":email,"profession":profession,"Year":year,"interest":interest,"collaboration":collaboration,"Topic":topic,"Skills":skills,"experience":experience,"password":password}
    x = collection.insert_one(dict)
    update_data()
    return jsonify({'message': 'Profile created successfully!'})
    
 
   
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=1005)