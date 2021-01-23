from  PySide2.QtWidgets  import * 
from  PySide2.QtUiTools  import  QUiLoader 
from  PySide2.QtCore  import  QFile
from  matplotlib.backends.backend_qt5agg  import  ( 
        FigureCanvas ,  NavigationToolbar2QT  as  NavigationToolbar )
import warnings
warnings.filterwarnings("ignore")
from  matplotlib.figure  import  Figure
import  numpy  as  np 

#MainWidget 
class  MainWidget ( QWidget ):
    
    def  __init__ ( self ):



        QWidget . __init__ ( self )
        
        #loading designer file
        designer_file  =  QFile ( "gui.ui" ) 
        designer_file . open ( QFile . ReadOnly )
        loader  =  QUiLoader () 
        loader . registerCustomWidget ( MplWidget ) 
        self . ui  =  loader . load ( designer_file ,  self )
        designer_file . close ()

        #setting window name and layout
        self . setWindowTitle ( "Function plotter" )
        grid_layout  =  QGridLayout () 
        grid_layout . addWidget ( self . ui ) 
        self . setLayout ( grid_layout )

        #plot button calls the update graph function to plot upon clicking 
        self . ui . plot . clicked . connect ( self . update_graph )
        

    
    def  update_graph ( self):

        f=self.ui.lineEdit.text() #assigning the function to be the lineedit text
        plot=Plotter() 
        f=plot.inputCorrection(f) #calling the inputcorrection function to process input 
          

        self . ui . MplWidget . canvas . axes . clear () #comment this if you want multiple plots on the same figure

        try:
            xMin=float(self.ui.lineEdit_2.text()) #assigning x miminum value
            xMax=float(self.ui.lineEdit_3.text()) #assigning x maximum value
            x = np.linspace(xMin,xMax , 100)    

            self . ui . MplWidget . canvas . axes . plot ( x ,  eval(f) ) #plotting x versus f(x)

        except NameError:
            self.nameError() #handling name errors such as undefined variables and calling the warning function
             
        
        except SyntaxError:
            self.syntaxError() #handling syntax errors such and calling the warning function


        except:
            self.error()    #handling any unaccounted errors and calling the warning function





        self . ui . MplWidget . canvas . draw ()
        
    #dispalying the warning messeage
    def nameError(self):
        QMessageBox.warning(self, "error", "Please make sure that your input is only function of x and e(x),ln(x),etc has parenthesis ")

    def syntaxError(self):
            QMessageBox.warning(self, "error", "Please enter a valid syntax i.e enter 2*x not 2x")


    def error(self):
            QMessageBox.warning(self, "error", "oops something went wrong, please enter a valid input")






#Matplotlib widget
class  MplWidget ( QWidget ):
    
    
    def  __init__ ( self ,  parent  =  None ):
        
        QWidget . __init__ ( self ,  parent )
        
        self . canvas  =  FigureCanvas ( Figure ())
        
        vertical_layout  =  QVBoxLayout () 
        vertical_layout . addWidget ( self . canvas )  
        vertical_layout . addWidget ( NavigationToolbar ( self . canvas ,  self )) 
        
        self . canvas . axes  =  self . canvas . figure . add_subplot ( 111 ) 
        self . setLayout ( vertical_layout )    



class Plotter:
    
    def __init__(self):
       pass
    
    

    #putting the power in python syntax
    def power(self,f):
        f=f.replace("^","**") #this replaces every "^" in a string to "**"
        return f
        
    #putting e,ln,sin,cos and tan respectively in numpy syntax
    
    def numpyExp(self,f):
        
        p1=f.find("e**(")+4 #position of what's after the opening parentheses
        p2=f.find(")",p1)   #position of the closing parentheses
        x=f[p1:p2]          #the string between the parentheses
        f=f.replace("e**({})".format(x),"np.exp({})".format(x)) #this replaces every e**(x) to numpy syntax
        return f


    def numpyLn(self,f):
        p1=f.find("ln(")+3  #position of what's after the opening parentheses
        p2=f.find(")",p1)   #position of the closing parentheses
        x=f[p1:p2]          #the string between the parentheses
        f=f.replace("ln({})".format(x),"np.log({})".format(x)) #this replaces every ln(x) to numpy syntax
        return f

    def numpySin(self,f):
        p1=f.find("sin(")+4 #position of what's after the opening parentheses
        p2=f.find(")",p1)   #position of the closing parentheses
        x=f[p1:p2]          #the string between the parentheses
        f=f.replace("sin({})".format(x),"np.sin(({})* np.pi / 180)".format(x)) #this replaces every sin(x) to numpy syntax in radian
        
        return f
        
        


    def numpyCos(self,f):
        p1=f.find("cos(")+4 #position of what's after the opening parentheses
        p2=f.find(")",p1)   #position of the closing parentheses
        x=f[p1:p2]          #the string between the parentheses
        f=f.replace("cos({})".format(x),"np.cos(({})* np.pi / 180)".format(x)) #this replaces every cos(x) to numpy syntax in radin
        return f
        
        



    def numpyTan(self,f):
        p1=f.find("tan(")+4 #position of what's after the opening parentheses
        p2=f.find(")",p1)   #position of the closing parentheses
        x=f[p1:p2]          #the string between the parentheses
        f=f.replace("tan({})".format(x),"np.tan(({})* np.pi / 180)".format(x)) #this replaces every tan(x) to numpy syntax in radian
        
        return f
        
    #calling all input correction functions

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
