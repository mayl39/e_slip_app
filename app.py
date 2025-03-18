from flask import Flask, render_template, redirect, url_for, request, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pandas as pd


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# การตั้งค่า Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# เชื่อมต่อกับไฟล์ Excel
df = pd.read_excel('user_data.xlsx')

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        user_data = df[df['UserID'] == user_id]

        if user_data.empty:
            return 'User not found!'
        if user_data.iloc[0]['Password'] == password:
            user = User(user_id)
            login_user(user)
            return redirect(url_for('view_slip'))

        return 'Invalid password!'
    return render_template('login.html')

@app.route('/view_slip')
@login_required
def view_slip():
    user_data = df[df['UserID'] == current_user.id].iloc[0]
    return render_template('slip.html', user=user_data)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
