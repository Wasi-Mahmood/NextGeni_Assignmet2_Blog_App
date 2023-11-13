import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import DictCursor
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


load_dotenv()

conn = psycopg2.connect(database = "Flask-app-blog-db", host="localhost", user="postgres", password="123", port ="5432")
conn.autocommit = True
cursor = conn.cursor(cursor_factory=DictCursor)

class Blogs:
    
    def __init__(self):
        return

    def get_all_blogs(self, email):
        """Get all blogs"""
        cursor.execute("SELECT * FROM blogs WHERE email =%s",(email,))
        all_blogs = cursor.fetchall()
        return {blog_id: (blog_data) for email,blog_id ,blog_data, in all_blogs}

    def get_blog_by_id(self, blog_id):
        """Get a book by id"""
        cursor.execute("SELECT * FROM blogs WHERE blog_id = %s", (blog_id,))
        blog = cursor.fetchone()[2]
        if not blog:
            return "Failed to Retreive the Blog"
        
        return blog

    
    def create_blog(self,email, blog_data):
        blog_id = (f"{email}-blog-{str(datetime.utcnow())}")
        cursor.execute("""
                       INSERT INTO blogs (email,blog_id,blog_data)
                       VALUES(%s,%s,%s)
                       RETURNING blog_id
                       """,
                       (email, blog_id, blog_data)
                       )
        
        new_blog_id = cursor.fetchone()[0]
        return new_blog_id
        
    
    


class Comments:
    
    def __init__(self):
         return
    
    def create_comment(self,blog_id,comment_data):
        comment_id = (f"{blog_id}--comment-{str(datetime.utcnow())}")
        cursor.execute("""
                    INSERT INTO comments (blog_id,comment_id,comment_data)
                    VALUES(%s,%s,%s)
                    RETURNING comment_id, comment_data
                    """,
                    (blog_id,comment_id, comment_data)
                    )
    
        new_comment_id = cursor.fetchone()
        return new_comment_id
     
    

class Users:
    def __init__(self):
        return

    def register(self, email, password):
        cursor = conn.cursor(cursor_factory=DictCursor)
        cursor.execute(
            """
            INSERT INTO users (email,password)
            VALUES (%s, %s)
            RETURNING email
            """,
            (email,self.encrypt_password(password))
        )
        new_user = cursor.fetchone()[0]
        return self.get_by_email(new_user)
    
    def check_for_email_duplicates(self,email):
        cursor.execute("SELECT * FROM users WHERE email = %s",(email,))
        users = cursor.fetchone()
        if users:
            return users
        else:
            return None


    def get_by_email(self, email):
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if not user:
            return
        #user["email"] = str(user["email"])
        user.pop(1)
        return user

    def encrypt_password(self, password):
        return generate_password_hash(password)

    def user_login(self, email, password):
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if not user or not check_password_hash(user["password"], password):
            return False
        elif user and check_password_hash(user['password'], password):
            return True
        # user.pop(1)
        # user["email"] = str(user["email"])
        # return user[0]
#cursor.close()
#conn.close()
