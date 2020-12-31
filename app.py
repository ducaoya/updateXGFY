from flask import Flask
import os
app = Flask(__name__)
@app.route('/')
def hello():
    print("The project is running !")
    os.system("python updateXGFY.py")
	
if __name__ == 	'__main__':
	app.run()