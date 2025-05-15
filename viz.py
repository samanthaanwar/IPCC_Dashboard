import pandas as pd
import plotly.express as px
import numpy as np

def sunburst(file, sheet):
    df = pd.read_excel(file, sheet_name = sheet)
    df = df[['Chapter', 'Type', 'Data status', 'Figure']].fillna('No data status')
    df['Chapter'] = df.Chapter.apply(lambda x:'Chapter '+str(x))
    grouped = df.groupby(['Chapter', 'Type', 'Data status']).size().reset_index(name='Count')
    
    # For Conceptual entries, we don't want a third level, so we collapse it
    grouped['path'] = grouped.apply(
                        lambda row: [str(row['Chapter']), row['Type']] 
                        if row['Type'] == 'Conceptual' 
                        else [str(row['Chapter']), row['Type'], row['Data status']], axis=1)

    conceptual = df[df['Type'] == 'Conceptual'].copy()
    quantitative = df[df['Type'] == 'Quantitative'].copy()

    # For Conceptual, no Data Status
    conceptual_grouped = conceptual.groupby(['Chapter', 'Type']).size().reset_index(name='Count')
    conceptual_grouped['Data status'] = None  # placeholder to match column structure
    
    # For Quantitative, include Data Status
    quantitative_grouped = quantitative.groupby(['Chapter', 'Type', 'Data status']).size().reset_index(name='Count')
    
    # Concatenate
    combined = pd.concat([conceptual_grouped, quantitative_grouped], ignore_index=True)

    fig = px.sunburst(data_frame=combined, path=['Chapter', 'Type', 'Data status'], values='Count')

    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25), height=650, width=650)
    fig.update_traces(hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Share of parent: %{percentParent:.1%}<extra></extra>')
    
    return fig

def concat_sheets(file, wg):
    sheets = pd.read_excel(file, sheet_name = None).keys()
    spm = pd.read_excel(file, sheet_name = wg+' SPM')
    spm['Section'] = 'SPM'
    
    ts = pd.read_excel(file, sheet_name = wg+' TS')
    ts['Section'] = 'TS'
    
    chapters = pd.read_excel(file, sheet_name = wg+' Chapters')
    chapters['Section'] = 'Chapters'

    extra=''
    for sheet in sheets:
        if 'Annex' in sheet:
            extra = sheet
        elif 'Cross' in sheet:
            extra = sheet
            
    if extra:
        extra_df = pd.read_excel(file, sheet_name = extra)
        extra_df['Section'] = extra
    
        all_dfs = pd.concat([spm, ts, chapters, extra_df])
        
    else:
        all_dfs = pd.concat([spm, ts, chapters])

    return all_dfs

def count_bar(df):
    columns = [
        'Section', 'Type', 'Data status', 'Issues?', 
        'Unique?', 'Unique data driven?',
        'Unique data driven & Archived & No issue?', 
        'Unique data driven & Archived']
    
    df = df[columns]
    
    df = df.groupby(by=['Section', 'Type'], observed=True).size().reset_index(name='Count')
    
    sections = df['Section'].unique()
    if len(sections) == 4:
        section_order = ['SPM', 'TS', 'Chapters', sections[-1]]
    else:
        section_order = ['SPM', 'TS', 'Chapters']

    fig = px.bar(
        df, x = 'Count', y = 'Section', 
        color = 'Type', orientation = 'h',
        custom_data = 'Type',
        category_orders={'Section': section_order})

    fig.update_layout(
        legend_title_text=None, 
        font_family='Arial',
        legend=dict(
            orientation='h',       # horizontal legend
            yanchor='bottom',
            y=1.02,                # just above the plot
            xanchor='center',
            x=0.5
        ))
    
    fig.update_traces(hovertemplate='<b>%{y}</b><br>%{customdata[0]}: %{x} Figures<extra></extra>')
    return fig

def quant_errors(df):
    columns = [
        'Section', 'Type', 'Data status', 'Issues?', 
        'Unique?', 'Unique data driven?',
        'Unique data driven & Archived & No issue?', 
        'Unique data driven & Archived']
    
    df = df[df.Type == 'Quantitative']
    df = df.groupby(by=['Section', 'Issues?'], observed=True).size().reset_index(name='Count')
    
    df['Percent'] = df.groupby('Section', observed=True)['Count'].transform(lambda x: round(x / x.sum() * 100, 1))
    df['Issues?'] = df['Issues?'].replace(True, 'Data-driven figures w/ issues')
    df['Issues?'] = df['Issues?'].replace(False, 'Data-driven figures w/o issues')

    sections = df['Section'].unique()
    if len(sections) == 4:
        section_order = ['SPM', 'TS', 'Chapters', sections[-1]]
    else:
        section_order = ['SPM', 'TS', 'Chapters']
    
    fig = px.bar(
        df, x = 'Percent', y = 'Section', 
        color = 'Issues?', 
        orientation = 'h',
        custom_data = 'Issues?',
        category_orders={'Section': section_order})
    
    fig.update_traces(hovertemplate='<b>%{y}</b><br>%{customdata[0]}: %{x}%<extra></extra>')
    fig.update_layout(
        legend_title_text=None, 
        font_family='Arial',
        legend=dict(orientation='h', yanchor='bottom',
                    y=1.02, xanchor='center', x=0.5))

    return fig

def error_mix(df):
    error_columns = ['Section', 'Data status', 'Metadata issues', 'Data issues', 'Other issues']
    error_mix = df[error_columns]

    df1 = (error_mix
       .groupby('Section')
       .apply(lambda g: g[['Metadata issues', 'Data issues', 'Other issues']]
              .notna().sum(), include_groups=False)
       .reset_index())

    df2 = error_mix.groupby(['Section', 'Data status']).size().reset_index(name='Missing data')
    df2 = df2[df2['Data status'] == 'Not Found'][['Section', 'Missing data']]
    counts = df1.merge(df2, on = 'Section', how='outer').fillna(0)

    sections = counts['Section'].unique()
    if len(sections) == 4:
        section_order = ['SPM', 'TS', 'Chapters', sections[-1]]
    else:
        section_order = ['SPM', 'TS', 'Chapters']

    # Select just the numeric columns
    issue_cols = ['Metadata issues', 'Data issues', 'Other issues', 'Missing data']
    
    # Calculate row totals
    row_totals = counts[issue_cols].sum(axis=1)
    
    # Compute row-wise percentages
    df_percent = counts[issue_cols].div(row_totals, axis=0) * 100
    df_percent = df_percent.round(1)
    df_percent.insert(0, 'Section', counts['Section'])
    
    df_melted = df_percent.melt(id_vars='Section', var_name='Issue Type', value_name='Percentage')

    fig = px.bar(
        df_melted, x = 'Percentage', y = 'Section', 
        color = 'Issue Type', orientation = 'h',
        custom_data = 'Issue Type',
        category_orders={'Section': section_order})

    fig.update_traces(hovertemplate='<b>%{y}</b><br>%{customdata[0]}: %{x}%<extra></extra>')
    fig.update_layout(
        legend_title_text=None, 
        font_family='Arial',
        legend=dict(orientation='h', yanchor='bottom',
                    y=1.02, xanchor='center', x=0.5))

    return fig

def sunburst2(file, wg_prefix='WGI'):
    xls = pd.ExcelFile(file)
    sheets = xls.sheet_names

    sheet_map = {
        f'{wg_prefix} SPM': 'SPM',
        f'{wg_prefix} TS': 'TS',
        f'{wg_prefix} Chapters': None,
        f'{wg_prefix} Annex': 'Annex',
    }

    all_dfs = []
    for sheet, chapter_label in sheet_map.items():
        if sheet in sheets:
            df = pd.read_excel(file, sheet_name=sheet)
            if chapter_label:
                df['Chapter'] = chapter_label
            all_dfs.append(df)

    # Add Cross-Chapter sheet if available
    cross_sheet = next((s for s in sheets if 'Cross' in s), None)
    if cross_sheet:
        df_cross = pd.read_excel(file, sheet_name=cross_sheet)
        all_dfs.append(df_cross)
    
    # Filter for Quantitative only
    df = pd.concat(all_dfs, ignore_index=True)
    df = df[df['Type'] == 'Quantitative'].copy()

    def format_chapter_label(x):
        try:
            return f'Chapter {int(x)}'  # if it's a number, format it
        except (ValueError, TypeError):
            return str(x)  # else keep it as-is (SPM, TS, Annex, etc.)

    df['Section'] = df['Chapter'].apply(format_chapter_label)

    # Sunburst hierarchy
    df['Unique Label'] = df['Unique?'].map({True: 'Unique', False: 'Not Unique'})
    df['Archived Label'] = df.apply(
        lambda row: 'Archived' if row['Unique Label'] == 'Unique' and row['Unique data driven & Archived'] else 
                    'Not Archived' if row['Unique Label'] == 'Unique' else None, axis=1)
    df['Issues Label'] = df.apply(
        lambda row: 'Issues' if row['Archived Label'] == 'Archived' and row['Issues?'] == True else 
                    'No Issues' if row['Archived Label'] == 'Archived' and row['Issues?'] == False else None, axis=1)

    grouped = df.groupby(['Section', 'Unique Label', 'Archived Label', 'Issues Label'], dropna=False).size().reset_index(name='Count')

    fig = px.sunburst(grouped, path=['Section', 'Unique Label', 'Archived Label', 'Issues Label'], values='Count')
    fig.update_layout(margin=dict(t=10, l=10, r=10, b=10), height=750, width=750)
    fig.update_traces(hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Share of parent: %{percentParent:.1%}<extra></extra>')

    return fig


