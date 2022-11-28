from flask import (
    Blueprint,
    render_template,
    url_for,
    request,
    redirect,
    flash,
)
from App.models import (
    User,
    Recipe,
    Ingredient,
    Saved,
)
from App import db, bcrypt
from App.forms import (
    UpdateProfileForm,
    RecipeForm,
    ChangePasswordForm,
)
from Controls import PassiveControls
user = Blueprint("user", __name__, static_folder="static", template_folder="templates")


@user.route('/')
def index():
    valid = PassiveControls.validation()
    if valid[0] and valid[2] == "user":
        editor_recipe = Recipe.query.filter_by(status=1).all()
        featured = Recipe.query.filter_by(status=2)
        users = User.query.filter_by(type="user").paginate(per_page=3)
        return render_template('user/index.html', editor_recipe=editor_recipe, featured=featured, users=users)
    else:
        return render_template("error.html", error=PassiveControls.ErrMsg.access)


@user.route('/profile')
def profile():
    valid = PassiveControls.validation()
    if valid[0] and valid[2] == "user":
        user_data = User.query.get_or_404(valid[1])
        recipe = Recipe.query.filter_by(created_by=valid[1]).all()
        return render_template('user/profile.html', user=valid[3], profile=user_data, recipes=recipe)
    else:
        return render_template("error.html", error=PassiveControls.ErrMsg.access)


@user.route('/edit/profile', methods=["POST", "GET"])
def edit_profile():
    valid = PassiveControls.validation()
    if valid[0] and valid[2] == "user":
        user = User.query.get_or_404(valid[1])
        form = UpdateProfileForm()
        if request.method == "POST":
            if form.image.data:
                image_file = PassiveControls.save_file(form.image.data)
                user.profile_pic = image_file
            user.name = form.name.data
            user.username = form.username.data
            user.email = form.email.data
            db.session.commit()
            return redirect(url_for('user.profile'))
        elif request.method == "GET":
            form.name.data = user.name
            form.username.data = user.username
            form.email.data = user.email
            form.designation.data = user.designation
            return render_template('user/edit_profile.html', user=valid[3], form=form)
    else:
        return render_template("error.html", error=PassiveControls.ErrMsg.access)


@user.route('/password/change', methods=["POST", "GET"])
def change_password():
    valid = PassiveControls.validation()
    if valid[0] and valid[2] == "user":
        form = ChangePasswordForm()
        users = User.query.get_or_404(valid[1])
        if form.validate_on_submit():
            hashed_pass = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            users.password = hashed_pass
            db.session.commit()
            return redirect(url_for('user.index'))
        return render_template('user/change_password.html', user=valid[3], users=users, form=form)
    else:
        return render_template("error.html", error=PassiveControls.ErrMsg.access)


@user.route('/chefs')
def cooks():
    valid = PassiveControls.validation()
    if valid[0] and valid[2] == "user":
        page = request.args.get('page', 1, type=int)
        users = User.query.filter_by(type="user").paginate(page=page, per_page=5)
        return render_template('user/cooks.html', user=valid[3], users=users)
    else:
        return render_template("error.html", error=PassiveControls.ErrMsg.access)


@user.route('/chef/<int:user_id>')
def user_profile(user_id):
    valid = PassiveControls.validation()
    if valid[0] and valid[2] == "user":
        user_data = User.query.get_or_404(user_id)
        recipe = Recipe.query.filter_by(created_by=valid[1]).all()
        return render_template('user/user_profile.html', user=valid[3], profile=user_data, recipes=recipe)
    else:
        return render_template("error.html", error=PassiveControls.ErrMsg.access)


@user.route('/ingredients')
def ingredients():
    valid = PassiveControls.validation()
    if valid[0] and valid[2] == "user":
        page = request.args.get('page', 1, type=int)
        ingredient = Ingredient.query.paginate(page=page, per_page=6)
        return render_template('user/ingredients.html', user=valid[3], ingredients=ingredient)
    else:
        return render_template("error.html", error=PassiveControls.ErrMsg.access)


@user.route('/publish', methods=["POST", "GET"])
def publish_recipe():
    valid = PassiveControls.validation()
    if valid[0] and valid[2] == "user":
        form = RecipeForm()
        if form.validate_on_submit():
            if form.image.data:
                image_file = PassiveControls.save_file(form.image.data)
            recipe = Recipe(title=form.title.data, description=form.description.data,time=form.time.data,
                            servings=form.servings.data, ingredients=form.ingredients.data, image=image_file,
                            approval="-1", status="0", created_by=valid[1])
            db.session.add(recipe)
            db.session.commit()
            flash("Recipe has been published, please wait till its approved by our team.", "success")
            return redirect(url_for('user.index'))
        return render_template('user/publish.html', user=valid[3], form=form)
    else:
        return render_template("error.html", error=PassiveControls.ErrMsg.access)


@user.route('/recipes')
def recipes():
    valid = PassiveControls.validation()
    if valid[0] and valid[2] == "user":
        page = request.args.get('page', 1, type=int)
        recipe = Recipe.query.filter_by(approval=-1 and 1).paginate(page=page, per_page=5)
        return render_template('user/recipes.html', user=valid[3], recipes=recipe)
    else:
        return render_template("error.html", error=PassiveControls.ErrMsg.access)


@user.route('/recipes/own')
def my_recipes():
    valid = PassiveControls.validation()
    if valid[0] and valid[2] == "user":
        recipe = Recipe.query.filter_by(created_by=valid[1]).all()
        return render_template('user/my_recipes.html', user=valid[3], recipes=recipe)
    else:
        return render_template("error.html", error=PassiveControls.ErrMsg.access)


@user.route('/recipe/<int:recipe_id>')
def single_recipe(recipe_id):
    valid = PassiveControls.validation()
    if valid[0] and valid[2] == "user":
        recipe = Recipe.query.get_or_404(recipe_id)
        featured = Recipe.query.filter_by(status=1 and 2)
        ingredient = recipe.ingredients.split(',')
        return render_template('user/single.html', user=valid[3], recipe=recipe, featured=featured, ingredients=ingredient)
    else:
        return render_template("error.html", error=PassiveControls.ErrMsg.access)


@user.route('/recipe/edit/<int:recipe_id>', methods=["POST", "GET"])
def edit_recipe(recipe_id):
    valid = PassiveControls.validation()
    recipe = Recipe.query.get_or_404(recipe_id)
    if valid[0] and valid[2] == "user" and valid[1] == recipe.created_by:
        form = RecipeForm()
        if form.validate_on_submit():
            if form.image.data:
                image_file = PassiveControls.save_file(form.image.data)
                recipe.image = image_file
            recipe.title = form.title.data
            recipe.description = form.description.data
            recipe.time = form.time.data
            recipe.servings = form.servings.data
            recipe.ingredients = form.ingredients.data
            db.session.commit()
            flash('Recipe has been edited!', 'success')
            return redirect(url_for('user.my_recipes'))
        elif request.method == "GET":
            form.title.data = recipe.title
            form.description.data = recipe.description
            form.time.data = recipe.time
            form.servings.data = recipe.servings
            form.ingredients.data = recipe.ingredients
            return render_template('user/edit_recipe.html', user=valid[3], form=form)
    else:
        return render_template("error.html", error=PassiveControls.ErrMsg.access)


@user.route('/recipe/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    valid = PassiveControls.validation()
    if valid[0] and valid[2] == "user":
        recipe = Recipe.query.get_or_404(recipe_id)
        if recipe.created_by == valid[1]:
            db.session.delete(recipe)
            db.session.commit()
            flash("Recipe has been deleted!", "info")
        else:
            flash("You don't have access to delete this recipe!", "info")
        return redirect(url_for('user.my_recipes'))
    else:
        return render_template("error.html", error=PassiveControls.ErrMsg.access)


@user.route('/save/<int:recipe_id>')
def save_recipe(recipe_id):
    valid = PassiveControls.validation()
    if valid[0] and valid[2] == "user":
        save = Saved( user_id=valid[1], recipe_id=recipe_id)
        db.session.add(save)
        db.session.commit()
        flash("Recipe has been saved!", "info")
        return redirect(url_for('user.saved'))
    else:
        return render_template("error.html", error=PassiveControls.ErrMsg.access)


@user.route('/saved')
def saved():
    valid = PassiveControls.validation()
    if valid[0] and valid[2] == "user":
        saved_recipe = Saved.query.filter_by(user_id=valid[1]).all()
        return render_template('user/saved.html', user=valid[3], saves=saved_recipe)
    else:
        return render_template("error.html", error=PassiveControls.ErrMsg.access)


@user.route('/save/remove/<int:save_id>')
def remove_saved(save_id):
    valid = PassiveControls.validation()
    if valid[0] and valid[2] == "user":
        save = Saved.query.get_or_404(save_id)
        if save.user_id == valid[1]:
            db.session.delete(save)
            db.session.commit()
            flash("Saved Recipe has been removed!", "info")
        else:
            flash("You don't have access to remove this recipe!", "info")
        return redirect(url_for('user.saved'))
    else:
        return render_template("error.html", error=PassiveControls.ErrMsg.access)


