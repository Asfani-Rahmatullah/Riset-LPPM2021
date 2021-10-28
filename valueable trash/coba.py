from flask import Flask, render_template, url_for, request

application = Flask(__name__)

@application.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        nama = request.form['nama']
        email = request.form['email']
        return render_template('cobatampil.html',nama=nama,email=email)
    return render_template('coba1.html')

if __name__ == '__main__':
    application.run(debug=True)