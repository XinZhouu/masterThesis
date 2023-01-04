# this file shows the project structure
import sys

class DirUsr:

    # class properties

    winRt = 'E:\\CMU\\thesis\\1127'
    linuxRt = 'C:/Users/zxin1/Desktop/Glare'

    # command promport location
    CMD = 'C:\\Windows\\System32\\cmd.exe'
    BASH = 'C:/Program Files/Git/bin/bash.exe'
    
    # honeybee engine recipes
    DASimEngine = 'C:\\Users\\zxin1\\anaconda3\\Lib\\site-packages\\lbt_recipes\\annual_daylight'
    imaglessGlareSimEngine = 'C:\\Users\\zxin1\\anaconda3\\Lib\\site-packages\\lbt_recipes\\imageless_annual_glare'

    # directory structure
    exeRad = winRt + '\\exeRad'
    results = winRt + '\\results'
    data = winRt + '\\data'
    model = winRt + '\\model'
    epwPath = model + '\\weather\\USA_MA_Boston-Logan.Intl.AP.725090_TMY3.epw'
    script = winRt + '\\scriptsEnv'
    
    # directory inside scriptEnv folder
    inputDataDir = script + '\\rawData'
    outputDataDir = script + '\\rawData\\output'
    modelForSimDir = script + '\\RModel'
    modelWithGridDir = modelForSimDir + '\\modelGrid'
    outDataDir = script + '\\outData'
    
    # radiance engine
    radianceEngineBinPath = script + '\\USimEngine\\URadiance\\Radiance\\bin'
    radianceEngineLibPath = script + '\\USimEngine\\URadiance\\Radiance\\lib'
    
    # directory inside Rmodel/model
    windowMatDir = modelForSimDir + '\\model\\aperture\\aperture.mat'
    windowRadDir = modelForSimDir + '\\model\\aperture\\aperture.rad'
    sceneMatDir = modelForSimDir + '\\model\\scene\\envelope.mat'
    sceneRadDir = modelForSimDir + '\\model\\scene\\envelope.rad'
    
    # directory inside Rmodel/modelGrid
    DAConfigFile = modelWithGridDir + '\\annual_daylight_inputs.json'
    
    # directory inside outData folder
    hdrDir = outDataDir + '\\hdr'
    