# ------------------ PySide2 - Qt Designer - Matplotlib ------------------ 
from  PySide2.QtWidgets  import * 
from  PySide2.QtUiTools  import  QUiLoader 
from  PySide2.QtCore  import  QFile
from  matplotlib.backends.backend_qt5agg  import  ( 
        FigureCanvas ,  NavigationToolbar2QT  as  NavigationToolbar )

from  matplotlib.figure  import  Figure
import  numpy  as  np 
import  random


# ------------------ MplWidget ------------------ 
class  MplWidget ( QWidget ):
    
    
    def  __init__ ( self ,  parent  =  None ):
        
        QWidget . __init__ ( self ,  parent )
        
        self . canvas  =  FigureCanvas ( Figure ())
        
        vertical_layout  =  QVBoxLayout () 
        vertical_layout . addWidget ( self . canvas ) 
        vertical_layout . addWidget ( NavigationToolbar ( self . canvas ,  self ))
        
        self . canvas . axes  =  self . canvas . figure . add_subplot ( 111 ) 
        self . setLayout ( vertical_layout )    

# ------------------ MainWidget ------------------ 
class  MainWidget ( QWidget ):
    
    def  __init__ ( self ):



        QWidget . __init__ ( self )

        designer_file  =  QFile ( "gui.ui" ) 
        designer_file . open ( QFile . ReadOnly )
        loader  =  QUiLoader () 
        loader . registerCustomWidget ( MplWidget ) 
        self . ui  =  loader . load ( designer_file ,  self )

        designer_file . close ()
  
        self . setWindowTitle ( "Function plotter" )

        grid_layout  =  QGridLayout () 
        grid_layout . addWidget ( self . ui ) 
        self . setLayout ( grid_layout )

        self . ui . plot . clicked . connect ( self . update_graph )
        


    def  update_graph ( self):

        f=self.ui.lineEdit.text()
        plot=Plotter()
        f=plot.inputCorrection(f)
          

        self . ui . MplWidget . canvas . axes . clear () 

        try:
            xMin=float(self.ui.lineEdit_2.text())
            xMax=float(self.ui.lineEdit_3.text())
            x = np.linspace(xMin,xMax , 100)

            self . ui . MplWidget . canvas . axes . plot ( x ,  eval(f) ) 

        except NameError:
            self.nameError()
             
        
        except SyntaxError:
            self.syntaxError()


        except:
            self.error()





        self . ui . MplWidget . canvas . draw ()
        

    def nameError(self):
        QMessageBox.warning(self, "error", "Please make sure that your input is only function of x and e(x),ln(x),etc has parenthesis ")

    def syntaxError(self):
            QMessageBox.warning(self, "error", "Please enter a valid syntax i.e enter 2*x not 2x")


    def error(self):
            QMessageBox.warning(self, "error", "oops something went wrong, please enter a valid input")


class Plotter:
    
    def __init__(self):
       pass
    
    xMin=-10
    xMax=10


    def power(self,f):
        f=f.replace("^","**")
        return f
        

    def numpyExp(self,f):
        
        p1=f.find("e**(")+4
        p2=f.find(")",p1)
        x=f[p1:p2]
        f=f.replace("e**({})".format(x),"np.exp({})".format(x))
        return f


    def numpyLn(self,f):
        p1=f.find("ln(")+3
        p2=f.find(")",p1)
        x=f[p1:p2]
        f=f.replace("ln({})".format(x),"np.log({})".format(x))
        return f

    def numpySin(self,f):
        p1=f.find("sin(")+4
        p2=f.find(")",p1)
        x=f[p1:p2]
        f=f.replace("sin({})".format(x),"np.sin(({})* np.pi / 180)".format(x))
        
        return f
        
        


    def numpyCos(self,f):
        p1=f.find("cos(")+4
        p2=f.find(")",p1)
        x=f[p1:p2]
        f=f.replace("cos({})".format(x),"np.cos(({})* np.pi / 180)".format(x))
        return f
        
        



    def numpyTan(self,f):
        p1=f.find("tan(")+4
        p2=f.find(")",p1)
        x=f[p1:p2]
        f=f.replace("tan({})".format(x),"np.tan(({})* np.pi / 180)".format(x))
        
        return f
        

    def inputCorrection(self,f):
        f=self.power(f)
        
        f=self.numpyExp(f)
        f=self.numpyLn(f)
        f=self.numpySin(f)
        f=self.numpyCos(f)
        f=self.numpyTan(f)
        
        return f









app  =  QApplication ([]) 
window  =  MainWidget () 
window . show () 
app . exec_ ()
