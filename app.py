from flask import Flask, render_template, redirect
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

    cur.execute(
        """
        SELECT * FROM mainIngridient WHERE product_id = ?
        """,
        (product_id,),
    )
    ingridient = cur.fetchone()

    cur.execute(
        """
        SELECT * FROM allergens WHERE product_id = ?
        """,
        (product_id,),
    )
    allergen = cur.fetchone()

    cur.execute(
        """
        SELECT * FROM toxicity WHERE product_id = ?
        """,
        (product_id,),
    )
    toxicity = cur.fetchone()
    conn.close()
    return render_template("products_show.html", product=product, ingridient=ingridient, allergen=allergen, toxicity=toxicity)

@app.route("/produkti/<int:product_id>/delete", methods=['POST'])
def delete_products(product_id):
    conn = sqlite3.connect("gus.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        """
        DELETE FROM mainIngridient WHERE product_id = ?
        """,
        (product_id,),
    )
    cur.execute(
        """
        DELETE FROM allergens WHERE product_id = ?
        """,
        (product_id,),
    )
    cur.execute(
        """
        DELETE FROM toxicity WHERE product_id = ?
        """,
        (product_id,),
    )
    cur.execute(
        """
        DELETE FROM products WHERE id = ?
        """,
        (product_id,),
    )
    conn.commit()
    conn.close()
    return redirect("/produkti")

if __name__ == "__main__":
    app.run(debug=True)