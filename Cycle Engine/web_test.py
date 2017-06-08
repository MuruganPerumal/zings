from flask import Flask, redirect, url_for, request,render_template,redirect
from flask import session
import Search_based_on_tags as engClass
app = Flask(__name__)
app.secret_key = 'some_secret'

@app.route("/searchRes",methods = ['POST', 'GET'])
def searchResult():
    if request.method == 'POST':
        user = request.form['searchbar']
        print(user)
        returnResult = engClass.searchEngine(user)
        return render_template('result.html', user=returnResult)

    messages = request.args['messages']  # counterpart for url_for()
    messages = session['messages']
    returnResult = engClass.searchEngine(messages)
    return render_template('result.html',user = returnResult)

@app.route('/about_us')
def about_us():
   return render_template("about_us.html")


@app.route('/',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['searchbar']
      messages = user
      session['messages'] = messages
      print(messages)
      return redirect(url_for("searchResult",messages=messages))

   return render_template("index.html")


if __name__ == '__main__':
    #app.run(debug = True)
    app.run()
