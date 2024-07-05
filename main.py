from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

config = {
    "host" : "127.0.0.1",
    "port" : "3306", 
    "user" : "root",
    "database" : "social"
}

class user_register(BaseModel):
    username: str
    nome: str
    cognome: str
    password: str

@app.post("/api/register")
def registrazione(user : user_register):
    conn = mysql.connector.connect(**config) 
    cursor  = conn.cursor()
    cursor.execute("INSERT INTO users (username, nome, cognome, password) VALUES (%s,%s,%s,%s)" 
                   , (user.username, user.nome, user.cognome, user.password))
    conn.commit()
    conn.close()
    return {
        "msg" : "utente inserito con successo"
    }
 
@app.get("/api/user/{username}")
def user(username : str):
    conn = mysql.connector.connect(**config) 
    cursor  = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * from users WHERE username = '{username}' ")
    user = cursor.fetchone()
    conn.close()
    if user :
        return user
    else : 
        return {
            "msg" : "utente not found"
        }
    
class post(BaseModel):
    contenuto: str
    
@app.post("/api/create_post/{username}")
def create_post(username:str, post: post):
    conn = mysql.connector.connect(**config)
    cursor  = conn.cursor(dictionary=True)
    cursor.execute("INSERT INTO posts(username, contenuto) VALUES (%s,%s)", 
                   (username, post.contenuto))
    conn.commit()
    conn.close()
    return {
        "msg" : "tutto andato a buon fine"
    }
    
@app.get("/api/home")
def all_post():
    conn = mysql.connector.connect(**config) 
    cursor  = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    conn.close()
    return posts

@app.get("/api/posts/{username}")
def cerca_post(username:str):
    conn= mysql.connector.connect(**config)
    cursor=conn.cursor(dictionary=True)
    cursor.execute(f"SELECT username,contenuto FROM posts WHERE username = '{username}' ")
    posts = cursor.fetchall()
    conn.close
    return posts