from datetime import datetime
from flask import url_for, render_template, redirect, request, flash, Blueprint
from flask_login import current_user, login_required

from tsdashboard import db, scheduler
from tsdashboard.utile.siem import Qradar, QradarInterface, QradarConfig

###############################
### FUNKCIJE KI JIH KLIČEMO ###
###############################

def testfunction1(): pass
    # print("DELA")
    # print(datetime.now())


def updateQradar(): pass
def updateMcafee(): pass
def updateSplunk(): pass

###################################
### TASKI, KI SE VEDNO IZVAJAJO ###
###################################

@scheduler.task('cron', id='do_testfunc', minute='*')
def testfunc():
    print("1-----------------------------------------------")
    print("Scheduler task dela", datetime.now())
    print("2-----------------------------------------------")

# ZA PREVERBO, ČE JE KAKŠEN NOV OFFENSE V QRADAR-JU
class QradarTasks:
    def checkQradar(api_ime, api_kluc, api_url, api_dostop):
        if_new = QradarConfig(api_ime, api_kluc, api_url, api_dostop)
        if_new.checkIfNew()
    
    def __call__(self):
        print("TEST TEST TEST")
