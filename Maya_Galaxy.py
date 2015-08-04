#coding=gbk
import maya.cmds as cmds
from functools import partial

# ===========Scale Function==========
def setScaleFactor(*argv):
    cmds.scale(argv[0], 1, argv[0], "Galaxy_Star", "Galaxy_Cloud")          # Set the scale factor (x = z, keep the shape)
    
def ScaleAdjust():
    # Draw interface
    name = "ScaleControl"
    myLabel = "Scale Factor: "
    attr = "Galaxy_Star.scaleX"
    MaxValue = 10
    MinValue = 0
    Step = 0.1
    ScaleSlider = cmds.attrFieldSliderGrp(name, label = myLabel, w = 280, at = attr, 
                        columnWidth = [(1, 80), (2, 80)], 
                        columnAttach = [(2, "left", 10), (3, "left", 10)], 
                        fieldMaxValue = MaxValue, fieldMinValue = MinValue, fieldStep = Step,
                        sliderMaxValue = MaxValue, sliderMinValue = MinValue, sliderStep = Step, 
                        columnAlign = [(1, "left"), (2, "center"), (3, "right")], 
                        cc = setScaleFactor) 
# -----------End of Scale---------

# ===========Set other factors function==========      
def setFactorFunc(attr, *argv):
    cmds.setAttr(attr, argv[0])  
    
def createAttrSlider(name, myLabel, attr, MaxValue, MinValue, Step):
    # Using attrSlider instead of floatSlider...
    attrSlider = cmds.attrFieldSliderGrp(name, label = myLabel, w = 280, at = attr, 
                        columnWidth = [(1, 80), (2, 80)], 
                        columnAttach = [(2, "left", 10), (3, "left", 10)], 
                        fieldMaxValue = MaxValue, fieldMinValue = MinValue, fieldStep = Step,
                        sliderMaxValue = MaxValue, sliderMinValue = MinValue, sliderStep = Step, 
                        columnAlign = [(1, "left"), (2, "center"), (3, "right")], 
                        cc = partial(setFactorFunc, attr)) 
    return attrSlider
    
def otherFactorAdjust():   
    # Draw interface
    # Function Usage: createAttrSlider(name, myLabel, attr, MaxValue, MinValue, Step)  
    StarCount = createAttrSlider("StarCount", "Star Count: ", "Galaxy_StarShape.multiCount", 60, 1, 1)
    StarRadius = createAttrSlider("StarRadius", "Star Radius: ", "Galaxy_StarShape.multiRadius", 10, 0, 0.1)
    CloudRadius = createAttrSlider("CloudRadius", "Cloud Radius: ", "Galaxy_CloudShape.radius", 1, 0, 0.05)
    StarOpacity = createAttrSlider("StarOpacity", "Star Opacity: ", "Galaxy_StarShape.opacity", 2, 0, 0.1)
    CloudOpacity = createAttrSlider("CloudOpacity", "Cloud Opacity: ", "Galaxy_CloudShape.opacity", 2, 0, 0.1) 
# -----------End of other factors---------

# ===========Set color function==========
def colorAdjust():
    GalaxyColor = cmds.colorSliderGrp("GalaxyColor", label="Galaxy Color: ", w = 280, 
                                      columnWidth = [(1, 80), (2, 80)], 
                                      columnAttach = [(1, "right", 10), (3, "left", 10)], 
                                      rgbValue = (1, 0.4, 1),
                                      columnAlign = [(1, "left"), (2, "left"), (3, "right")], 
                                      cc = setColor)
def setColor(*argv):
    rgb = cmds.colorSliderGrp("GalaxyColor", q = True, rgbValue = True)
    rgb = ', '.join(str(i) for i in rgb)
    rgb = 'rgbPP = rand(<<0, 0, 0.6>>,<<' + str(rgb) + '>>)'
    cmds.dynExpression("Galaxy_StarShape", s = rgb, creation = True, runtimeAfterDynamics = True)    
    cmds.dynExpression("Galaxy_CloudShape", s = rgb, creation = True, runtimeAfterDynamics = True) 
    
# -----------End of color---------

def userGuide(*argv):
    
    if cmds.window("UserGuideWindow", exists = True):
        cmds.deleteUI("UserGuideWindow")
        
    window = cmds.window("UserGuideWindow",title = "User Guide for Galaxy Modifier v0.2", w = 600,  
                         minimizeButton = True, maximizeButton = False, sizeable = True) 
    
    cmds.paneLayout()
    
    cmds.textScrollList( "guideInfo", allowMultiSelection = False, 
                         append=[ "//    作者：李宏杰",
                                  "//    星系编辑脚本，版本V0.1，20150415",
                                  "//    脚本主页：http://lhj.nkco.org/?p=1173", 
                                  "",
                                  "*使用步骤：",
                                  "    1、使用Maya打开随脚本一起下载的MyGalaxy.mb，同时把脚本放到Maya的脚本目录下，", 
                                  "        例如 C:\Users\Lee\Documents\maya\2015-x64\zh_CN\scripts；", 
                                  "    2、在Maya的Python命令框输入以下语句，并拖动到工具栏：",
                                  "        import MyGalaxy", 
                                  "        reload(MyGalaxy)", 
                                  "        MyGalaxy.createUI()", 
                                  "    3、自由调节各参数至获得满意效果即可。", 
                                  "", 
                                  "*参数说明：（模型中的星系由两层粒子组成，一层代表星星，一层代表星云）", 
                                  "    Scale Factor: 按比例放大/缩小；", 
                                  "    Galaxy Color：星系的主体颜色。星系的颜色会以该颜色为基色随机。", 
                                  "    Star Count：星星的数量；", 
                                  "    Star Radius：星星的密度（多点半径）；", 
                                  "    Cloud Radius：星云的粒子半径；", 
                                  "    Star Opacity, Cloud Opacity：星星/星云的透明度；"]
                         )    
    
    cmds.showWindow(window)

def resetAllFactors(*argv):  
    # Reset scale factor
    setScaleFactor(1)
    
    # Reset color selector
    setColor([1, 0.4, 1])
    cmds.colorSliderGrp("GalaxyColor", e = True, rgbValue = (1, 0.4, 1))
    
    # Reset other factors
    setFactorFunc("Galaxy_StarShape.multiCount", 10, 10)
    setFactorFunc("Galaxy_StarShape.multiRadius", 1.7, 1.7)
    setFactorFunc("Galaxy_CloudShape.radius", 0.1, 0.1)
    setFactorFunc("Galaxy_StarShape.opacity", 0.3, 0.3)
    setFactorFunc("Galaxy_CloudShape.opacity", 0.6, 0.6)    
    
# ==========Program Entrance Function=========
# Create our interface
def createUI():
    
    # Check if window already exists
    if cmds.window("MyGalaxy", exists = True):
        cmds.deleteUI("MyGalaxy")
    if cmds.window("UserGuideWindow", exists = True):
        cmds.deleteUI("UserGuideWindow")        
        
    # Create our window
    window = cmds.window("MyGalaxy",title = "Galaxy Modifier v0.2", w = 300, 
                         minimizeButton = True, maximizeButton = False, sizeable = True)
    
    # MAIN layout
    mainLayout = cmds.columnLayout(columnAlign = "center", columnAttach = ("both", 10), rowSpacing = 5, visible = True)
    
    # banner
    bannerPath = cmds.internalVar(userScriptDir = True) + "banner.jpg"
    cmds.image(w = 280, h = 160, image = bannerPath)
    
    # User guide
    guidebtn = cmds.button("User Guide", align = "center", label = "User Guide", w = 280, actOnPress = False, command = userGuide)
    
    # Scale Factor
    cmds.text(align = "left", label = "Galaxy Size Adjust: ", font = "boldLabelFont", w = 280) 
    ScaleAdjust()
    
    # Color factor
    cmds.text(align = "left", label = "Color Adjust: ", font = "boldLabelFont", w = 280)    
    colorAdjust()
      
    # Other factors
    cmds.text(align = "left", label = "Other Factors Adjust: ", font = "boldLabelFont", w = 280)  
    otherFactorAdjust()
    
    # Reset button
    resetBtn = cmds.button("reset", align = "center", label = "RESET ALL FACTORS", w = 280, actOnPress = False, command = resetAllFactors)
     
    # show
    cmds.showWindow(window)