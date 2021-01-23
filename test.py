
from main import*
def test_power():
    f="x^2"
    assert Plotter().power(f)=="x**2"
    
def test_exp():
    f="e**(2*x+2)" # the power is written as ** not ^ because it should be already replace from the power func
    assert Plotter().numpyExp(f)=="np.exp(2*x+2)" 

def test_ln():
    f="ln(9*x)"
    assert Plotter().numpyLn(f)=="np.log(9*x)"



def test_sin():
    f="sin(x-90)"
    assert Plotter().numpySin(f)=="np.sin((x-90)* np.pi / 180)"


def test_cos():
    f="cos(x+180)"
    assert Plotter().numpyCos(f)=="np.cos((x+180)* np.pi / 180)"
    
def test_tan():
    f="tan(x+90)"
    assert Plotter().numpyTan(f)=="np.tan((x+90)* np.pi / 180)"


def test_f():
    f="x^3+2*x-e^(3*x)-ln(x)"
    assert Plotter().inputCorrection(f)=="x**3+2*x-np.exp(3*x)-np.log(x)"





        




        
