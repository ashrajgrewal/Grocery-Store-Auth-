from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    DateField,
    SelectField,
    SubmitField,
    FloatField,
    PasswordField,
)

from wtforms.validators import DataRequired, Length, URL, optional
from grocery_app.models import ItemCategory, GroceryStore


class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""

    title = StringField(
        "Store Title", validators=[DataRequired(), Length(min=3, max=80)]
    )
    address = StringField(
        "Store Address", validators=[DataRequired(), Length(min=3, max=200)]
    )
    submit = SubmitField("Submit")


class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""

    name = StringField("Item Name", validators=[DataRequired(), Length(min=3, max=80)])
    price = FloatField("Item Price", validators=[DataRequired()])
    category = SelectField("Category", choices=ItemCategory.choices())
    photo_url = StringField("Item Photo URL", validators=[URL(require_tld=True)])
    store = SelectField("Stores", query_factory=lambda: GroceryStore.query)
    submit = SubmitField("Submit")
