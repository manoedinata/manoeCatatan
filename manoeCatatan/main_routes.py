from flask import Blueprint
from flask import url_for, redirect, render_template, request, flash
import base64
import random

from manoeCatatan import catatanDb

main = Blueprint("main_routes", __name__)

def generate_random_id():
    return random.randint(10, 500)

@main.route("/")
def home():
    return render_template("home.html")

@main.route("/add", methods=["POST"])
def add():
    id = generate_random_id()
    editorFormTitle = request.form.get("editorFormTitle")
    editorFormCategory = request.form.get("editorFormCategory")
    editorFormMarkdown = request.form.get("editorFormMarkdown")
    decodedMarkdown = base64.b64decode(editorFormMarkdown)

    data = {
        "judul": editorFormTitle,
        "kategori": editorFormCategory,
        "konten": editorFormMarkdown
    }

    if catatanDb.fetch({"value.judul": editorFormTitle}).items:
        flash("Judul sudah ada!", "danger")
        return redirect(url_for("main_routes.home"))

    try:
        catatanDb.insert({
            "key": str(id),
            "id": id,
            "value": data
        })
        flash("Sukses menambah catatan!", "success")
    except Exception as e:
        flash(str(e), "danger")

    return redirect(url_for("main_routes.home"))

@main.route("/list")
def list():
    catatanList = catatanDb.fetch().items

    return render_template("list.html", list=catatanList)

@main.route("/view/<int:id>")
def view(id):
    catatanItem = catatanDb.fetch({"id": id}).items[0]

    return render_template("view.html", item=catatanItem, id=id)

@main.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    catatanItem = catatanDb.fetch({"id": id}).items[0]

    if request.method == "GET":
        return render_template("edit.html", item=catatanItem, id=id)

    elif request.method == "POST":
        editorFormTitle = request.form.get("editorFormTitle")
        editorFormCategory = request.form.get("editorFormCategory")
        editorFormMarkdown = request.form.get("editorFormMarkdown")
        decodedMarkdown = base64.b64decode(editorFormMarkdown)

        data = {
            "value.judul": editorFormTitle,
            "value.kategori": editorFormCategory,
            "value.konten": editorFormMarkdown,
        }

        try:
            catatanDb.update(data, str(id))
            flash("Sukses mengedit catatan!", category="success")
        except Exception as e:
            flash(str(e), "danger")

        return redirect(url_for("main_routes.view", id=id))

@main.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    try:
        catatanDb.delete(str(id))
        flash(f"Sukses menghapus catatan {id}", "success")
    except Exception as e:
        flash(str(e), "danger")

    return redirect(url_for("main_routes.list"))

@main.route("/category/<postCategory>")
def category(postCategory):
    categoryPosts = catatanDb.fetch({"value.kategori": postCategory})
    count = categoryPosts.count
    items = categoryPosts.items

    return render_template("category.html", category=postCategory, count=count, items=items)
