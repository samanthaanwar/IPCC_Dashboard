import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from viz import *

st.set_page_config(
    page_title='IPCC AR6 Data Rescue',
    page_icon='🌎',
)

tab1, tab2, tab3 = st.tabs(['WGI', 'WGII', 'WGIII'])

with tab1:
    st.title('Working Group I Data Rescue')

    wg1 = concat_sheets('WGI.xlsx', wg='WGI')
    
    st.plotly_chart(count_bar(wg1))
    st.plotly_chart(quant_errors(wg1))
    st.plotly_chart(error_mix(wg1))
    st.plotly_chart(sunburst('WGI.xlsx', 'WGI Chapters'))

with tab2:
    st.title('Working Group II Data Rescue')

    wg2 = concat_sheets('WGII.xlsx', wg='WGII')
    
    st.plotly_chart(count_bar(wg2))
    st.plotly_chart(quant_errors(wg2))
    st.plotly_chart(error_mix(wg2))
    st.plotly_chart(sunburst('WGII.xlsx', 'WGII Chapters'))

with tab3:
    st.title('Working Group III Data Rescue')

    wg3 = concat_sheets('WGIII.xlsx', wg='WGIII')
    
    st.plotly_chart(count_bar(wg3))
    st.plotly_chart(quant_errors(wg3))
    st.plotly_chart(error_mix(wg3))
    st.plotly_chart(sunburst('WGIII.xlsx', 'WGIII Chapters'))
