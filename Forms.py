from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, DecimalField, validators, \
    ValidationError, IntegerField


class CreateItemForm(Form):
    name = StringField('Name: ', [validators.Length(min=1, max=150), validators.DataRequired()], default='')
    price = DecimalField('Price($): ', [validators.NumberRange(min=1), validators.DataRequired()], default=0, places=2)
    have = IntegerField('Amount we have in stock: ', [validators.NumberRange(min=1), validators.DataRequired()],
                        default=0)
    picture = StringField('Picture (link): ', [validators.Length(min=1, max=150), validators.DataRequired()],
                          default='')
    bio = TextAreaField('Item Description: ', [validators.DataRequired()], default='')


class BuyItemForm(Form):
    want = IntegerField('Purchasing Quantity: ', [validators.NumberRange(min=1), validators.DataRequired()], default=0)


class CheckoutForm(Form):
    # Could use user profiles instead
    address = StringField('Address: ', [validators.Length(min=1, max=150), validators.DataRequired()], default='')
    # Use Sting field as Postal Code needs to be saved as string as integer removes front 0 i.e 081456 = 81456
    postal_code = StringField('Postal Code: ', [validators.Length(min=6, max=6), validators.DataRequired()], default='')
