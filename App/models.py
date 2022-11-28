from App import db, app


    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_pic = db.Column(db.String(20), nullable=False, default='default_user.jpg')
    password = db.Column(db.String(60), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    designation = db.Column(db.Text, nullable=False)

    ingredient = db.relationship('Ingredient', backref='ing_creator', lazy=True)
    recipes = db.relationship('Recipe', backref='recipe_creator', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.name}')"


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    details = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(20), nullable=False, default="default.jpg")
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Ingredient('{self.name}')"


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    time = db.Column(db.Integer, nullable=False)
    servings = db.Column(db.Integer, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(20), nullable=False, default="default.jpg")
    approval = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(12), nullable=False)

    saved = db.relationship('Saved', backref='saved_recipe', lazy=True)

    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Recipe('{self.title}')"


class Saved(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

    def __repr__(self):
        return f"Saved('{self.recipe_id}', '{self.user_id}')"


