from fasthtml.common import *
import re

db=database('data/test.db')

class User: id: int; dmcl_name: str; p_dmcl_name: str; dob: str;
class Domicile: id: int; dmcl_name:str; locality: str; state: str; nation: str
class Pat_Domicile: id: int; p_dmcl_name:str; locality: str; state: str; nation: str
class DoB: id: int; dob: str; dob_partial: str; dob_full: str

app = FastHTML(...)
rt = app.route()

@app.get('/')
def homepage(): 
    return Form(hx_post='/submit', hx_target='#submit-btn-container', hx_swap='outerHTML')(

                Div(hx_target='this', hx_swap='outerHTML')(
                    Label(_for='name')('Name'),
                    Input(type='text', name='name', id='name', hx_post='/name')),
                
                Div(hx_target="this",hx_swap="outerHTML")(
                    Label(_for='domicile')('Place of birth (domicile)'),
                    Input(type='search', name='domicile', id='domicile', hx_trigger="input changed delay:500ms search", hx_target="#domicile_results", hx_indicator=".htmx-indicator",
                           hx_post='/domicile')),

                # Div(hx_target="this", hx_swap="outerHTML")(
                #     Label(_for="p_domicile")("Father's domicile"),
                #     Input(type="search", name="p_domicile", id="p_domicile", hx_post="/p_domicile")),
               
                # Div(hx_target="this",hx_swap="outerHTML")(
                #     Label(_for='dob')('Date of birth'),
                #     Input(type='text', name='dob', id='dob', hx_post='/dob')),
                
                Div(id='submit-btn-container')(
                    Button(type='submit', id='submit-btn',)('Submit')))

@app.post('/name')
def contact_name(name: str): return inputTemplate('Name,', 'name', name, validate_name(name))

@app.post('/domicile')
def contact_domicile(domicile: str): return inputTemplate('Place of birth (domicile)', 'domicile', domicile, validate_domicile(domicile))

@app.post('/p_domicile')
def contact_p_domicile(p_domicile: str): return inputTemplate("Father's domicile.", 'p_domicile', p_domicile, validate_p_domicile(p_domicile))

@app.post('/dob')
def contact_dob(dob: str): return inputTemplate('Date of birth', 'dob', dob, validate_dob(dob))

@app.post('/submit')
def contact_submit(name: str, domicile: str, p_domicile: str, dob: str):
    errors = {'name': validate_name(name),
            'domicile': validate_domicile(domicile),
            'p_domicile': validate_p_domicile(p_domicile),
            'dob': validate_dob(dob)
             }
    errors = {k: v for k, v in errors.items() if v is not None}
    # Return Button with error message if they exist
    return Div(id='submit-btn-container')(
        Button(type='submit', id='submit-btn', hx_post='/submit', hx_target='#submit-btn-container', hx_swap='outerHTML')('Submit'),
        *[Div(error, style='color: red;') for error in errors.values()])

def validate_name(name: str):
    regex = r'\b[A-Za-z]+[A-Za-z]\b'
    if name == "":  return "Empty."
    # If no errors, return None (default of python)

def validate_domicile(domicile: str):
    regex = r'\b[A-Za-z]\b'
    if domicile == "": return "Empty."

def validate_p_domicile(p_domicile: str):
    regex = r'\b[A-Za-z]\b'
    if p_domicile == "": return "Empty."

def validate_dob(dob: str):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if dob == "": return "Empty."

def inputTemplate(label, name, val, errorMsg=None, input_type='text'):
    # Generic template for replacing the input field and showing the validation message
    return Div(hx_target='this', hx_swap='outerHTML', cls=f"{errorMsg if errorMsg else 'Valid'}")(
               Label(label), # Creates label for the input field
               Input(name=name,type=input_type,value=f'{val}',hx_post=f'/{name.lower()}'), # Creates input field
               Div(f'{errorMsg}', style='color: red;') if errorMsg else None) # Creates red error message below if there is an error
