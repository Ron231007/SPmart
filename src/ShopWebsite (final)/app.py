from flask import Flask, render_template, request, redirect, url_for, session, abort, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField, PasswordField
from wtforms.validators import DataRequired, NumberRange, ValidationError, Optional
import qrcode
import os
import bcrypt
from datetime import datetime, timedelta,timezone
import math




# ——— 1. App & DB setup —————————————————————————————
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-this-to-a-secure-key')
# Your existing alwaysdata connection (keeps original creds)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+mysqlconnector://'
     'spmart_rondell:%40F5urcfEttYixft'
     '@mysql-spmart.alwaysdata.net:3306/'
     'spmart_main_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ——— 2. Models ——————————————————————————————————————
class Product(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(50), nullable=False)
    isAlcoholic   = db.Column(db.Integer, nullable=False, default=0)
    price         = db.Column(db.Float, nullable=False)
    quantity      = db.Column(db.Integer, nullable=False, default=0)

class Order(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    option        = db.Column(db.String(10), nullable=False)
    delivery_fee  = db.Column(db.Float, nullable=False, default=0.0)
    total_amount  = db.Column(db.Float, nullable=False)

class OrderItem(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    order_id   = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity   = db.Column(db.Integer, nullable=False)
    price_each = db.Column(db.Float, nullable=False)

# Map to your phpMyAdmin table "user_info"
class UserInfo(db.Model):
    __tablename__ = 'user_info'
    user_id = db.Column(db.Integer, primary_key=True)       # maps to user_id column
    passwd = db.Column(db.String(128), nullable=False)      # maps to passwd column; storing plain text per your request
    points = db.Column(db.Integer, nullable=True)
    card_id = db.Column(db.String(100), nullable=True)
    card_password = db.Column(db.String(100), nullable=True)
    failed_attempts = db.Column(db.Integer, default=0)
    lockout_until = db.Column(db.DateTime, nullable=True)
    lockout_count = db.Column(db.Integer, default=0)

# ——— 3. Create tables & seed products (if not present) —————————
offset = 1000000000
with app.app_context():
    db.create_all()   # safe: will create any missing tables (won't drop existing)
    # Seed default products if empty
    if Product.query.count() == 0:
        products = [
            Product(id=offset+1, name='Apple',    isAlcoholic=0, price=1.2,  quantity=10),
            Product(id=offset+2, name='Water',    isAlcoholic=0, price=0.55, quantity=50),
            Product(id=offset+3, name='Butter',   isAlcoholic=0, price=5.15, quantity=20),
            Product(id=offset+4, name='Milk',     isAlcoholic=0, price=6.70, quantity=20),
            Product(id=offset+5, name='Eggs',     isAlcoholic=0, price=4.15, quantity=30),
            Product(id=offset+6, name='Oil',      isAlcoholic=0, price=8.95, quantity=30),
            Product(id=offset+7, name='Salmon',   isAlcoholic=0, price=8.50, quantity=20),
            Product(id=offset+8, name='Honey',    isAlcoholic=0, price=6.65, quantity=30),
            Product(id=offset+9, name='IceCream', isAlcoholic=0, price=14.77,quantity=30),
            Product(id=offset+10, name='Beer',     isAlcoholic=1, price=5.50, quantity=20),
            Product(id=offset+11, name='Wine',     isAlcoholic=1, price=26.50,quantity=30),
            Product(id=offset+12, name='Bread',    isAlcoholic=0, price=3.20, quantity=40),
        ]
        db.session.add_all(products)
        db.session.commit()

# ——— 4. Cart helpers ————————————————————————————————
def get_cart():
    """Return cart dict stored in session: { prod_id_str: qty_int }"""
    return session.setdefault('cart', {})

def add_to_cart(prod_id, qty=1):
    cart = get_cart()
    # ensure qty is int >= 1
    try:
        qty = int(qty)
    except Exception:
        qty = 1
    if qty < 1:
        qty = 1
    cart[str(prod_id)] = cart.get(str(prod_id), 0) + qty
    session.modified = True

def set_cart_item(prod_id, qty):
    """Set quantity or remove if qty <= 0"""
    cart = get_cart()
    if qty <= 0:
        cart.pop(str(prod_id), None)
    else:
        cart[str(prod_id)] = int(qty)
    session.modified = True

def remove_from_cart(prod_id):
    cart = get_cart()
    cart.pop(str(prod_id), None)
    session.modified = True

def clear_cart():
    session.pop('cart', None)

# ——— 5. WTForms ————————————————————————————————
class CheckoutForm(FlaskForm):
    name   = StringField('Your Name', validators=[DataRequired()])
    option = SelectField('Delivery Option', choices=[('pickup','Pickup (free)'),('delivery','Delivery ($4)')])
    submit = SubmitField('Place Order')

    def validate(self, extra_validators=None):
        rv = super().validate(extra_validators=extra_validators)
        if not rv:
            return False

        # Reload current user fresh from the database
        user_id = session.get('user_id')
        if not user_id:
            self.option.errors.append("You must be logged in to place an order.")
            return False

        user = UserInfo.query.get(user_id)
        print(f"Card ID is: {user.card_id}")

        # Conditional check: delivery requires a linked card
        if self.option.data == 'delivery' and user.card_id is None:
            self.option.errors.append("You must link an ATM card to choose delivery.")
            return False

        return True
    

def validate_card_id(form, field):
    if field.data:
        if not field.data.isdigit() or len(field.data) != 10:
            raise ValidationError("Card ID must be exactly 10 digits")

def validate_card_password(form, field):
    if field.data:
        if not field.data.isdigit() or len(field.data) > 10:
            raise ValidationError("Card password cannot be longer than 10 digits")
# Validation rules for signup
def password_rule(form, field):
    pw = field.data or ''
    if not pw.isdigit() or len(pw) != 8:
        raise ValidationError('Password must be exactly 8 digits.')
    if len(set(pw)) < 4:
        raise ValidationError('Password must contain at least 4 distinct digits.')

class SignupForm(FlaskForm):
    user_id = IntegerField('Username (numbers only)', validators=[
        DataRequired(),
        NumberRange(min=1, max=99999999, message='Username must be between 1 and 99,999,999')
    ])
    passwd = StringField('Password (8 digits)', validators=[DataRequired(), password_rule])
    card_id = StringField('Card ID', validators=[Optional(), validate_card_id])
    card_password = PasswordField('Card Password', validators=[Optional(), validate_card_password])
    submit = SubmitField('Sign Up')

    def validate(self, extra_validators=None):
    # first run default validation
        rv = super().validate(extra_validators=extra_validators)
        if not rv:
            return False

        # conditional card password check
        if self.card_id.data and not self.card_password.data:
            self.card_password.errors.append("Card password is required")
            return False

        return True
class EditCardForm(FlaskForm):
    card_id = StringField('Card ID', validators=[DataRequired(), validate_card_id])
    card_password = PasswordField('Card Password', validators=[DataRequired(), validate_card_password])
    back = SubmitField('back')
    submit = SubmitField('Save')


class LoginForm(FlaskForm):
    user_id = IntegerField('Username', validators=[DataRequired()])
    passwd = PasswordField('Password', validators=[DataRequired()])
    
    submit = SubmitField('Log In')

    

# ——— 6. Routes —————————————————————————————————————
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/product/<int:prod_id>', methods=['GET', 'POST'])
def detail(prod_id):
    """
    GET: show product page with qty form
    POST: add requested quantity to cart and redirect to cart (or back)
    """
    product = Product.query.get_or_404(prod_id)

    if request.method == 'POST':
        # get qty from the form, default 1
        qty = request.form.get('qty', '1')
        try:
            qty = int(qty)
        except Exception:
            qty = 1
        if qty < 1:
            qty = 1

        # Optionally, check stock and warn if user tries to add more than available.
        if qty > product.quantity:
            flash(f'Only {product.quantity} of {product.name} available. Added maximum available.')
            qty = product.quantity

        add_to_cart(prod_id, qty)
        flash(f'Added {qty} x {product.name} to cart.')
        return redirect(url_for('index'))

    # GET
    return render_template('detail.html', product=product)

@app.route('/add/<int:prod_id>')   # backward-compatible link usage
def add(prod_id):
    """Simple add-one-by-one route kept for compatibility; supports optional ?qty= query param."""
    p = Product.query.get_or_404(prod_id)
    qty = request.args.get('qty', '1')
    try:
        qty = int(qty)
    except Exception:
        qty = 1
    if qty < 1:
        qty = 1
    # optional check vs stock
    if qty > p.quantity:
        flash(f'Only {p.quantity} of {p.name} available.')
        qty = p.quantity
    add_to_cart(prod_id, qty)
    flash('Added to cart!')
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    cart = get_cart()
    items, subtotal = [], 0
    for pid, qty in cart.items():
        p = Product.query.get(int(pid))
        if not p:
            continue
        line = p.price * qty
        items.append((p, qty, line))
        subtotal += line
    return render_template('cart.html', items=items, subtotal=subtotal)

@app.route('/cart/update', methods=['POST'])
def update_cart():
    """
    Update quantity or remove item from cart.
    Expects form fields: prod_id, action ('update'|'remove'), qty (for update).
    """
    prod_id = request.form.get('prod_id')
    action = request.form.get('action')
    if not prod_id:
        flash('Invalid request.')
        return redirect(url_for('cart'))

    try:
        pid = int(prod_id)
    except Exception:
        flash('Invalid product id.')
        return redirect(url_for('cart'))

    if action == 'remove':
        remove_from_cart(pid)
        flash('Item removed from cart.')
        return redirect(url_for('cart'))

    if action == 'update':
        qty = request.form.get('qty', '0')
        try:
            qty = int(qty)
        except Exception:
            qty = 0
        if qty <= 0:
            remove_from_cart(pid)
            flash('Item removed from cart.')
            return redirect(url_for('cart'))

        # check stock
        p = Product.query.get(pid)
        if p and qty > p.quantity:
            flash(f'Only {p.quantity} available for {p.name}. Quantity set to available stock.')
            qty = p.quantity

        set_cart_item(pid, qty)
        flash('Cart updated.')
        return redirect(url_for('cart'))

    flash('Unknown action.')
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = CheckoutForm()
    cart_data = get_cart()
    if not cart_data:
        flash('Your cart is empty.')
        return redirect(url_for('index'))

    if form.validate_on_submit():
        name, option = form.name.data, form.option.data
        fee = 4.0 if option == 'delivery' else 0.0
        subtotal = sum(Product.query.get(int(pid)).price * qty for pid, qty in cart_data.items())
        total = subtotal + fee

        order = Order(customer_name=name, option=option, delivery_fee=fee, total_amount=total)
        db.session.add(order)
        db.session.flush()

        # Store order items & update stock
        items_text = []
        for pid, qty in cart_data.items():
            p = Product.query.get(int(pid))
            if p.quantity < qty:
                flash(f'Not enough stock for {p.name}.')
                return redirect(url_for('cart'))
            p.quantity -= qty
            db.session.add(OrderItem(order_id=order.id, product_id=p.id, quantity=qty, price_each=p.price))
            items_text.append(f"{p.name} x{qty}")

        db.session.commit()

        # Create QR content as a clean text block
        qr_content = (
            f"Order ID: {order.id}\n"
            f"Customer: {name}\n"
            f"Option: {option}\n"
            f"Items:\n" + "\n".join(items_text) + "\n"
            f"Delivery Fee: ${fee:.2f}\n"
            f"Total: ${total:.2f}"
        )

        qr_url = None
        if option == 'pickup':
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_Q,
                box_size=4,
                border=2
            )
            qr.add_data(qr_content)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            # Save to the app's static folder reliably
            qr_dir = os.path.join(app.root_path, 'static', 'qr')
            os.makedirs(qr_dir, exist_ok=True)
            path = os.path.join(qr_dir, f'order_{order.id}.png')
            img.save(path)
            qr_url = url_for('static', filename=f'qr/order_{order.id}.png')

        clear_cart()
        return render_template('confirmation.html', order=order, qr_url=qr_url)

    return render_template('checkout.html', form=form)

# ——— Authentication routes —————————————————————————————
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    
    # Determine the next available user_id
    last_user = db.session.query(UserInfo).order_by(UserInfo.user_id.desc()).first()
    next_user_id = 1 if not last_user else last_user.user_id + 1
    if next_user_id > 99999999:
        flash('Maximum number of users reached.')
        return redirect(url_for('login'))   

    # Pre-fill the form's user_id field with next available ID
    form.user_id.data = next_user_id

    if form.validate_on_submit():
        pw = form.passwd.data  # plain text per your table design
        hashed_pw = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        card_id = form.card_id.data
        if card_id:  # True if user entered something
            card_pw = form.card_password.data
            hashed_card_password = bcrypt.hashpw(card_pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user = UserInfo(
                user_id=next_user_id,
                passwd=hashed_pw,
                points=0,
                card_id=card_id,
                card_password=hashed_card_password
            )
        else:
            user = UserInfo(
                user_id=next_user_id,
                passwd=hashed_pw,
                points=0,
                card_id=None,
                card_password=None
            )
        db.session.add(user)
        db.session.commit()
        flash(f'Account created. Your User ID is {next_user_id}. Please log in.')
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

@app.route('/edit_card', methods=['GET', 'POST'])
def edit_card():
    user_id = session.get('user_id')
    if not user_id:
        flash("You must be logged in to edit your card.")
        return redirect(url_for('login'))

    user = UserInfo.query.get(user_id)
    if not user:
        flash("User not found.")
        return redirect(url_for('login'))

    form = EditCardForm()

    # Pre-fill form with existing card info (but not password)
    if request.method == "GET" and user.card_id:
        form.card_id.data = user.card_id

    if form.validate_on_submit():
        card_id = form.card_id.data.strip()
        card_pw = form.card_password.data.strip()

        if len(card_pw) > 10:
            flash("Password cannot be more than 10 digits long.")
            return render_template('edit_card.html', form=form)

        # Save / update card
        hashed_card_pw = bcrypt.hashpw(card_pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.card_id = card_id
        user.card_password = hashed_card_pw

        db.session.commit()
        flash("Card info updated successfully!")
        return redirect(url_for('checkout'))

    return render_template('edit_card.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    MAX_ATTEMPTS = 5
    form = LoginForm()

    if form.validate_on_submit():
        # Validate user ID
        try:
            uid = int(form.user_id.data)
        except (ValueError, TypeError):
            flash("Wrong username or password, try one more time")
            return render_template('login.html', form=form)

        user = UserInfo.query.filter_by(user_id=uid).first()

        # Check if account is locked
        if user and user.lockout_until:
            # Convert DB value (naive) to aware UTC
            lockout_aware = user.lockout_until.replace(tzinfo=timezone.utc)
            now_utc = datetime.now(timezone.utc)
            if lockout_aware > now_utc:
                remaining_seconds = (lockout_aware - now_utc).total_seconds()
                remaining_minutes = max(1, math.ceil(remaining_seconds / 60))
                flash(f"Account locked. Try again in {remaining_minutes} minutes.")
                return render_template('login.html', form=form)

        # Get password from form
        pw = form.passwd.data

        # Check password
        if not user or not bcrypt.checkpw(pw.encode('utf-8'), user.passwd.encode('utf-8')):
            if user:
                # Increment failed attempts
                user.failed_attempts += 1

                if user.failed_attempts >= MAX_ATTEMPTS:
                    # Exponential backoff: 2^lockout_count minutes, at least 1 minute
                    lock_minutes = max(1, 2 ** user.lockout_count)
                    user.lockout_until = datetime.now(timezone.utc) + timedelta(minutes=lock_minutes)
                    user.failed_attempts = 0
                    user.lockout_count += 1
                    db.session.commit()
                    flash(f"Account locked for {lock_minutes} minutes due to too many failed attempts.")
                else:
                    db.session.commit()
                    remaining_tries = MAX_ATTEMPTS - user.failed_attempts
                    flash(f"Wrong username or password, remaining tries: {remaining_tries}")

            else:
                flash("Wrong username or password, try one more time")

            return render_template('login.html', form=form)

        # Success: password correct
        else:
            session['user_id'] = user.user_id
            user.failed_attempts = 0
            user.lockout_until = None
            user.lockout_count = 0
            db.session.commit()
            flash('Logged in successfully.')
            return redirect(url_for('index'))

    return render_template('login.html', form=form)

    

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out.')
    return redirect(url_for('index'))

# ——— 7. Run —————————————————————————————————————
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
   
