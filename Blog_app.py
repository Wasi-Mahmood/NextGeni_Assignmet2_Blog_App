

from flask import Flask, request , jsonify, make_response

import jwt
from datetime import datetime, timedelta
from functools import wraps
from models import Users,Blogs,Comments
from validate_email_address import validate_email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'forurosurwasobaiii6-4--1'

users = Users()
blogs =Blogs()
comments =Comments()

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert': 'Token is Missing' })
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'],'HS256')
            # print(payload)
            expiration = payload['expiration']
            expiration = datetime.strptime(expiration, '%Y-%m-%d %H:%M:%S.%f')
            current_time = datetime.utcnow()
            # print(expiration, " < ", current_time)

            if expiration < current_time:
                return jsonify({'Alert': 'Expired token login again'})
        except jwt.InvalidTokenError:
            return jsonify({'Alert': 'Invalid token'})
        return func(*args, **kwargs)
    return decorated


@app.route('/register')
def register_user():
    email = request.args.get('email')
    
   
    if not validate_email(email):
        return "Invalid email address"
    
    if not users.check_for_email_duplicates(email):
        new_user = users.register(email, request.args.get('password'))
        return new_user
    else:
        return "Email address already exists"
    
    
#home
@app.route('/')
@token_required
def home():
   
    email = request.args.get('email')
    all_blogs = blogs.get_all_blogs(email)
    if all_blogs:
        return jsonify(all_blogs)
    else:
        return "Failed To Retrieve Blogs" 
    


#login
@app.route('/login', methods =['POST'])
def login():
    
    if users.user_login(request.args.get('email'), request.args.get('password')):
        token = jwt.encode({
            'user': request.args.get('email'),
            'expiration': str(datetime.utcnow() + timedelta(seconds = 5000))
        },app.config['SECRET_KEY'])
        print(token)
        return jsonify({'token': token})
    else:
        return make_response('Unable to verify, email or password might be incorrect', 403, {'WWW- Authenticate': 'Basic realm: "Authentication Failed!"'})




# #Authenticated
# @app.route('/auth')
# @token_required
# def auth(): 
#     return jsonify({'welcome':'JWT is Verified, Welcomee aboard !'})


@app.route('/add_blog', methods =["POST"])
@token_required
def add_blog():
    
    #post_id = request.args.get('post_id')
    email = request.args.get('email')
    blog_data =request.args.get('blog_data')
    new_blog_id =blogs.create_blog(email,blog_data)
    if new_blog_id:
        return(jsonify({"blog_id": new_blog_id}))
    else:
        return "Blog can't be added t this moment"
    

@app.route('/blog/add_comment', methods=['POST'])
@token_required
def add_comment():
    
    blog_id = request.args.get('blog_id')
    comment_data = request.args.get('comment_data')
    new_comment = comments.create_comment(blog_id,comment_data)
    if new_comment:
        return (jsonify({"comment_id": new_comment[0], "comment_data": new_comment[1]}))
    else:
        return "Comment can't be added"
        

        
if __name__ == "__main__":
    app.run(debug= True )
    