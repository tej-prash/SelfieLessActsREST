# SelfieLessActsREST
A REST API for SelfieLessActs project <br/>

app_rest.py contains the python code that implements the REST API. This is present on VM2 <br/>
app_backend.py contains python code for rendering webpages. This communicates with the REST API to obtain information. This is present on VM1 <br/>
templates- Folder that contains html files to be rendered <br/>

Architecture: <br/>
Client --> VM1(Renders Webpages) --> VM2(REST API)

Instructions for running: <br/>
Run python3 app_rest.py for running the REST API. Requests can be made only to the REST API <br/>
Run python3 app_backend.py for running the backend. app_rest.py must be run along with this since it makes requests to it. <br/>

Dependendies: <br/>
Flask Web Framework needs to be setup in order to run this  <br/>
