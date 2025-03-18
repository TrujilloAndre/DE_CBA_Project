from flask import Flask, render_template, request, redirect, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), 'Storage.env')
load_dotenv(dotenv_path)

# Flask Instance
app = Flask(__name__)

# Creating DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)
app.secret_key = app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# DB Model
class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    store_id = db.Column(db.String(100), nullable=False)
    total_sales = db.Column(db.Numeric(10,2), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id
    
# Routes using post and get methods
@app.route('/', methods=['POST', 'GET'])
def index():
    # Post Method
    if request.method == 'POST':
        store_id = request.form['store_id']
        total_sales = request.form['total_sales']
        date = request.form['date']

        new_task = Sales(store_id=store_id, 
                        total_sales=float(total_sales),
                          date=datetime.strptime(date, '%Y-%m-%d'))

        try:
            db.session.add(new_task)
            db.session.commit()
            flash('Sale added successfully!', 'success')
            return redirect('/')
        except:
            return 'Error adding sale'
    # Get Method
    else:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        output_format = request.args.get('output_format')

        # If no date range is selected, show last 5 sales
        if not start_date or not end_date:
            sale_vals = Sales.query.order_by(Sales.id.desc()).limit(5).all()
            return render_template('index.html', sales=sale_vals)
        else:
            sale_vals = Sales.query.filter(Sales.date.between(start_date, end_date)).all()
        if not sale_vals:
            return 'No data found for the selected range'
        # Adding data to a list if in date range
        sales_data = []
        for sale in sale_vals:
            sales_data.append({
                'id': sale.id,
                'store_id': sale.store_id,
                'total_sales': sale.total_sales,
                'date': sale.date
            })
        # Output format, either json, list or dataframe
        if output_format == 'json':
            return jsonify(sales_data)
        if output_format == 'list':
            return str(sales_data)
        if output_format == 'dataframe':
            df = pd.DataFrame(sales_data)
            return df.to_html()  
        else: 
            return 'Invalid output format. Please use json, list or dataframe.'

# Delete function
@app.route('/delete/<int:id>')
def delete(id):
    sale_to_delete = Sales.query.get_or_404(id)

    try:
        db.session.delete(sale_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Error deleting sale'
# Update function
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    sale = Sales.query.get_or_404(id)
    if request.method == 'POST':
        sale.store_id = request.form['store_id']
        sale.total_sales = request.form['total_sales']
        sale.date = request.form['date']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Error updating sale'
    else:
        return render_template('update.html', sale=sale)
# Run the app
if __name__ == '__main__':
    app.run(debug=True)
