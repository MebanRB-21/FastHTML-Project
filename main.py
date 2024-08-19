from fasthtml.common import *
import re

db = database('data/test.db')
app, rt = fast_app()

@app.get('/')
def form():
    return Form(hx_post='/submit', hx_target="#submit-btn-container", hx_swap='outerHTML')(
                Div(hx_target='this',hx_swap='outerHTML')(
                    Label(_for='name')('Enter your full name.'),
                    Input(type='text', name='name', id='name', hx_post='/name')),
                Div(hx_target='this',hx_swap='outerHTML')(
                    Label(_for='domicile')('Enter your place of birth (domicile).'),
                    Input(type='text', name='domicile', id='domicile', hx_post='/domicile')),
                Div(hx_target='this',hx_swap='outerHTML')(
                    Label(_for='paternal_domicile')("Enter your father's domicile."),
                    Input(type='text', name='paternal_domicile', id='paternal_domicile', hx_post='/paternal_domicile')),
                Div(hx_target='this',hx_swap='outerHTML')(
                    Label(_for='dob')('Enter the date of birth.'),
                    Input(type='text', name='dob', id='dob',hx_post='/dob')),
                Div(id='submit-btn-container')(
                    Button(type='submit', id='submit-btn',)('Submit')))

@app.post('/name')
def contact_name(name: str): return inputTemplate('Enter your full name.','name', name, validate_name(name))

@app.post('/domicile')
def contact_domicile(domicile: str): return inputTemplate('Enter your place of birth (domicile).','domicile', domicile, validate_domicile(domicile))

@app.post('/paternal_domicile')
def contact_paternal_domicile(paternal_domicile: str): return inputTemplate("Enter your father's domicile.",'paternal_domicile', paternal_domicile, validate_paternal_domicile(paternal_domicile))
    
@app.post('/dob')
def contact_dob(dob: str): return inputTemplate('Enter the date of birth.','dob',dob, validate_dob(dob))

@app.post('/submit')
def contact_submit(name: str, dmcl: str, paternal_domicile: str, dob: str):
    errors={'full_name': validate_name(name),
            'domicile': validate_domicile(dmcl),
            'paternal_domicile': validate_paternal_domicile(paternal_domicile),
            'dob': validate_dob(dob) 
            }
    errors={i: j for i, j in errors.items() if j is not None}
    return Div(id='submit-btn-container')(
        Button(type='submit', id='submit-btn', hx_post='/submit', hx_target='#submit-btn-container', hx_swap='outerHTML')('Submit'),
        *[Div(error, style='color: red;') for error in errors.values()])

def validate_name(name: str):
    name_regex = r'\A[a-zA-Z]+'
    if name == "":  return "Field cannot be empty. Please enter your full name."

def validate_domicile(dmcl: str):
    dmcl_regex = r'\A[a-zA-Z]+'
    if dmcl == "":  return "Field cannot be empty. Please enter a domicile."

def validate_paternal_domicile(paternal_domicile: str):
    paternal_domicile_regex = r'\b[A-Za-z]+\b'
    if paternal_domicile == "":  return "Field cannot be empty. Please enter your father's domicile."

def validate_dob(dob: str):
    dob_regex = r'\b(0[1-9]|1[012])[-/.](0[1-9]|[12][0-9]|3[01])[-/.](19|20)+\b'
    if dob == "":  return "Field cannot be empty."


def inputTemplate(label, name, val, errorMsg=None, input_type='text'):
    return Div(hx_target='this', hx_swap='outerHTML', cls=f"{errorMsg if errorMsg else 'Valid'}")(
               Label(label),
               Input(name=name,type=input_type,value=f'{val}',hx_post=f'/{name.lower()}'),
               Div(f'{errorMsg}', style='color: red;') if errorMsg else None)