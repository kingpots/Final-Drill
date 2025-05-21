from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root123'
app.config['MYSQL_DB'] = 'mydb'

mysql = MySQL(app)


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM customers")
    customers = cur.fetchall()
    cur.close()

    return render_template('index.html', customers=customers)

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        email = request.form['email']
        phone_number = request.form['phone_number']
        town_city = request.form['town_city']
        country = request.form['country']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO customers (first_name, middle_name, last_name, gender, email, phone_number, town_city, country) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (first_name, middle_name, last_name, gender, email, phone_number, town_city, country))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        email = request.form['email']
        phone_number = request.form['phone_number']
        town_city = request.form['town_city']
        country = request.form['country']
        cur.execute("UPDATE customers SET first_name=%s, middle_name=%s, last_name=%s, gender=%s, email=%s, phone_number=%s, town_city=%s, country=%s WHERE id=%s", (first_name, middle_name, last_name, gender, email, phone_number, town_city, country, id))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('index'))
    else:
        cur.execute("SELECT * FROM customers WHERE id = %s", (id,))
        customer = cur.fetchone()
        cur.close()

        return render_template('edit_add.html', customer=customer)

@app.route('/delete/<int:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM customers WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
