from backend_web import os, load_dotenv, Flask, render_template, LoginManager, login_user, logout_user, login_required, current_user, flash, url_for, redirect
from backend_web import models as mdls
from backend_web import functions as func
from backend_web import login_required, request, QRcode, abort

load_dotenv(os.path.join(os.getcwd(),".env"))

app = Flask(__name__, static_url_path="/static")

login_manager = LoginManager(app)
login_manager.login_view = "login_page"
QRcode(app)

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
        instance = mdls.Customers("None", form.Name.data, form.Password.data, form.Email.data, form.Phone.data, form.Credit_Card.data)
        instance.register()
        func.notify_new(form.Email.data)
        flash("Created New Account Successfully!")
        return redirect(url_for('login_page'))
    
    for err in form.errors.values():
        flash(f'Error: {err}', category="danger")

    return render_template("register.html", form=form, active_item="Register")

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

@app.route("/register", methods=["GET", "POST"])
@login_required
def checkout():
    form = mdls.CheckOutForm()
    data = mdls.Orders.view_cart(current_user.Cus_Id)
    filled = False
    if form.validate_on_submit() and request.method == "POST":
        if data:
            mdls.Orders.update_order(data["ID_ORDER"].values, "PENDING")
            flash("ORDER SENT", category="success")
            return redirect(url_for("view_all"))
    return render_template("checkout.html", items=data, form=form, filled=filled)

@app.route("/view", methods=["GET"])
@login_required
def view_all():
    data = mdls.Orders.view_orders(current_user.Cus_Id)
    return render_template("view_all.html", items=data)

@app.route("/qrcode/send/<orders_id>")
def QR_CODES(orders_id: str):
    return render_template("qrcode.html", items=orders_id)

@app.route("/query/<items>")
def query_items(items: str):
    cmd, cmd_data, data = func.parse_items(items)

    dic = {
        "STALL_EX": mdls.Stall.retrieve_info,
        "ORDER_STALL": mdls.Orders.view_stall_orders,
        
        }
    


    return 
    

@app.route("/update/<items>")
def update_items(items: str):
    cmd, cmd_data, data = func.parse_items(items)


@app.route("/delete/<items>")
def delete_items(items: str):
    cmd, cmd_data, data = func.parse_items(items)

    dic = {"ORDERS":mdls.Orders.cancel_orders,
            "PRODUCTS": mdls.Products.delete_food}

    if dic.get(cmd_data):
        dic[cmd_data](data)
        return "Success"
    
    return abort(404)
    
    

@app.route("/log_out")
@login_required
def log_out_page():
    logout_user()
    flash("You have been logged out", category="info")
    return redirect(url_for("index"))



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)