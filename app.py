import sys

sys.dont_write_bytecode = True

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from viz import *
from st_flexible_callout_elements import flexible_callout, flexible_info, flexible_warning

st.set_page_config(
    page_title='IPCC AR6 Data Rescue',
    page_icon='🌎',
)

flexible_warning('''
    <b>Navigation Help</b>

    All visualizations here are dynamic and interactive. In the bar charts and funnel chart,
    double-click on a category (SPM, TS, etc.) to isolate the visualization to the selection.
    Single-click will remove the selection from view.

    Click on the inner rings in the sunburst charts to view more details in that section.''',
    border_radius=20)

tab1, tab2, tab3, tab4 = st.tabs(['WGI', 'WGII', 'WGIII', 'SYR'])

with tab1:
    st.title('Working Group I Data Rescue')

    wg1 = concat_sheets('WGI.xlsx', wg='WGI')
    
    st.header("No. of figures", divider=True)
    st.plotly_chart(count_bar(wg1))

    st.header("Data-driven figures with and without issues", divider=True)
    st.plotly_chart(quant_errors(wg1))

    st.header("Error percentage", divider=True)
    st.plotly_chart(error_mix(wg1))

    st.header("Figures breakdown", divider=True)
    st.plotly_chart(sunburst('WGI.xlsx', 'WGI Chapters'))

    st.header("Data-driven figures breakdown", divider=True)
    st.markdown("This sunburst diagram shows the number of data-driven figures in " \
    "SPM, TS, chapters, annexes, and cross-chapters. It first breaks them down into unique and non-unique figures." \
    "We break down unique figures further into those with archived data and those without. Among unique figures with archived data," \
    "we distinguish between those with and without issues with the archived data.")
    st.plotly_chart(sunburst2('WGI.xlsx', wg_prefix='WGI'))

    st.header('Archived data-driven figures', divider=True)
    st.plotly_chart(funnel(wg1))

with tab2:
    st.title('Working Group II Data Rescue')

    wg2 = concat_sheets('WGII.xlsx', wg='WGII')
    
    st.header("No. of figures", divider=True)
    st.plotly_chart(count_bar(wg2))

    st.header("Data-driven figures with and without issues", divider=True)
    st.plotly_chart(quant_errors(wg2))

    st.header("Error percentage", divider=True)
    st.plotly_chart(error_mix(wg2))

    st.header("Figures breakdown", divider=True)
    st.plotly_chart(sunburst('WGII.xlsx', 'WGII Chapters'))

    st.header("Data-driven figures breakdown", divider=True)
    st.markdown("This sunburst diagram shows the number of data-driven figures in " \
    "SPM, TS, chapters, annexes, and cross-chapters. It first breaks them down into unique and non-unique figures." \
    "We break down unique figures further into those with archived data and those without. Among unique figures with archived data," \
    "we distinguish between those with and without issues with the archived data.")
    st.plotly_chart(sunburst2('WGII.xlsx', wg_prefix='WGII'))

    st.header('Archived data-driven figures', divider=True)
    st.plotly_chart(funnel(wg2))

with tab3:
    st.title('Working Group III Data Rescue')

    wg3 = concat_sheets('WGIII.xlsx', wg='WGIII')
    
    st.header("No. of figures", divider=True)
    st.plotly_chart(count_bar(wg3))

    st.header("Data-driven figures with and without issues", divider=True)
    st.plotly_chart(quant_errors(wg3))

    st.header("Error percentage", divider=True)
    st.plotly_chart(error_mix(wg3))

    st.header("Figures breakdown", divider=True)
    st.plotly_chart(sunburst('WGIII.xlsx', 'WGIII Chapters'))

    st.header("Data-driven figures breakdown", divider=True)
    st.markdown("This sunburst diagram shows the number of data-driven figures in " \
    "SPM, TS, chapters, annexes, and cross-chapters. It first breaks them down into unique and non-unique figures." \
    "We break down unique figures further into those with archived data and those without. Among unique figures with archived data," \
    "we distinguish between those with and without issues with the archived data.")
    st.plotly_chart(sunburst2('WGIII.xlsx', wg_prefix='WGIII'))

    st.header('Archived data-driven figures', divider=True)
    st.plotly_chart(funnel(wg3))

with tab4:
    st.title('SYR Data Rescue')

    df = pd.DataFrame({
        'sections': ['SPM', 'SPM', 'SPM', 'SPM', 'LR', 'LR', 'LR', 'LR'],
        'cat1':     ['Archived', 'Archived', 'Archived', 'Not Archived', 'Archived', 'Archived', 'Archived', 'Not Archived'],
        'cat2':     ['Unique', 'Unique', 'Not Unique', None, 'Unique', 'Unique', 'Not Unique', None],
        'cat3':     ['Issues', 'No Issues', None, None, 'Issues', 'No Issues', None, None],
        'values':   [1, 22, 0, 1, 0, 27, 19, 3]
    })
    
    fig = px.sunburst(df, path=['sections', 'cat1', 'cat2', 'cat3'], values='values')
    fig.update_layout(margin=dict(t=10, l=10, r=10, b=10), height=600, width=600)
    fig.update_traces(hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Share of parent: %{percentParent:.1%}<extra></extra>')
    st.plotly_chart(fig)