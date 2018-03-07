import numpy as np
import pandas as pd
from datetime import datetime
import logging


LEVELS = {'debug':0, 'info':1, 'warning':2, 'error':3, 'critical':4}

class LogEntry(object):
    def __init__(self,level,msg):
        now = datetime.now()
        self.time = now.strftime("%Y-%m-%d_%H:%M:%S")
        self.level = level
        self.msg = msg

class Style(object):
    def __init__(self,fmt=None,title="",prefix="",EOL="\n"):
        self.fmt=fmt
        self.title = title
        self.prefix = prefix
        self.EOL = EOL

    def line(self,msg):
        """ For single message """
        if isinstance(msg,pd.DataFrame):
            if self.fmt=='md':
                lineout = "  \n"
                lineout += '| ' + ' | '.join([k for k in msg.keys()]) + ' |\n'
                lineout += " | :----"*len(msg.keys()) + ' |\n'
                for row in range(len(msg)):
                    lineout += '| ' + ' | '.join([str(item) for item in list(msg.iloc[row,:])]) + ' |\n'
                return lineout
            elif self.fmt=='html':
                txt = "<table>\n"
                # Write header
                txt += "<tr>\n"
                keys = []
                for k in msg.keys():
                    keys.append(k)
                    txt += "<th>%s</th>\n" %k
                txt += "</tr>\n"
                # Write values
                for i in range(len(msg)):
                    row = msg.iloc[i]
                    txt += "<tr>\n"
                    for k in keys:
                        txt += "<td>%s</td>\n" %row[k]
                    txt += "</tr>\n"
                txt += "</table>\n"
                return txt
            else:
                return str(msg).strip()+self.EOL
        elif isinstance(msg,np.ndarray):
            if len(msg.shape)<2:
                return str(msg).strip() + self.EOL
            else:
                if self.fmt=='md':
                    lineout = "  \n"
                    lineout += '| ' + ' | '.join(["Column "+str(i) for i in range(msg.shape[1])]) + ' |\n'
                    lineout += " | :----"*msg.shape[1] + ' |\n'
                    for row in msg:
                        lineout += '| ' + ' | '.join([str(item).strip() for item in row]) + ' |\n'
                    return lineout
                elif self.fmt=='html':
                    txt = "<table>\n"
                    # Write values
                    for row in msg:
                        txt += "<tr>\n"
                        for val in row:
                            txt += "<td>%s</td>\n" %val
                        txt += "</tr>\n"
                    txt += "</table>\n"
                    return txt
                else:
                    lineout = ""
                    for row in msg:
                        lineout += "".join([str(item).strip()+self.EOL for item in row])
                    return lineout

        elif isinstance(msg,list):
            return "".join([self.prefix+str(item).strip()+self.EOL for item in msg])
        else:
            return self.prefix+str(msg).strip()+self.EOL

    def message(self,msg):
        if isinstance(msg,list):
            return "".join([self.line(item) for item in msg])
        else:
            return self.line(msg)

    def output(self,entry):
        msg = entry.msg
        if isinstance(msg,list):
            msg[0] = " | ".join([entry.time,entry.level.upper(),entry.msg[0]])
        else:
            msg = " | ".join([entry.time,entry.level.upper(),entry.msg])
        return self.title + self.message(msg)

class LogStyle(object):
    def __init__(self,log=None):
        self.data = []
        if log is None:
            self.log = logging.getLogger(__name__)
            self.log.setLevel(logging.INFO)
        else:
            self.log = log
        self.set_style()
        self.null_style = Style()
        for level in LEVELS.keys():
            self.add_level(level)

    def set_log(self,log):
        self.log = log

    def set_style(self):
        self.style = {}
        # Markdown format
        self.style['md'] = {}
        self.style['md']['critical'] = Style("md","## CRITICAL:  \n","**","**  \n")
        self.style['md']['error'] = Style("md","### ERROR:  \n","**","**  \n")
        self.style['md']['warning'] = Style("md","**WARNING:**  \n","***","***  \n")
        self.style['md']['info'] = Style("md","INFO:  \n","","  \n")
        self.style['md']['debug'] = Style("md","Debug:  \n","","  \n")
        self.style['md']['header'] = "# LOG REPORT  \n"
        self.style['md']['footer'] = "### End Report  \n"

        # HTML format
        self.style['html'] = {}
        self.style['html']['critical'] = Style("html",'<h3 style="color:white;background-color:red;"> CRITICAL:</h3>',"","<br>")
        self.style['html']['error'] = Style("html",'<h4 style="color:red;"> ERROR:</h4>',"","<br>")
        self.style['html']['warning'] = Style("html",'<h4 style="color:blue;">WARNING:</h4>',"","<br>")
        self.style['html']['info'] = Style("html",'<br><b style="color:green;">INFO:</b><br>',"","<br>")
        self.style['html']['debug'] = Style("html","<br><b>Debug:</b><br>","","<br>")
        self.style['html']['header'] = """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        table {
            font-family: arial, sans-serif;
            border-collapse: collapse;
            width: 100%;
        }

        td, th {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }

        tr:nth-child(even) {
            background-color: #dddddd;
        }
        </style>
        <title>Log Report</title>
        </head>
        <body>
        <h2>LOG REPORT</h2>
        """
        self.style['html']['footer'] = """
        <h3>End Report </h3>
        </body>
        </html>
        """

    def add_level(self,level):
        def _fset(msg):
            entry = LogEntry(level,msg)
            self.data.append(entry)
            getattr(self.log,level)(self.null_style.message(entry.msg))
        setattr(self,level,_fset)

    def filter(self,level='info'):
        return [datum for datum in self.data \
                if LEVELS[datum.level]>=LEVELS[level]]

    def report(self,fname,fmt='md',level='info',order='time',group=None):
        """ Print a report
        """
        entries = self.filter(level=level)
        with open(fname,'w') as f:
            f.write(self.style[fmt]['header'])
            for entry in sorted(entries,key=lambda x:getattr(x,order)):
                f.write(self.style[fmt][entry.level].output(entry))
            f.write(self.style[fmt]['footer'])

if __name__=="__main__":
    # Testing
    log = LogStyle()
    log.debug("This is Debug #1.")
    log.info("This is Info #1.")
    x1D = np.array([1,2,3,4,5,6])
    log.info(["This is Info #2. The 1D array is: ",x1D])
    x2D = np.array([[1,2,3],[2,4,6],[3,6,9],[4,8,12]])
    log.error(["This is Error #1. The 2D array is:",x2D])
    log.warning("This is Warning #1. A critical error is going to occur!")
    df = pd.DataFrame(data=x2D,columns=['Union','Double','Triple'])
    log.critical(["This is Critical #1. The DataFrame is:",df])
    log.warning("This is Warning #2. Ignored the critical failure.")
    log.debug("This is Debug #2. About to end.")
    log.info("This is Info #3: Finished.")
    log.report("Test_report.md",level='debug')
    log.report("Test_report.html",fmt='html',level='debug')
