# -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe
import os,sys
sys.argv.append('py2exe')

options = {
    "py2exe":{
        "compressed": 1, #压缩  
        "optimize": 2,  
        "bundle_files": 1 #所有文件打包成一个exe文件  
    }
}  

setup(
    version = "0.1.7",
    description = "Auto Course Selector",
    name = "CD_Selector",
    options=options,
    console = [
        {'script': 'CDSelector.py'}
    ]
)