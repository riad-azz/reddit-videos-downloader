from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Regexp


class FetchForm(FlaskForm):
    url = StringField(
        "URL",
        validators=[
            InputRequired(message="Post URL is required"),
            Regexp(
                r"^https?://(?:www\.)?reddit\.com/r/\w+/comments/\w+/",
                message="Invalid Reddit post URL",
            ),
        ],
    )
