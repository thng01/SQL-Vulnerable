from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    SelectField,
    TextAreaField,
    IntegerField,
    SelectMultipleField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    ValidationError,
    EqualTo,
)
from App.models import (
    User,
    Ingredient,
)
from Controls import PassiveControls


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=8)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=13)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    image = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    type = SelectField('User Type', validators=[DataRequired()], choices=[('admin', 'Admin'), ('user', 'User')])
    designation = StringField('Job Designation', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username has been taken, Please use another one!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email has been taken, Please use another one!')


class UpdateProfileForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=13)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    image = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    designation = StringField('Job Designation', validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        session = PassiveControls.validation()
        user_data = User.query.get_or_404(session[1])
        if username.data != user_data.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username has been taken, Please use another one!')

    def validate_email(self, email):
        session = PassiveControls.validation()
        user_data = User.query.get_or_404(session[1])
        if email.data != user_data.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email has been taken, Please use another one!')


class IngredientForm(FlaskForm):
    name = StringField('Ingredient Name', validators=[DataRequired()])
    image = FileField('Ingredient Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    description = TextAreaField('Ingredient Details')
    submit = SubmitField('Submit')

    def validate_name(self, name):
        ing = Ingredient.query.filter_by(name=name.data).first()
        if ing:
            raise ValidationError('Ingredient has been added, Please add another one!')


class RecipeForm(FlaskForm):
    title = StringField('Recipe Name', validators=[DataRequired()])
    description = TextAreaField('Recipe Details', validators=[DataRequired()])
    time = IntegerField('Time Needed to Cook', validators=[DataRequired()])
    servings = IntegerField('Servings', validators=[DataRequired()])
    image = FileField('Dish Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    ingredients = StringField('Ingredients', validators=[DataRequired()])
    submit = SubmitField('Publish')


class ApproveRecipeForm(FlaskForm):
    approval = SelectField('Type', validators=[DataRequired()], choices=[('1', 'Approved'), ('0', 'Rejected')])
    status = SelectField('Featured As', validators=[DataRequired()], choices=[("1", "Editor's Pick"), ('2', 'Weekly Featured'), ('0', 'Normal')])
    submit = SubmitField('Submit')
    
    
class ChangePasswordForm(FlaskForm):
    password = PasswordField('Old Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    submit = SubmitField('Change Password')

class SearchForm(FlaskForm):
    keyword = StringField('')

