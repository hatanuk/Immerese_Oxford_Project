# WX library for GUI building
import wx

# General libraries
from re import match
import io
from os import environ, getcwd

# Google libraries for Cloud Vision
from google.cloud import vision

#Gets the JSON API file with Google Cloud credentials  [Make sure it's named vision_api.json and in the same directory]
environ["GOOGLE_APPLICATION_CREDENTIALS"]= (getcwd()) + "\\vision_api.json"




#Creates Main Frame

class myFrame(wx.Frame):



    def __init__(self, parent, title):
        super(wx.Frame, self).__init__(parent, title=title, size=(600,600), style = (wx.DEFAULT_FRAME_STYLE) &  ~ (wx.RESIZE_BORDER|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX))  
        self.maxWidth = 275
        self.client = vision.ImageAnnotatorClient()
        self.pathImage = None
        self.initUI()
        
        

    def initUI(self):
        
        #MENU ZONE

        # MAIN Menu Bar
        menuBar = wx.MenuBar()
        
        

        # FILE Menu
        fileMenu = wx.Menu()
        newItem = wx.MenuItem(fileMenu, id=wx.ID_NEW, text="&New\tCtrl+N", kind=wx.ITEM_NORMAL)
        fileMenu.Append(newItem)

        openItem = wx.MenuItem(fileMenu, id=wx.ID_OPEN, text="&Open\tCtrl+O", kind=wx.ITEM_NORMAL)
        fileMenu.Append(openItem)

        quitItem = wx.MenuItem(fileMenu, id=wx.ID_EXIT, text="&Quit\tCtrl+Q", kind=wx.ITEM_NORMAL)
        fileMenu.Append(quitItem)

        self.Bind(wx.EVT_MENU, self.onNew, newItem)
        self.Bind(wx.EVT_MENU, self.onOpen, openItem)
        self.Bind(wx.EVT_MENU, self.onQuit, quitItem)


        # PROCESS Menu

        processMenu = wx.Menu()
        textItem = wx.MenuItem(processMenu, id=wx.ID_ANY, text="&Text\tCtrl+T", kind=wx.ITEM_NORMAL)
        processMenu.Append(textItem)

        imageItem = wx.MenuItem(processMenu, id=wx.ID_ANY, text="&Image\tCtrl+I", kind=wx.ITEM_NORMAL)
        processMenu.Append(imageItem)

        self.Bind(wx.EVT_MENU, self.onText, textItem)
        self.Bind(wx.EVT_MENU, self.onImage, imageItem)

        # INFO Menu
        infoMenu = wx.Menu()
        aboutItem = wx.MenuItem(infoMenu, id=wx.ID_ANY, text="&About", kind=wx.ITEM_NORMAL)
        infoMenu.Append(aboutItem)

        self.Bind(wx.EVT_MENU, self.onAbout, aboutItem)
        
        

        # Appending to Menu Bar
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(processMenu, "&Process")
        menuBar.Append(infoMenu, "&Info")

        self.SetMenuBar(menuBar)


        self.Show(True)

        #---------------SLIDER PANEL CREATION-----------------
        self.sliderPanel = wx.Panel(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size= (600, 75), style=wx.TAB_TRAVERSAL, name = "Text Entry")
        self.sliderPanel.SetBackgroundColour((230, 230, 230))
        self.sliderPanel.Show(True)

        #----------------TEXT PANEL CREATION---------------------

        self.textPanel = wx.Panel(self, id=wx.ID_ANY, pos=(0, 75), size= (600, 250), style=wx.TAB_TRAVERSAL, name = "Text Entry")
        self.textPanel.SetBackgroundColour((240, 240, 240))
        self.textPanel.Show(True)

        #--------------------IMAGE PANEL CREATION--------------------------
        self.imagePanel= wx.Panel(self, id=wx.ID_ANY, pos=(0, 75), size= (600, 500), style=wx.TAB_TRAVERSAL, name = "Text Entry")
        self.imagePanel.SetBackgroundColour((240, 240, 240))
        self.imagePanel.Show(False)

        #-----------------OUTPUT PANEL CREATION--------------

        self.outputPanel= wx.Panel(self, id=wx.ID_ANY, pos=(0, 320), size= (600, 300), style=wx.TAB_TRAVERSAL, name = "Text Entry")
        self.outputPanel.SetBackgroundColour((240, 240, 240))
        self.outputPanel.Show(True)


        #SLIDER PANEL CONTENT
        
        # Slider between Text & Image
        self.panelSlider = wx.Slider(self.sliderPanel, id=wx.ID_ANY, value=0, minValue=0, maxValue=1, pos=(240, 25), size=(120, 25), style=wx.SL_HORIZONTAL,validator=wx.DefaultValidator, name="Test")
        self.panelSlider.SetForegroundColour((0, 0 ,0))
        self.panelSlider.SetBackgroundColour((25, 189, 255))
        self.Bind(wx.EVT_SCROLL, self.onSlider, self.panelSlider) 
        
        # "Text" Label
        panelText1 = wx.StaticText(self.sliderPanel, -1, "Text", pos=(200, 30), size=(30, 30))
        self.panelFont = wx.Font(10, wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_NORMAL, weight = 1000)
        panelText1.SetFont(self.panelFont)
        
        # "Image" Label
        panelText2 = wx.StaticText(self.sliderPanel, -1, "Image", pos=(367, 30), size=(30, 30))
        panelText2.SetFont(self.panelFont)
        
        # TEXT PANEL CONTENT
        
        # Label for textbox
        text1 = wx.StaticText(self.textPanel, -1, "Number plate text:", pos=(75, 50), size=(275, 50))
        self.font1 = wx.Font(20, wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_NORMAL, weight = 1000)
        text1.SetFont(self.font1)


        # Textbox with string entry
        self.textbox1 = wx.TextCtrl(self.textPanel, wx.ID_ANY, value="", pos=(75, 100), size=(275, 50), style=0)
        self.textbox1.SetHint("Enter registration here...")
        self.font2 = wx.Font(15, wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_NORMAL, weight = 500)
        self.textbox1.SetFont(self.font2)
        self.textbox1.SetForegroundColour((100, 100, 100))
        self.textbox1.SetMaxLength(8)
        
        self.textbox1.Bind(wx.EVT_TEXT, self.onTextChange)


       
        # OK Button for text entry
        self.button1 = wx.Button(self.textPanel, wx.ID_ANY, label="OK", pos=(360, 100), size=(50, 50))
        self.button1.SetFont(self.font1)
        self.button1.SetBackgroundColour((25, 189, 255))
        self.button1.SetForegroundColour((255, 255, 255))
        self.Bind(wx.EVT_BUTTON, self.onClickOK, self.button1)
        


        # OUTPUT PANEL CONTENT
        
        # Label for output box
        text2 = wx.StaticText(self.outputPanel, -1, "Results:", pos=(75, 0), size=(275, 50))
        text2.SetFont(self.font1)

        # Uneditable text box for output
        self.textbox2 = wx.TextCtrl(self.outputPanel, wx.ID_ANY, value="Results will appear here", pos=(75, 45), size=(335, 100), style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_NO_VSCROLL )
        self.textbox2.SetFont(self.font2)
        self.textbox2.SetForegroundColour((100, 100, 100))
        self.textbox2.Disable()
       

        # IMAGE PANEL CONTENT
        
        # Label for image
        text3 = wx.StaticText(self.imagePanel, -1, "Number plate image:", pos=(75, 50), size=(275, 50))
        text3.SetFont(self.font1)
        
        # Label for image file name
        self.text4 = wx.StaticText(self.imagePanel, -1, "", pos=(360, 210), size=(75, 30), style = wx.ST_ELLIPSIZE_END)
        self.text4.SetFont(self.panelFont)
    
        self.text4.Show(True)
        
        # Blank image slate
        img = wx.Image(275, 125)
        img.Replace(0, 0, 0, 255, 255, 255)
        self.imageCtrl = wx.StaticBitmap(self.imagePanel, id=wx.ID_ANY, bitmap=wx.NullBitmap, pos=(75, 100), size=(0, 0))
        self.imageCtrl.SetBitmap(wx.Bitmap(img))
        
        # OK button for image
        self.button2 = wx.Button(self.imagePanel, wx.ID_ANY, label="OK", pos=(360, 100), size=(50, 50))
        self.button2.SetFont(self.font1)
        self.button2.SetBackgroundColour((25, 189, 255))
        self.button2.SetForegroundColour((255, 255, 255))
        self.Bind(wx.EVT_BUTTON, self.onImage, self.button2)

       

    #MENU METHOD ZONE

    def onNew(self, event):
        self.reset()
        

    def onOpen(self, event):
        dlg = wx.FileDialog(self, message="Select an image", defaultDir="", defaultFile= "", wildcard ="", style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
           self.pathImage = dlg.GetPath()
           fileImage = dlg.GetFilename() 
           img = wx.Image(self.pathImage, wx.BITMAP_TYPE_ANY)
           W = img.GetWidth()
           H = img.GetHeight()
          
           if W != self.maxWidth:
                coefficient = self.maxWidth / W
                NewW = int(coefficient * W)
                NewH = int(coefficient * H)
                aspectRation = NewW/ NewH
                if NewH > 125:
                    NewH = 125
                    #if aspectRation > 1:
                        #NewH = 125 / aspectRation
                img.Rescale(NewW, NewH)

           self.imageCtrl.SetBitmap(wx.Bitmap(img))
           self.displayImageName(fileImage, NewH)
           

        dlg.Destroy()

    def onQuit(self, event):
        self.Close()

    def onText(self, event):
        self.textPanel.Show(True)
        self.imagePanel.Show(False)
        self.onClickOK(None)
     
    #-----------------------------
    
    def onSlider(self, event):
        value = self.panelSlider.GetValue()
        if value == 0:
            
            self.textPanel.Show(True)
            self.imagePanel.Show(False)
        else:
            self.textPanel.Show(False)
            self.imagePanel.Show(True)

    


    def reset(self):
        #make text default
        self.printOutput("Results will appear here")
        self.clearInput(self.textbox1)
        #clear image
        img = wx.Image(275, 125)
        img.Replace(0, 0, 0, 255, 255, 255)
        self.imageCtrl.SetBitmap(wx.Bitmap(img))
        self.text4.Show(False)
  

    #ABOUT popup
    def onAbout(self, event):

        #Creation of ABOUT page

        self.aboutDialog = wx.Dialog(self, id=wx.ID_ANY, title="About", pos=wx.DefaultPosition, size=(400, 400), style=wx.DEFAULT_DIALOG_STYLE, name="")

        dialogImage = wx.Image("C:\\Users\\Lordf\\OneDrive\\Desktop\\Project_Immerse\\logo.png", wx.BITMAP_TYPE_ANY)
        dialogImage.Rescale(80, 80)

        dialogBitmap = wx.StaticBitmap(self.aboutDialog, id=wx.ID_ANY, bitmap=wx.NullBitmap, pos=(148, 20))
        dialogBitmap.SetBitmap(wx.Bitmap(dialogImage))

        dialogTitle = wx.StaticText(self.aboutDialog, -1, "Identifier for Standard Number Plates", pos=(43, 120), size=(50, 30))
        fontTitle = wx.Font(13, wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_NORMAL, weight = 1000)
        dialogTitle.SetFont(fontTitle)

        wx.StaticText(self.aboutDialog, -1, "A simple application capable of identifying and calculating date of manufactoring of cars with standard UK license plates using Google Vision. Created as part of the 2022 Immerse Education Computer Science course.", pos=(20, 150), size=(340, 250))

        dialogThankYou = wx.StaticText(self.aboutDialog, -1, "Thank you for visiting.", pos=(43, 275), size=(50, 30))
        dialogThankYou.SetFont(self.font1)

        #------------------------------------------------------#

        try:
        
            if self.aboutDialog.ShowModal() == wx.ID_OK:
                # do something here
                print('Hello')
            else:
                pass
                # handle dialog being cancelled or ended by some other button
        finally:
            self.aboutDialog.Destroy()

            

    #When you click the OK button (text)
    def onClickOK(self, event):
        numPlate = self.getText()
        self.extractYear(numPlate)

    #When image run event is called
    def onImage(self, event):
        self.textPanel.Show(False)
        self.imagePanel.Show(True)
        self.processImage()

    #Processes the image
    def processImage(self):
        print(self.pathImage)
        if self.pathImage is not None:
            result = self.detect_text(self.pathImage, self.client)
            fullNumberPlate = result[0].description
            coordinatePoly = result[0].bounding_poly.vertices
            coordinateVertices =  (['({},{})'.format(vertex.x, vertex.y)
                for vertex in coordinatePoly])
            print(fullNumberPlate)
            self.extractYear(fullNumberPlate)
            self.textbox1.SetValue(fullNumberPlate)
            self.drawBox(coordinateVertices)
        else:
            self.printOutput("No image is uploaded")
    
    #Draws box around license plate (unused)

    #def drawBox(self, coordinateVertices):
        #dc = wx.MemoryDC(self.bmp)
        #dc.SetPen(wx.Pen('green', 5, wx.SOLID))
        #dc.SetBrush(wx.Brush('green', wx.TRANSPARENT))


       
    #Gets text from input texbox
    def getText(self):
        return self.textbox1.GetValue()

    
    #Puts text into output textbox
    def printOutput(self, anyText):
        self.textbox2.SetValue(anyText)
        
    #Label for image file name    
    def displayImageName(self, name, height):
        dc = wx.ScreenDC()
        dc.SetFont(self.panelFont)
        self.text4.SetLabel("{}".format(name))
        self.text4.Ellipsize(name, dc= dc, mode = wx.ELLIPSIZE_END, maxWidth= 200, flags = wx.ELLIPSIZE_FLAGS_DEFAULT)
        self.text4.SetSize(200, 30)
        self.text4.Show(True)  

    ## Functions for the manufactoring date calculation

    def checkYear(self, inp):
        half = "first half"
        if inp >= 5:
            inp = inp - 5
            half = "second half"
        return inp, half
    
    def getNum(self, inp):
        num = int(self.replaceNum2Letter(inp[2:4]))
        num1 = num // 10
        num2 = num % 10
        return num1, num2

    def replaceNum2Letter(self, inputString):
        inputString.replace("o", "0")
        inputString.replace("O", "0")
        inputString.replace("I", "1")
        inputString.replace("l", "1")
        inputString.replace("s", "5")
        inputString.replace("S", "5")
        return inputString


    def calYear(self, inp1, inp2, origin):
        year = inp1 * 10 + inp2 + origin
        return year
        

    def createMessageYear(self, year, half):
        return ("This car is registered in {} \nin the {} of the year" .format(year, half))
    

    def extractYear(self, numPlate):

        if len(numPlate) == 7:
            numPlate = numPlate[:4] + " " + numPlate[4:]
        elif len(numPlate) > 8:
                self.printOutput("Please make sure there is no other visible text in the image apart from the number plate")
                return

        if match('^[a-zA-Z0-9 ]*$', numPlate):
            if len(numPlate) == 8:
                try:
    
                    [a1, a2] = self.getNum(numPlate)
                    print(numPlate, a1, a2)
                    [a1, half] = self.checkYear(a1)
                    year = self.calYear(a1, a2, 2000)
                    #puts the text in output
                    self.printOutput(self.createMessageYear(year, half))
    
                except:
                        # puts the text in output
                        self.printOutput(("The 3rd and 4th digits must be integers"))
            
        
            else:
                #puts the text in output
                self.printOutput("Standard UK license plates must have 8 characters (including space)")
        else:
            self.printOutput("Number plate contains illegal characters")
    
    # GOOGLE CLOUD API

    def detect_text(self, path,client):
        
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        response = client.text_detection(image=image)
        texts = response.text_annotations
        print('Texts:')

        for text in texts:
            print('\n"{}"'.format(text.description))

            vertices = (['({},{})'.format(vertex.x, vertex.y)
                        for vertex in text.bounding_poly.vertices])

            print('bounds: {}'.format(','.join(vertices)))

        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))
        return texts
  

app = wx.App()


frm = myFrame(None, title = "ISNP")

frm.Show()
app.MainLoop()
