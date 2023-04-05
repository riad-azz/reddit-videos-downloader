from wtforms.validators import Email, Length, EqualTo, DataRequired

register_validators = {
    "username": (
        Length(min=2, max=30, message="Username must be between 2 to 30 characters."),
        DataRequired(),
    ),
    "email": (Email(), DataRequired()),
    "password": (Length(min=8), DataRequired()),
    "confirm_password": (
        EqualTo("password", message="Password confirmation does not match."),
        DataRequired(),
    ),
}

login_validators = {
    "username": (
        Length(min=2, max=30, message="Username must be between 2 to 30 characters."),
        DataRequired(),
    ),
    "password": (DataRequired(),),
}
