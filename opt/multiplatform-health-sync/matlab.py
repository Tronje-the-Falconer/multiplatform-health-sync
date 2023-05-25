#!/usr/bin/python3
"""
    matlab.com
"""
# import matlab.engine

def runImReady4():
    eng = matlab.engine.start_matlab()
    eng.triarea(nargout=0)
    print('matlab')