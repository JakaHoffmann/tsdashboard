from flask import url_for, render_template, redirect, request, flash, Blueprint
from flask_login import current_user, login_required

from tsdashboard import db, scheduler


casi  = Blueprint('timers', __name__)

@casi.route('/timers', methods=['GET'])
@login_required
def timers():
    data = {}
    jobs = scheduler.get_jobs()
    # test_tmp = scheduler.print_jobs()
    for i in range(len(jobs)):
        data[i] = {"name": jobs[i].name, "id": jobs[i].id, "trigger": jobs[i].trigger, "next_run_time": jobs[i].next_run_time, "func": jobs[i].func_ref}
        print(type(jobs[i].trigger))
    return render_template('scheduler.html', title='scheduler', name='scheduler', jobs=jobs, data=data)

@casi.route('/timers/<string:id>/pause', methods=['GET'])
def pause_timer(id):
    if id == "ALL":
        scheduler.pause()
    else:
        scheduler.pause_job(id)
    return redirect(url_for('timers.timers'))

@casi.route('/timers/<string:id>/resume', methods=['GET'])
def resume_timer(id):
    if id == "ALL":
        scheduler.resume()
    else:
        scheduler.resume_job(id)
    return redirect(url_for('timers.timers'))

@casi.route('/timers/add', methods=['GET', 'POST'])
def add_timer(): pass

@casi.route('/timers/<string:id>/edit', methods=['GET', 'POST'])
def edit_timer(id): 
    if request.method == 'POST':
        print(request.form["triggerName"])
        print(request.form["triggerTrig"])
        scheduler.modify_job(id, name=request.form["triggerName"])
        scheduler.scheduler.reschedule_job(id, trigger="cron", minute='*')
    return redirect(url_for('timers.timers'))
    
    # if request.method == 'POST': pass

@casi.route('/timers/<string:id>/delete', methods=['GET'])
def delete_timer(id):
    scheduler.remove_job(id)
    return redirect(url_for('timers.timers'))