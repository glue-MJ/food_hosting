from backend_web import os, load_dotenv, Flask, render_template, LoginManager, login_user, logout_user, login_required, current_user, flash, url_for, redirect
from backend_web import models as mdls
from backend_web import functions as func
from backend_web import login_required, request, QRcode, abort, pd, path_sql
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import json

load_dotenv(os.path.join(os.getcwd(),".env"))

app = Flask(__name__, static_url_path="/static")

SECRET_KEY = os.environ.get("SECRET_KEY")
app.config["SECRET_KEY"] = SECRET_KEY
app.config["UPLOADED_PHOTOS_DEST"] = os.path.join(os.getcwd(), "static")

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

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
@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = mdls.RegisterForm()
    if form.validate_on_submit():
        instance = mdls.Customers(0, form.Name.data, form.Password.data, form.Email.data, form.Phone.data, form.Credit_Card.data)
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
    if form.validate_on_submit() and request.method == "POST":
        data = mdls.Products.query_food(form.SearchValue.data)[["NAME", "PRICE", "DESCRIPTION", "ID_PRODUCT"]]
        return render_template("search.html", active_item="Search", form=form, items=data, purchase_form=p_form)
    if p_form.validate_on_submit() and request.form.get("Purchased-Item"):
        data = mdls.Products.query_food(form.SearchValue.data)[["NAME", "PRICE", "DESCRIPTION", "ID_PRODUCT"]]
        cart = mdls.Orders(0, request.form.get("Purchased-Item"), "CARTED", "NULL", current_user.Phone, current_user.Cus_Id)
        cart.new_order()
        flash("Added", category="success")
        return render_template("search.html", active_item="Search", form=form, items=data, purchase_form=p_form)
    return render_template("search.html", active_item="Search", form=form, items=mdls.Products.query_food("")[["NAME", "PRICE", "DESCRIPTION", "ID_PRODUCT"]], purchase_form=p_form)

@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    form = mdls.CheckOutForm()
    data = mdls.Orders.view_cart(current_user.Cus_Id)[["NAME", "PRICE", "ID_ORDER"]]
    subtotal = data.PRICE.values.sum()
    filled = data.values.size >= 1  # TEST FOR LEN
    if form.validate_on_submit() and request.method == "POST":
        if filled:
            mdls.Orders.update_order(data["ID_ORDER"].values, "PENDING")
            flash("ORDER SENT", category="success")
            return redirect(url_for("view_all"))
    return render_template("checkout.html", items=data, form=form, filled=filled, Aggregate=subtotal)

@app.route("/view", methods=["GET"])
@login_required
def view_all():
    data = mdls.Orders.view_orders(current_user.Cus_Id)
    return render_template("view_all.html", items=data)

@app.route("/qrcode/send/<orders_id>")
def QR_CODES(orders_id: str):
    return render_template("qrcode.html", items=f'{orders_id}')

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    form = mdls.UploadForm()
    if form.validate_on_submit():
        with open("products.json") as file:
            dic = json.load(file)
            filename = photos.save(form.photo.data)
            file_url = photos.url(filename)
            if dic.get(f'{form.ID.data}'):
                dic[f'{form.ID.data}'] = f'{filename}'
    else:
        file_url = None
    return render_template("upload.html", form=form, file_url=file_url)

@app.route("/query/<items>")
def query_items(items: str):
    cmd, cmd_data, data = func.parse_items(items)

    dic = {
        "STALL": mdls.Stall.retrieve_info,
        "ORDER": mdls.Orders.view_stall_orders,
        "TRACK": mdls.Track.QUERY,
        "TRACK_QUERY": mdls.Track.QUERY_BOX
        }
    
    if dic.get(cmd_data):
        df = dic[cmd_data](*data)
        typing = type(df) == pd.core.frame.DataFrame or type(df) == pd.core.series.Series
        return df.to_html() if typing else f'{df}'

    return abort(404)

@app.route("/query_sql/<query>")
def query_sql(query: str):
    cmd, cmd_data, data = func.parse_items(query)
    key = os.environ.get("SECRET_KEY")
    if cmd_data == key:
        return func.query_sql(path_sql, query, True)
    return abort(404)

@app.route("/upload")

@app.route("/update/<items>")  # CMD=COMMAND&FIELD1=1&3 EXAMPLE
def update_items(items: str):
    cmd, cmd_data, data = func.parse_items(items)

    if cmd_data == "REGISTER_STALL":
        mdls.Stall(*data).register()
        return "Success"
    elif cmd_data == "ADD_FOOD":
        mdls.Products(*data).add_food()
        return "Success"
    elif cmd_data == "UPDATE_FOOD":
        dic = {i.upper():j for i, j in (x.split("=") for x in data)}
        mdls.Products.update_food(**dic)
        return "Success"
    elif cmd_data == "UPDATE_ORDER":
        mdls.Orders.update_order(*data)
        return "Success"
    elif cmd_data == "ALLOCATE_ORDER":
        mdls.Track.ALLOCATE(*data)
        return "Success"
    elif cmd_data == "COLLECTION_ORDER":
        mdls.Orders.update_order(data, "COLLECTED")
        return "Success"
    elif cmd_data == "COMPLETE_TRACK_ORDER":
        mdls.Track.COMPLETE(*data)
        return "Success"
    else:
        return abort(404)

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