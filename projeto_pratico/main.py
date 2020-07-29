#!/usr/bin/env python
# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd 
import numpy as np 
import pystaticplot as ps
import functions as fun
import pipeline as pp

if __name__ == '__main__':
    
    fun.style()
    fun.sidebar()