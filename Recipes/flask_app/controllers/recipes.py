from flask import render_template, redirect, request,session
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User


@app.route('/new/recipe')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('add_recipe.html',user=User.get_by_id(data))


@app.route('/create/recipe',methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate(request.form):
        return redirect('/new/recipe')
    data = {
        "user_id": session["user_id"],
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "date": request.form["date"],
        "under_30_min": int(request.form["under_30_min"])
        
        
    }
    Recipe.create(data)
    return redirect('/dashboard')

@app.route('/edit/recipe/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_recipe.html",edit=Recipe.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/recipe',methods=['POST'])
def update():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate(request.form):
        return redirect('/new/recipe')
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "under_30_min": int(request.form["under_30_min"]),
        "date": request.form["date"],
        "id": request.form['id']
    }
    Recipe.update(data)
    return redirect('/dashboard')

@app.route('/recipe/<int:id>')
def show_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    recipe = Recipe.get_one(data)
    user_data = {
        "id": session['user_id']
    }
    user = User.get_by_id(user_data)
    updated_date = None
    if recipe.updated_at is not None and recipe.updated_at > recipe.created_at:
        updated_date = recipe.updated_at.strftime('%Y-%m-%d %H:%M:%S')

    return render_template("show_recipe.html", recipe=recipe, user=user, updated_date=updated_date)






@app.route('/destroy/recipe/<int:id>')
def destroy_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Recipe.destroy(data)
    return redirect('/dashboard')
