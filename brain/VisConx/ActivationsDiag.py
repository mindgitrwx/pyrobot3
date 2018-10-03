__author__ = "Matt Fiedler"
__version__ = "$Revision: 1.7 $"

import tkinter
import copy
import math
import tkinter.simpledialog

class LayerCanvas(tkinter.Canvas):
    PADDING = 4
    def __init__(self, parent, numNodes, numColumns=3, nodeSize=25):
        #calculate dimensions
        self.numColumns = numColumns
        self.numRows = int(math.ceil(float(numNodes)/numColumns))
        self.nodeSize = nodeSize
        self.numNodes = numNodes
        self.plotWidth = numColumns*nodeSize + (numColumns+1)*self.PADDING
        self.plotHeight = self.numRows*nodeSize + (self.numRows + 1)*self.PADDING
        self.visible = 1

        #create canvas
        tkinter.Canvas.__init__(self, parent, height=self.plotHeight, width=self.plotWidth, bg = "white")

        #draw nodes
        self.nodeItems = []
        for i in range(numNodes):
            coords = self.nodeNumToCoords(i)
            self.nodeItems += [self.create_oval(coords[0], coords[1], coords[0]+nodeSize, coords[1]+nodeSize, outline="black")]
            self.create_text(coords[0] + nodeSize/2 + 1, coords[1]+nodeSize/2 + 1, text="%u" % (i,), fill="red", font=("Arial", 10, "bold"))

    def nodeNumToCoords(self, nodeNum):
        xCoord = (nodeNum//self.numRows)*(self.nodeSize + self.PADDING) + self.PADDING
        yCoord = (nodeNum % self.numRows)*(self.nodeSize + self.PADDING) + self.PADDING

        return xCoord, yCoord
    
    def updateActivs(self, newActivs):
        for i in range(len(self.nodeItems)):
            try:
                if newActivs[i] > 1.0:
                    self.itemconfigure(self.nodeItems[i], fill ="#%04x%04x%04x" % ((65535,)*3))
                else:
                    self.itemconfigure(self.nodeItems[i], fill ="#%04x%04x%04x" % ((65535*newActivs[i],)*3))
            except:
                pass

    def getWidth(self):
        return int(self.cget("width"))

    def setVisible(self, visible):
        self.visible = visible

        if visible:
            self.config(height=self.plotHeight, width=self.plotWidth)
        else:
            self.config(height=0, width=0)

class LevelFrame(tkinter.Frame):
    def __init__(self, parent, nameSizeList):
        tkinter.Frame.__init__(self, parent)
        self.nameSizeList = nameSizeList
        self.layerCanvasList = []
        self.layerLabelList = []
        self.visibleList = [1]*len(nameSizeList)
        
        for i in range(len(self.nameSizeList)):
            self.layerLabelList += [tkinter.Label(self, text=self.nameSizeList[i][0])]
            self.layerLabelList[-1].grid(row=2*i, col=0)
            self.layerCanvasList += [LayerCanvas(self, self.nameSizeList[i][1], numColumns=3, nodeSize=25)]
            self.layerCanvasList[-1].grid(row=2*i+1, col=0)

    def updateActivs(self, newActivs):
        for i in range(len(self.layerCanvasList)):
            self.layerCanvasList[i].updateActivs(newActivs[i])

    def getWidth(self):
        maxWidth = 0
        for layerCanvas in self.layerCanvasList:
            if layerCanvas.getWidth() > maxWidth:
                maxWidth = layerCanvas.getWidth()

        return maxWidth

    def getNameList(self):
        return [item[0] for item in self.nameSizeList]

    def getVisList(self):
        return self.visibleList

    def setVisible(self, visibleList):
        self.visibleList = visibleList
        for i in range(len(visibleList)):
            self.layerCanvasList[i].setVisible(visibleList[i])
            if self.layerLabelList[i] and not visibleList[i]:
                self.layerLabelList[i].config(text="")
            elif visibleList[i]:
                self.layerLabelList[i].config(text=self.nameSizeList[i][0])
        
class LayerSelectionDialog(tkinter.simpledialog.Dialog):
    def __init__(self, parent, levelFrameList):
        self.levelFrameList = levelFrameList
        self.varLists = []
        tkinter.simpledialog.Dialog.__init__(self, parent, title="Select Layers")
        self.parent=parent
        
    def body(self, master):
        nameLists = []
        visLists = []
        for level in self.levelFrameList:
            nameLists += [level.getNameList()]
            visLists += [level.getVisList()]  

        for i in range(len(nameLists)):
            levelVarList = []
            for j in range(len(nameLists[i])):
                levelVarList += [tkinter.IntVar(self.parent)]
                levelVarList[-1].set(visLists[i][j])
                tkinter.Checkbutton(master, text=nameLists[i][j], variable=levelVarList[-1]).grid(row=j, col=i)
            self.varLists += [levelVarList]

        self.update_idletasks()

    def apply(self):
        self.result = [[layerVar.get() for layerVar in level] for level in self.varLists]        

class ActivDiag(tkinter.Toplevel):
    SCALE_HEIGHT = 20
    def __init__(self, parent, netStruct):
        tkinter.Toplevel.__init__(self, parent)
        self.title("Network Activations")
        self.netStruct=netStruct
        self.levelFrameList = []
        
        self.genLevelFrames()        
        self.scaleCanvas = tkinter.Canvas(self, height=self.SCALE_HEIGHT)
        self.drawScale(self.calcFullWidth())

        self.buttonFrame = tkinter.Frame(self)
        self.layersButton = tkinter.Button(self.buttonFrame, text="Layers...", command=self.handleLayerSelectDialog)
        self.layersButton.pack(side=tkinter.RIGHT)
        self.buttonFrame.grid(row=2, column=0, columnspan=len(self.levelFrameList)+1)
        
        self.updateActivs()

    def genLevelFrames(self):
        for i in range(len(self.netStruct.levelList)):
            nameSizeList = [(vertex.name, vertex.layerObj.size) for vertex in self.netStruct.levelList[i]]
            self.levelFrameList += [LevelFrame(self, nameSizeList)]
            self.levelFrameList[i].grid(row=0, column=i)
        nameSizeList = [("Desired %s" % (layer[0],), layer[1]) for layer in nameSizeList]
        self.levelFrameList += [LevelFrame(self, nameSizeList)]
        self.levelFrameList[-1].grid(row=0, column=len(self.netStruct.levelList))
        # Go through and set visible based on nodeNum
        # If too many (> 50), then don't initially show
        for i in range(len(self.levelFrameList)):
            vlist = []
            for canvas in self.levelFrameList[i].layerCanvasList:
                if canvas.numNodes <= 50:
                    vlist.append( 1 )
                else:
                    vlist.append( 0 )
            self.levelFrameList[i].setVisible(vlist)
    
    def updateActivs(self):
        for i in range(len(self.levelFrameList)-1):
            self.levelFrameList[i].updateActivs([vertex.layerObj.activation for vertex in self.netStruct.levelList[i]])

        self.levelFrameList[-1].updateActivs([vertex.layerObj.target for vertex in self.netStruct.levelList[-1]])
        self.update_idletasks()

    def drawScale(self, width):
        self.scaleCanvas.config(width=width)
        for i in range(width):
            self.scaleCanvas.create_line(i, 0, i, self.SCALE_HEIGHT, fill="#%04x%04x%04x" % ((65535*float(i)/(width-1),)*3))
        self.scaleCanvas.create_text(1, self.SCALE_HEIGHT/2, text="0.0", fill="red", anchor = tkinter.W)
        self.scaleCanvas.create_text(width-1, self.SCALE_HEIGHT/2, text="1.0", fill="red", anchor = tkinter.E)
        self.scaleCanvas.grid(row=1, column=0, columnspan=len(self.levelFrameList)+1, sticky=tkinter.N)

    def calcFullWidth(self):
        fullWidth=0
        for levels in self.levelFrameList:
            fullWidth += levels.getWidth()

        return fullWidth

    def handleLayerSelectDialog(self):
        layerSelectDialog = LayerSelectionDialog(self, self.levelFrameList)
        if layerSelectDialog.result:
            for i in range(len(layerSelectDialog.result)):
                self.levelFrameList[i].setVisible(layerSelectDialog.result[i])

        self.drawScale(self.calcFullWidth())
        self.update_idletasks()

    def reset(self):
        for levelFrames in self.levelFrameList:
            levelFrame.destroy()
        self.levelFrameList = []
        self.genLevelFrames()
        self.drawScale()

class ActivSweepDiag(ActivDiag):
    def __init__(self, parent, netStruct):
        ActivDiag.__init__(self, parent, netStruct)
        
        #make prev/next buttons
        self.prevButton = tkinter.Button(self.buttonFrame, text="Previous", command=self.handlePrev, state=tkinter.DISABLED)
        self.prevButton.pack(side=tkinter.LEFT)
        self.nextButton = tkinter.Button(self.buttonFrame, text="Next", command=self.handleNext)
        self.nextButton.pack(side=tkinter.LEFT)

        self.storedActivs= []
        self.currentIndex = 0

        self.calcActivs()
        self.drawActivs()
        
    def handleNext(self):
        self.currentIndex += 1
        self.prevButton.config(state=tkinter.NORMAL)
        if self.currentIndex ==  len(self.storedActivs)-1:
            self.nextButton.config(state=tkinter.DISABLED)
            
        self.drawActivs()
            
    def handlePrev(self):
        self.currentIndex -= 1
        self.nextButton.config(state=tkinter.NORMAL)
        if self.currentIndex == 0:
            self.prevButton.config(state=tkinter.DISABLED)

        self.drawActivs()
    
    def calcActivs(self):
        #this is ugly, but essential to the extraction of data from sweep
        self.netStruct.network.activDiag = self
        self.netStruct.network.sweep()
        
    def extractActivs(self):
        currentPattern = []
        for level in self.netStruct.levelList:
            currentLevel =[]
            for vertex in level:
                currentLevel += [copy.deepcopy(vertex.layerObj.activation)]
            currentPattern += [currentLevel]
        currentLevel = []
        for vertex in self.netStruct.levelList[-1]:
            currentLevel += [copy.deepcopy(vertex.layerObj.target)]
        currentPattern += [currentLevel]
        self.storedActivs += [currentPattern]

    def drawActivs(self):
        for i in range(len(self.levelFrameList)):
            self.levelFrameList[i].updateActivs(self.storedActivs[self.currentIndex][i])
        self.update_idletasks()
