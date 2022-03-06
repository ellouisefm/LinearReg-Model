from server import server
from dashapp.CaseStudyDash import app
# from CSDash import app as cs_dash

if __name__ == '__main__':
    #server.run(debug=False)
    app.run_server(debug=False)
