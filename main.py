from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from polynomial import Polynomial

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  
import numpy as np
import io
import base64

    
def get_coefficient_list(coefficients):
    coefficient_list = list(map(float, coefficients.split()))
    return coefficient_list


@app.get("/solve")
async def solve(request: Request, 
                coefficients,
                guess):
    coefficient_list, x = None, None
    try:
        coefficient_list = get_coefficient_list(coefficients)
        x = float(guess)
    except Exception as e:
        return {"error": repr(e)}
    p = Polynomial(coefficient_list)
    root = None
    try:
        root = p.newtons_method(x)
    except Exception as e:
        return {"error": repr(e)}
    return {"root": root}

@app.post("/plot")
async def main(request: Request,
               coefficients: str = Form(...),
               left_bound: str = Form(...),
               right_bound: str = Form(...)):
    fig = plt.figure()
    
    coefficient_list, left, right = None, None, None
    try:
        coefficient_list = get_coefficient_list(coefficients)
        left = float(left_bound)
        right = float(right_bound)
    except Exception as e:
        return {"error": repr(e)}
    
    p = Polynomial(coefficient_list)
    poly_string = str(p)
    
    # Get range of x coordinates over which graph will be plotted
    x = np.linspace(left, right, 100)
    y = p(x)
    
    #plot axis lines
    plt.axhline(y=0, color='black')
    plt.axvline(x=0, color='black')
    plt.grid()
    plt.plot(x, y)
    
    pngImage = io.BytesIO()
    fig.savefig(pngImage)
    pngImageB64String = base64.b64encode(pngImage.getvalue()).decode('ascii')
    
    return templates.TemplateResponse("plot.html", 
                                      {"request": request,
                                       "poly_string": poly_string,
                                       "picture": pngImageB64String})    
    
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("main.html", 
                                      {"request": request})    
    