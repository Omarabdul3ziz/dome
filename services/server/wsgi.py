#! /usr/bin/python3

from app import app

if __name__ == '__main__':
    app.run(debug=True, ssl_context=('/home/omar/localhost.pem', '/home/omar/localhost-key.pem'))