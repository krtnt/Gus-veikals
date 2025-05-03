from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/produkti")
def products():
    conn = sqlite3.connect("gus.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM products
        """
    )
    products = cur.fetchall()
    conn.close()
    print(products[0]['name'])
    return render_template("products.html", products=products)

@app.route("/produkti/<int:product_id>")
def products_show(product_id):
    conn = sqlite3.connect("gus.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM products WHERE id = ?
        """,
        (product_id,),
    )
    product = cur.fetchone()
    conn.close()
    return render_template("products_show.html", product=product)

if __name__ == "__main__":
    app.run(debug=True)