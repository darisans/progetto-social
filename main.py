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
    
#la rotta di stampa di tutti gli utenti
@app.get("/api/allusers")
def all_users():
    conn = mysql.connector.connect(**config) # host = config#host
    cursor  = conn.cursor(dictionary=True)
    cursor.execute("SELECT * from users")
    #fetchall restituisce una lista degli oggetti utenti trovati
    users = cursor.fetchall()
    conn.close()
    return users
    
#la rotta che stampa i dati di un dato username specifico
@app.get("/api/user/{username}")
def user(username : str):
    conn = mysql.connector.connect(**config) # host = config#host
    cursor  = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * from users WHERE username = '{username}' ")
    conn.close()
    #fetchone restituisce la prima riga che ha trovato
    #   noi sappiamo che la riga sarà prima ma anche unica
    user = cursor.fetchone()
    if user :
        return user
    else : 
        return {
            "msg" : "utente not found"
        }
        
# La parte due : 
#voglio creare la rotta di creazione post e di stampa tutti i post
class post(BaseModel):
    descrizione: str
    image_url: str
    
#rotta di creazione post tramite metodo post
@app.post("/api/create_post/{username}")
def create_post(username:str, post: post):
    conn = mysql.connector.connect(**config) # host = config#host
    cursor  = conn.cursor(dictionary=True)
    cursor.execute("INSERT INTO posts(username, descrizione, image_url) VALUES (%s,%s,%s)", 
                   (username, post.descrizione, post.image_url))
    conn.commit()
    conn.close()
    return {
        "msg" : "tutto andato a buon fine"
    }
    
#creiamo la rotta di stampa post
@app.get("/api/home")
def all_post():
    conn = mysql.connector.connect(**config) # host = config#host
    cursor  = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    #fetchall restituisce una lista degli oggetti post trovati
    conn.close()
    return posts