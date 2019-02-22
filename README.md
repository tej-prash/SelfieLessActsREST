# SelfieLessActsREST
A REST API for SelfieLessActs project

app_rest.py contains the python code that implements the REST API. This is present on VM2
app_backend.py contains python code for rendering webpages. This communicates with the REST API to obtain information. This is present on VM1
templates- Folder that contains html files to be rendered

Architecture:
Client --> VM1(Renders Webpages) --> VM2(REST API)
