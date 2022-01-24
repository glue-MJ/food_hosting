from backend_web import os, load_dotenv, Flask, render_template, LoginManager

load_dotenv(os.path.join(os.getcwd(),".env"))

app = Flask(__name__, static_url_path="/static")

login_manager = LoginManager(app)
login_manager.login_view = "login_page"

# @login_manager.user_loader
# def load_user(user_id):
#     return 0

# HOME PAGE
@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html", active_item="home")

# @app.route("/search")
# def search():
#     return render_template("search.html")

# @app.route("/login")
# def login_page():
    # return render_template("login_page.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
    