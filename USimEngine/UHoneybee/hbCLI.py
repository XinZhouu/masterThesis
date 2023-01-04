import subprocess
from dataCtl import *
from directory import *

class hbCLI:
    @staticmethod
    def hbOctree(folder):
        cmd = (
                'honeybee-radiance octree from-folder' +
                ' ' + folder
                )
        
        print('honeybee octree command: ', cmd)
        subprocess.call(cmd,
                        shell = True,
                        executable = dir.CMD,
                        cwd = folder)
        
    
    @staticmethod
    def hbRpict(view, scene, fileDir, para):
        resolution = '-r 800'
        name = strUtil.extractTargetStrLayer(scene, '.', 1, 'left')
        output = '-o ' + name + '.hdr'
        cmd = (
               'honeybee-radiance rpict rpict --rad-params' +
               ' ' + para +  
               ' ' + output +
               ' ' + resolution +
               ' ' + scene +
               ' ' + view
            )
        
        print('honeybee rpict command: ', cmd)
        subprocess.call(cmd,
                        shell = True,
                        executable = dir.CMD,
                        cwd = fileDir)

# fileDir = dir.root + '\\file'
# view = 'view.vf'
# scene = 'scene.oct'
# para = '-ab 2'
# #hbCLI.hbRpict(view, scene, fileDir, para)
        
        