# IPCC AR6 Data Rescue Progress
### https://ipcc-dashboard.streamlit.app

This deployed Streamlit app summarizes the data rescue for IPCC AR6 WGI, WGII, and WGIII, completed in the spring of 2025 by Samantha Anwar, Gideon Tay, and Yasmine Daouk
under the direction of Xiaoshi Xing at Columbia University. Data last updated on May 14, 2025. 

To update the data in the app, ensure that the file contains the same column names and same sheet names. Sheet names should be in the format: [WG] [SPM/TS/Chapters]. 
The code looks for Annex and Cross-chapter sections too. View `concat_sheets` in `viz.py` for more details on how the app reads in the Excel files. The visualizations
should update automatically (may take a few minutes to reboot) without rerunning any code.

To add another tab in the app, update `app.py`.

***Note:*** The data in the SYR tab is currently hardcoded into `app.py` because we did not have access to a file in the same format as the others. Please update data in `app.py` directly.

Visualizations were created using interactive graphing library [Plotly](https://plotly.com/python/). The web application uses [Streamlit](https://docs.streamlit.io).

The owner of this Github and the deployed Streamlit app is Samantha Anwar (soa2134@columbia.edu). Contact Samantha with any questions or to request push access to this repo
to update the app.
