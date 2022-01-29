from unicodedata import category
from backend_web import os, load_dotenv, Flask, render_template, LoginManager, login_user, logout_user, login_required, current_user, flash, url_for, redirect
from backend_web import models as mdls
from backend_web import functions as func
from backend_web import login_required, request

load_dotenv(os.path.join(os.getcwd(),".env"))

app = Flask(__name__, static_url_path="/static")

login_manager = LoginManager(app)
login_manager.login_view = "login_page"

@login_manager.user_loader
def load_user(user_id):
    return mdls.Customers.retrieve_person(user_id)

# HOME PAGE
@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html", active_item="home")

# LOGIN PAGE
@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = mdls.LoginForm()
    if form.validate_on_submit():
        user_attempt = mdls.Customers.signin(form.Name.data, form.Password.data)
        login_user(user_attempt)
        flash("Logged In", category="success")
        return redirect(url_for("index"))

    for err in form.errors.values():
        flash(f'Error: {err}', category="danger")
    
    return render_template("login.html", active_item="Login", form=form)

# REGISTER PAGE
@app.route("/register")
def register_page():
    form = mdls.RegisterForm()
    if form.validate_on_submit():
        mdls.Customers("None", form.Name.data, form.Password.data, form.Email.data, form.Phone.data, form.Credit_Card.data)

# SEARCH PAGE
@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    form = mdls.SearchForm()
    p_form = mdls.PurchaseForm()
    if form.validate_on_submit():
        data = mdls.Products.query_food(form.SearchValue.data)
        return render_template("search.html", active_item="Search", form=form, items=data, purchase_form=p_form)
    if p_form.validate_on_submit() and request.form.get("Purchased-Item"):
        data = mdls.Products.query_food(form.SearchValue.data)
        cart = mdls.Orders("NULL", request.form.get("Purchased-Item"), "CARTED", "NULL", current_user.Phone, current_user.Cus_Id)
        cart.new_order()
        flash("Added", category="success")
        return render_template("search.html", active_item="Search", form=form, items=data, purchase_form=p_form)
    return render_template("search.html", active_item="Search", form=form, items=mdls.Products.query_food(""), purchase_form=p_form)



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
    