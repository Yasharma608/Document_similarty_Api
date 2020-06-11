from flask import Flask,jsonify,request
from flask_restful import Api ,Resource
from pymongo import MongoClient
import bcrypt

app=Flask(__name__)
api=Api(app)

client =MongoClient("mongodb://db:27017")
db=client.SimilartyDB
users=db["Users"]

def UserExist(username):
    if users.find({"Username":username}).count() == 0:
        return False
    else:
        return True
def verfiypw(ussername):
    if not UserExist(username):
        return False
    hashed_pw=users,find({
        "username":username})[0]["Password"]
    
    if bcrypt.hashpw(password.encode('utf8'),hashed_pw == hashed_pw:
                     retun True
    else:
        return False
def countTokens(username):
    tokens =users.find({
        "username":username})[0]["Tokens"]
    return tokens

class Register(Resource):
        def post(self):
            postedData =request.get_json()
            
            username=postedData["username"]
            password=postedData["password"]
            
            if UserExist(username):
                retjson={
                    "status":301,
                    "msg":"Invalid Username"}
                return jsonify(retjson)
            hashed_pw = bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt())
            users.insert({
                "Username":username,
                "password":hashed_pw,
                "Tokens":6
                })
            retjson={
                "status":200,
                "msg":"you have sucessfulyy signed up to the Api"}
            return jsonify(retjson)

class Detect(Resource):
    def post(self):
        postedData=request.getjson()
        
        username=postedData["username"]
        password =postedData["password"]
        
        if not UserExist(username):
            retjson={
                "status":"301",
                "msg":"invalid Usernamee"
                }
            return jsonify(retjson)
        correct_pw=verifypw(username,password)
        
        if not correct_pw:
            retjson={
                "status":"302",
                "msg":"Invalid Password"}
            return jsonify(retjson)
        
        num_tokens = countTokens(username)
        
        if num_tokens<=0:
            retjson ={
                "status":"303",
                "msg":"sorry out of tokens refine"
                }
            return jsonify(retjson)
        #calculating the editditance
        nlp=spacy.load("en_core_web_sm")
        
        text1=nlp(text1)
        text2=nlp(text2)
        
        #ratio of the text
        ratio =text1.similarity(text2)
        
        retjson ={
            "status":200,
            "similarity":ratio,
            "msg":"similarity score"
            }
        current_token=countTokens(username)
        
        
        user.update({
            "username":username,
            },{
                "$set":{
                    "Token":current_token-1}  
                })
        return jsonify(retjson)

class Refill(Resource):
    def post(self):
        postedData = request.get_jason()
        
        username=postedData["username"]
        password=postedData["admin_pw"]
        refill_amount =postedData["refill"]
        
        if not UserExist(username):
            retjson={
                "status":"301",
                "msg":"invalid Usernamee"
                }
            return jsonify(retjson)
        correct_pw="abc123"
        if not passoword==correct_pw:
            retjson={
                "status":304,
                "msg":"invalid admin password"
                }
            return jsonify(retjson)
        current_token=countTokens(username)
        
        
        users.update({
            "username":username,
            },{
                "$set":{
                    "Token":current_token+refill_amount}  
                })
        retjson={
            "status":200,
            "msg":"token is filled "}
        return jsonify(retjson)

api.add_resource(Register, '/register')
api.add_resource(Detect, '/detect')
api.add_resource(Refill, '/refill')


if __name__=="__main__":
    app.run(host='0.0.0.0')
    
