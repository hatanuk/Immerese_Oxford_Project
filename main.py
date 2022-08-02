# WX libraries
import wx

# Google vision api librraies
from google.cloud import vision
import io
client = vision.ImageAnnotatorClient()


def detect_text(path,client):
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

# Make Main Frame

class myFrame(wx.Frame):

    def __init__(self, parent, title):

        super(wx.Frame, self).__init__(parent, title=title, size=(1000,600))
        self.maxWidth = 500
        self.initUI()
        self.pathImage = None
        self.img = None

    def initUI(self):
        # Main menu bar
        menuBar = wx.MenuBar()
        
        # File menu and items
        fileMenu = wx.Menu()
        newItem = wx.MenuItem(fileMenu, id=wx.ID_NEW, text="&New\tCtrl+N", kind = wx.ITEM_NORMAL)
        fileMenu.Append(newItem)
        
        openItem = wx.MenuItem(fileMenu, id=wx.ID_OPEN, text="&Open\tCtrl+O", kind = wx.ITEM_NORMAL)
        fileMenu.Append(openItem)
       
        fileMenu.AppendSeparator()
        quitItem = wx.MenuItem(fileMenu, id=wx.ID_EXIT, text="&Quit\tCtrl+Q", kind = wx.ITEM_NORMAL)
        fileMenu.Append(quitItem)

        # File menu binds
        self.Bind(wx.EVT_MENU, self.onOpen, openItem)
        self.Bind(wx.EVT_MENU, self.onQuit, quitItem)        
        self.Bind(wx.EVT_MENU, self.onNew, newItem)

        # Run menu and items
        runMenu = wx.Menu()
        textItem = wx.MenuItem(runMenu, id=wx.ID_ANY, text="Text", kind = wx.ITEM_NORMAL)
        runMenu.Append(textItem)
        imageItem = wx.MenuItem(runMenu, id=wx.ID_ANY, text="Image", kind=wx.ITEM_NORMAL)
        runMenu.Append(imageItem)        

        # Run menu binds
        self.Bind(wx.EVT_MENU, self.onText, textItem)
        self.Bind(wx.EVT_MENU, self.onImage, imageItem)

        # Appending the menus
        menuBar.Append(fileMenu, '&File', )
        menuBar.Append(runMenu, '&Process')

        self.SetMenuBar(menuBar)
     
        # Panel
        panel = wx.Panel(self, id=wx.ID_ANY, pos=(1000, 1000), size = (1000, 1000))

        #Make the text above the textbox and set the font for it
        text1 = wx.StaticText(self, -1, "Enter number plate:", pos=(50, 50), size=(275, 50))
        self.font1 = wx.Font(20, wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_NORMAL, weight = 1000)
        text1.SetFont(self.font1)

        text2 = wx.StaticText(self, -1, "Number Plate Image:", pos=(450, 50), size=(275, 50))
        text2.SetFont(self.font1)

        #Make the textbox where number plate is entered
        self.textbox1 = wx.TextCtrl(self, wx.ID_ANY, value="", pos=(50, 125), size=(265, 50), style=0)
        self.textbox1.SetHint("Enter registration here...")
        self.font2 = wx.Font(15, wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_NORMAL, weight = 500)
        self.textbox1.SetFont(self.font2)
        self.textbox1.SetForegroundColour((166, 166, 166))

        img = wx.Image(self.maxWidth,120)
        img.Replace(0,0,0,0,0,255)
        self.imageCtrl = wx.StaticBitmap(self, id=wx.ID_ANY, bitmap=wx.NullBitmap, pos=(450, 125))
        self.imageCtrl.SetBitmap(wx.Bitmap(img))
        
        #Make giant OK button
        self.button1 = wx.Button(self, wx.ID_ANY, label="OK", pos=(350, 125), size=(50, 50))
        self.button1.SetFont(self.font1)
        self.button1.SetBackgroundColour((0, 200, 0))
        self.button1.SetForegroundColour((255, 255, 255))
        self.Bind(wx.EVT_BUTTON, self.onClickOK, self.button1)

        #Make Results text
        text3 = wx.StaticText(self, -1, "Results:", pos=(50, 300), size=(275, 50))
        text3.SetFont(self.font1)


        #Make result output box that's uneditable
        self.textbox2 = wx.TextCtrl(self, wx.ID_ANY, value="Results will appear here", pos=(50, 350), size=(500, 80), style=wx.TE_READONLY)
        self.textbox2.SetFont(self.font2)
        self.textbox2.SetForegroundColour((166, 166, 166))
        
    #def onNew(self, event):
        
    def onOpen(self, event):
        dlg = wx.FileDialog(self, message="Select an iamge", defaultDir = "", defaultFile = "",\
                            wildcard = "", style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.pathImage = dlg.GetPath()
            self.img = wx.Image(self.pathImage, wx.BITMAP_TYPE_ANY)
            W = self.img.GetWidth()
            H = self.img.GetHeight()
            
            if W != self.maxWidth:
                coefficient = self.maxWidth / W
                NewW = int(coefficient * W)
                NewH = int(coefficient * H)
                self.img = self.img.Scale(NewW,NewH)
                
            self.imageCtrl.SetBitmap(wx.Bitmap(self.img))
        
        dlg.Destroy()

        
    def onNew(self, event):
        self.reset()
  
    def onText(self, event):
        self.processText()

    def onImage(self, event):
        self.processImage()

    def onQuit(self, event):
        self.Close()

    def onClickOK(self, event):
        self.processText()
    
    def processText(self):
        numPlate = self.getText()
        self.extractYear(numPlate)
    
    def processImage(self):
        print(self.pathImage)
        if self.pathImage is not None:
            result = detect_text(self.pathImage,client)
            fullNumberPlate = result[0].description
            coordinatePoly = result[0].bounding_poly.vertices
            coordinateVertices = (['({},{})'.format(vertex.x, vertex.y)
                for vertex in coordinatePoly])
            print(fullNumberPlate)
            print(coordinateVertices)
            
            self.extractYear(fullNumberPlate)
            self.textbox1.SetValue(fullNumberPlate)
            #self.drawBox(coordinateVertices)
            
    
    #def drawBox(self, coordinateVertices):
    #    img_bitmap = self.img.ConvertToBitmap()
    #    dc = wx.MemoryDC(img_bitmap)
    #    dc.SetPen(wx.Pen('red', 5, wx.SOLID))
    #    dc.SetBrush(wx.Brush('red', wx.TRANSPARENT))
    #    dc.DrawLines(coordinateVertices)
    #    del dc
     #   self.imageCtrl.SetBitmap(img_bitmap)        
    
    def getText(self):
        return self.textbox1.GetValue()
        
    def printOutput(self, anyText):
        self.textbox2.SetValue(anyText)
        
    def reset(self):
        # Make the text to defaultDir
        self.textbox1.SetValue("")
        self.textbox2.SetValue("Results will appear here")
        # Clear the imageCtrl
        img = wx.Image(self.maxWidth,120)
        img.Replace(0,0,0,0,0,255)
        self.imageCtrl.SetBitmap(wx.Bitmap(img))        
       
    def extractYear(self,numPlate):
        if len(numPlate) == 8:
            #try:
            [a1, a2] = self.getNum(numPlate)
            [a1, half] = self.checkYear(a1)
            year = self.calYear(a1, a2, 2000)
            outputText = self.createMessageYear(year, half)
            self.printOutput(outputText)
            #except:
            #   self.printOutput("The 3rd and 4th digits must be integers")
        else:
            self.printOutput("It is not a UK Standard license plate") 
    
    def checkYear(self,inp):
        half = "1st half"
        if inp >= 5:
            inp = inp - 5
            half = "2nd half"
        return inp, half

    def getNum(self, inp):
        num = int(self.replaceNum2Letter(inp[2:4]))
        num1 = num // 10
        num2 = num % 10
        return num1, num2
    
    def replaceNum2Letter(self, inputString):
        inputString = inputString.replace("o", "0")
        inputString = inputString.replace("O", "0")
        inputString = inputString.replace("I", "1")
        inputString = inputString.replace("l", "1")
        inputString = inputString.replace("s", "5")
        inputString = inputString.replace("S", "5")
        return inputString
        
        
    
    def calYear(self, inp1, inp2, origin):
        year = inp1 * 10 + inp2 + origin
        return year

    def createMessageYear(self, year, half):
        return "This car is registered in {} in the {} of the year" .format(year, half)        
    
app = wx.App()
frm = myFrame(None, title = "Immerse Oxford Project")
frm.Show()
app.MainLoop()