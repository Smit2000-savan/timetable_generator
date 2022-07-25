
from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect,reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout, get_user_model
from django.contrib import messages
from .models import Course, Available, Batch, Prof, Slots, P_pref, C_pref, Time_to_slot, Program
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User



# ------------------------------------- DATABASE QUERY FUNCTIONS ------------------------------------------------------- #

from django.db import connection, transaction
from pprint import pprint
cursor = connection.cursor()

def query_slot(ibatch,islot):
    cursor.execute("SELECT slot{} FROM sriapp_available where batch = '{}'".format(islot,ibatch) )
    ifavail = cursor.fetchall()
    return ifavail

def query_set_slot(islot,ibatch, iprof, icourse):
    cursor.execute("UPDATE sriapp_available SET slot{}='{} | {}' WHERE batch = '{}'".format(islot,icourse,iprof,ibatch))
    connection.commit()

def set_slot(islot, ibatch, icourse, iprof ):
    qslot = query_slot(ibatch,islot)
    # print(qslot)
    if qslot[0][0] != '0':
        return "Selected Slot Not available for {} for {}".format(icourse,ibatch)

    else :
        query_set_slot(islot,ibatch, iprof, icourse)
        return "Slot Set successfully for course {} of batch {} by {}".format(icourse,ibatch,iprof)

def get_slot(islot):
    cursor.execute("select slot{} from sriapp_available".format(islot))
    slot = cursor.fetchall()
    for i in range(0, len(slot)):
        slot[i] = slot[i][0]
    return slot

# ------------------------------------- URL RENDER FUNCTIOS -------------------------------------------------------------------------------- #

def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('cindex')
        else:
            return redirect('pindex')
    return render(request, 'homepage.html')

def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('Home')

# ------------------------------------------------- PROFESSOR VIEWS ------------------------------------------------------#

def p_login(request):

    if request.user.is_authenticated:
        if not request.user.is_superuser:
            return redirect('pindex')

    if request.method == "POST":
        u = request.POST.get('usr')
        p = request.POST.get('pass')
        user = authenticate(request,username=u, password=p)
        if user is None:
            messages.error(request, (" Please Enter valid Username and Password."))
            return redirect('plogin')
        elif user.is_superuser == False:
            login(request, user)
            return redirect('pindex')
        else:
            messages.error(request,(" {} is not a Professor Account.").format(u))
            return redirect('plogin')

        # res = Prof.objects.filter(email=u, pswrd=p).count()
        # if res == 0:
        #     messages.error(request, (" Please Enter valid Username and Password."))
        #     return redirect('plogin')
        # else:
        #     login()

    else:
        return render(request, 'professor/p_login.html')

# def index(request,**kargs):
def p_index(request):

    # CHECKING IF SOMEONE ENTERS THE SITE URL WITHOUT LOGGING IN
    if not request.user.is_authenticated :
        messages.warning(request,"You are not Logged in. Please Log in to access the page.")
        return redirect('Home')

    # CHECKING IF LOGGED IN COORDINATOR TRIES TO ACCESS PROFESSOR URL #VIA CHANGE THE URL TO /p_login/p_preferences
    if request.user.is_superuser :
        messages.error(request, "You are not allowed to enter Professor section without Professor authentication.")
        return redirect('Home')

    # print(u)
    # print(kargs)

    u = request.user.first_name

    if request.method == "POST":

        # crs = request.POST.get('dropdown1', None)
        day = request.POST.get('dropdown2',None)
        time = request.POST.get('dropdown3',None)
        if day == 'Select Day' or time == 'Select Timeslot':
            messages.error(request, "Please select Valid Option")

        else :
            # iprof = u
            old_p_pref = P_pref.objects.all().filter(prof = u).values()
            if old_p_pref[0]['cnt'] == 5:
                messages.error(request, "You have reached Preferences limit. Kindly wait for Timetable to be ready.")
            else:
                # messages.success(request, "day - {}, time - {}".format(day, time))
                temp_slot = Slots.objects.all().filter(prof = u).values()
                temp_day = day+time

                if not temp_slot.exists():
                    messages.error(request, "Sorry, Your course is not listed in this semester timetable. ")
                else:
                    old_cnt = C_pref.objects.all().filter(slt = temp_slot[0]['slt']).values()[0]['cnt']
                    C_pref.objects.all().filter(slt = temp_slot[0]['slt']).update( **{temp_day: old_c_pref[0][temp_day] + 1} )
                    P_pref.objects.filter(prof = u).update(cnt = old_p_pref[0]['cnt'] + 1)
                    messages.success(request, "your preferences are stored successfully.")

    mycourses = Course.objects.all().values()
    # allp_pref = P_pref.objects.all().values()
    # allslots = Slots.objects.all().values()
    slot1 = get_slot(1)
    slot2 = get_slot(2)
    slot3 = get_slot(3)
    slot4 = get_slot(4)
    slot5 = get_slot(5)
    slot6 = get_slot(6)
    slot7 = get_slot(7)
    slot8 = get_slot(8)

    context = {
        'mycourses' : mycourses,
        'pid' : u,
        'slot1': slot1,
        'slot2': slot2,
        'slot3': slot3,
        'slot4': slot4,
        'slot5': slot5,
        'slot6': slot6,
        'slot7': slot7,
        'slot8': slot8,
        # 'allp_pref' : allp_pref,
        # 'allslots' : allslots,
        # 'curAvailable' : available    //  TO SEND AVAILABLE TABLE TO HTML PAGE
    }

    return render(request,'professor/p_index.html', context )



# ------------------------------------------------- COORDINATOR VIEWS ------------------------------------------------------#

def c_login(request):
    # CHECKING IF SOMEONE ENTERS THE SITE URL WITHOUT LOGGING IN
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('cindex')

    # CHECKING IF LOGGED IN PROFESSOR TRIES TO ACCESS COORDINATOR URL #VIA CHANGE THE URL TO /c_index

    if request.method == 'POST':
        ur = request.POST.get('usr')
        ps = request.POST.get('pass')

        user = authenticate(request, username=ur, password=ps)
        if user is None:
            messages.error(request, (" Please enter valid username and password").format(ur))
            return redirect('clogin')
        elif user.is_superuser is True:
            login(request, user)
            return redirect('cindex')
        else:
            messages.error(request, (" {} is not a coordinator account.").format(ur))
            return redirect('clogin')

    return render(request, 'coordinator/c_login.html')

def c_index(request):
    # CHECKING IF SOMEONE ENTERS THE SITE URL WITHOUT LOGGING IN
    if not request.user.is_authenticated :
        messages.warning(request,"You are not Logged in. Please Log in to access the page.")
        return redirect('Home')

    # CHECKING IF LOGGED IN PROFESSOR TRIES TO ACCESS COORDINATOR URL #VIA CHANGE THE URL TO /c_index
    if not request.user.is_superuser :
        messages.error(request, "You are not allowed to enter coordinator section without coordinator authentication.")
        return redirect('Home')

    if request.method == 'POST':
        slt_change = request.POST.get('dropdown11')
        slt_with = request.POST.get('dropdown21')
        day_change = request.POST.get('dropdown12')
        day_with = request.POST.get('dropdown22')
        time_change = request.POST.get('dropdown13')
        time_with = request.POST.get('dropdown23')

        if slt_change=='select' or slt_with == 'select' or day_change=='select' or day_with == 'select' or time_change=='select' or time_with == 'select':
            messages.error(request, "Please enter valid details. You have entered wrong data")
        else:
            temp_change = day_change+time_change
            temp_with = day_with+time_with

            check_change = Time_to_slot.objects.all().filter(time = temp_change).values()
            check_with = Time_to_slot.objects.all().filter(time = temp_with).values()

            if check_with[0]['slt'] == slt_with and check_change[0]['slt'] == slt_change and check_change[0]['slt'] != check_with[0]['slt']:
                Time_to_slot.objects.all().filter(time = temp_change).update(slt = slt_with)
                Time_to_slot.objects.all().filter(time = temp_with).update(slt = slt_change)
                messages.success(request, "Slot changed successfully")
            else :
                messages.error(request, "Please enter valid details. You have entered wrong data")

    u = request.user.first_name
    tot_batch = []
    for batch in Batch.objects.all().values():
        tot_batch.append({'bname': batch['bname'], 'colspan': 1})
    days = ['mn', 'tu', 'wd', 'th', 'fr']
    times = ['8', '10', '12']

    time_table = {}
    batch = {}
    for time in times:
        curr_time_table = []
        # max_len = {}
        for day in days:
            curr_day_table = []
            for batch in tot_batch:
                curr_t = day + time
                time_slt = Time_to_slot.objects.all().filter(time=curr_t).values()[0]
                slot = list(Slots.objects.all().filter(slt=time_slt['slt'], bname=batch['bname']).values())
                curr_day_table.append(slot)
            curr_time_table.append(curr_day_table)
        n = len(tot_batch)
        curr_batch = []
        for i in range(n):
            max_len = 0
            curr_batch.append(tot_batch[i])
            for ee in range(len(days)):
                max_len = max(max_len, len(curr_time_table[ee][i]))
            for j in range(len(days)):
                while len(curr_time_table[j][i]) < max_len:
                    curr_time_table[j][i].append(' ')
            for i in range(max_len - 1):
                curr_batch.append(' ')
        time_table[time] = curr_time_table
        batch[time] = curr_batch

    all_pref = C_pref.objects.all().values()

    context = {
        'cfname' : u,
        'allcpref' : all_pref,
        'batch': batch,
        'time_table': time_table,
        'mn8': 0,
        'tu8': 0,
        'wd8': 0,
        'th8': 0,
        'fr8': 0,
        'mn10': 0,
        'tu10': 0,
        'wd10': 0,
        'th10': 0,
        'fr10': 0,
        'mn12': 0,
        'tu12': 0,
        'wd12': 0,
        'th12': 0,
        'fr12': 0,
    }

    for i in Time_to_slot.objects.all().values():
        context[i['time']] = i['slt']

    return render(request, 'coordinator/c_index.html', context)


# ------------------------------------------------- #### COURSES PAGES ####------------------------------------------------------#
def c_course(request):

    if not request.user.is_authenticated :
        messages.warning(request,"You are not Logged in. Please Log in to access the page.")
        return redirect('Home')

    # CHECKING IF LOGGED IN PROFESSOR TRIES TO ACCESS COORDINATOR URL #VIA CHANGE THE URL TO /c_index
    if not request.user.is_superuser :
        messages.error(request, "You are not allowed to enter coordinator section without coordinator authentication.")
        return redirect('Home')

    courseDetails = Course.objects.all().order_by('branch').values()
    allbatch = Batch.objects.all().values()
    context = {
        'allCourses' : courseDetails,
        'allbatches' : allbatch,
    }
    return render(request, 'coordinator/course_detail.html',context)

def c_addCourse(request):

    if not request.user.is_authenticated :
        messages.warning(request,"You are not Logged in. Please Log in to access the page.")
        return redirect('Home')

    # CHECKING IF LOGGED IN PROFESSOR TRIES TO ACCESS COORDINATOR URL #VIA CHANGE THE URL TO /c_index
    if not request.user.is_superuser :
        messages.error(request, "You are not allowed to enter coordinator section without coordinator authentication.")
        return redirect('Home')

    allbatch = Batch.objects.all().values()
    context = {
        'selectbatches' : allbatch,
    }
    return render(request, 'coordinator/add_course.html', context)

def c_courseRecord(request):

    if not request.user.is_authenticated :
        messages.warning(request,"You are not Logged in. Please Log in to access the page.")
        return redirect('Home')

    # CHECKING IF LOGGED IN PROFESSOR TRIES TO ACCESS COORDINATOR URL #VIA CHANGE THE URL TO /c_index
    if not request.user.is_superuser :
        messages.error(request, "You are not allowed to enter coordinator section without coordinator authentication.")
        return redirect('Home')

    course_id = request.POST.get('courseID')
    course_name = request.POST.get('courseName')
    # course_batch = request.POST.get('batch')
    course_batch = request.POST.get('selectbatch')
    course_type = request.POST.get('selecttype')

    if course_id != "" and course_batch != "" and course_name != "":
        olddata_course = Course.objects.all().filter(cid = course_id, branch = course_batch)
        if olddata_course.exists():
            messages.error(request, "Course {} is already enrolled in {} batch".format(course_id,course_batch))
        else:
            curCourse = Course(cid=course_id, cname=course_name, branch = course_batch, type=course_type)
            curCourse.save()
            messages.success(request, "Course '{}' Added to the batch '{}' Scuccessfully".format(course_id, course_batch))
    else:
        messages.error(request, "Please Enter Valid Fields")
        return redirect('addCourse')

    return redirect('ccourse')

def c_deleteCourse(request, id):
    if not request.user.is_authenticated :
        messages.warning(request,"You are not Logged in. Please Log in to access the page.")
        return redirect('Home')

    # CHECKING IF LOGGED IN PROFESSOR TRIES TO ACCESS COORDINATOR URL #VIA CHANGE THE URL TO /c_index
    if not request.user.is_superuser :
        messages.error(request, "You are not allowed to enter coordinator section without coordinator authentication.")
        return redirect('Home')

    try:
        curCourse = Course.objects.get(id=id)
        curCourse.delete()
        messages.success(request, "Course deleted Successfully")

    except Course.DoesNotExist:
        messages.error(request, "Course can't be deleted. Maybe it is not Exist")

    return redirect('ccourse')


# ------------------------------------------------- #### Batch PAGES ####------------------------------------------------------#

def c_batch(request):
    if not request.user.is_authenticated :
        messages.warning(request,"You are not Logged in. Please Log in to access the page.")
        return redirect('Home')

    # CHECKING IF LOGGED IN PROFESSOR TRIES TO ACCESS COORDINATOR URL #VIA CHANGE THE URL TO /c_index
    if not request.user.is_superuser :
        messages.error(request, "You are not allowed to enter coordinator section without coordinator authentication.")
        return redirect('Home')

    batchDetails = Batch.objects.all().order_by('bname').values()
    context = {
        'allBatches' : batchDetails,
    }
    return render(request, 'coordinator/batch_detail.html', context)

@csrf_exempt
def c_addBatch(request):
    if not request.user.is_authenticated :
        messages.warning(request,"You are not Logged in. Please Log in to access the page.")
        return redirect('Home')

    # CHECKING IF LOGGED IN PROFESSOR TRIES TO ACCESS COORDINATOR URL #VIA CHANGE THE URL TO /c_index
    if not request.user.is_superuser :
        messages.error(request, "You are not allowed to enter coordinator section without coordinator authentication.")
        return redirect('Home')

    allProgs = Program.objects.all().order_by('pname').values()
    context = {
        'selectprogs' : allProgs,
    }

    return render(request, 'coordinator/add_batches.html',context)

def c_bacthRecord(request):
    if not request.user.is_authenticated :
        messages.warning(request,"You are not Logged in. Please Log in to access the page.")
        return redirect('Home')

    # CHECKING IF LOGGED IN PROFESSOR TRIES TO ACCESS COORDINATOR URL #VIA CHANGE THE URL TO /c_index
    if not request.user.is_superuser :
        messages.error(request, "You are not allowed to enter coordinator section without coordinator authentication.")
        return redirect('Home')

    # batch_name = request.POST.get('batchName')
    prog_year = request.POST.get('Year')
    prog_name = request.POST.get('selectprog')

    batch_data = prog_name + " " + prog_year
    if prog_name != "" and prog_year != "":
        olddata_batch_name = Batch.objects.all().filter(bname = batch_data).values()

        if olddata_batch_name.exists():
            messages.error(request, "{} batch is already enrolled".format(batch_data))
        else:
            curBatch = Batch(bname=batch_data)
            curBatch.save()
            messages.success(request, "Batch '{}' Added Successfully".format(batch_data))
    else:
        messages.error(request, "Please Enter Valid Fields")
        return redirect('addBatch')

    return HttpResponseRedirect(reverse('cbatch'))

def c_deleteBatch(request, id):
    if not request.user.is_authenticated :
        messages.warning(request,"You are not Logged in. Please Log in to access the page.")
        return redirect('Home')

    # CHECKING IF LOGGED IN PROFESSOR TRIES TO ACCESS COORDINATOR URL #VIA CHANGE THE URL TO /c_index
    if not request.user.is_superuser :
        messages.error(request, "You are not allowed to enter coordinator section without coordinator authentication.")
        return redirect('Home')

    try:
        curBatch = Batch.objects.get(id=id)
        curBatch.delete()
        messages.success(request, "Batch deleted Successfully")

    except Batch.DoesNotExist:
        messages.error(request, "Batch can't be deleted. Maybe it is not Exist")

    return HttpResponseRedirect(reverse('cbatch'))


# ------------------------------------------------- #### Faculty PAGES ####------------------------------------------------------#

def c_facultyDetails(request):
    if not request.user.is_authenticated :
        messages.warning(request,"You are not Logged in. Please Log in to access the page.")
        return redirect('Home')

    # CHECKING IF LOGGED IN PROFESSOR TRIES TO ACCESS COORDINATOR URL #VIA CHANGE THE URL TO /c_index
    if not request.user.is_superuser :
        messages.error(request, "You are not allowed to enter coordinator section without coordinator authentication.")
        return redirect('Home')

    # u = User.objects.all().values()
    u = User.objects.all().exclude(is_superuser = True).order_by('first_name')

    # facultyDetails = Prof.objects.all().values()
    context = {
        'allFaculty' : u,
    }
    return render(request, 'coordinator/faculty_detail.html',context)

@csrf_exempt
def c_addFaculty(request):
    if not request.user.is_authenticated :
        messages.warning(request,"You are not Logged in. Please Log in to access the page.")
        return redirect('Home')

    # CHECKING IF LOGGED IN PROFESSOR TRIES TO ACCESS COORDINATOR URL #VIA CHANGE THE URL TO /c_index
    if not request.user.is_superuser :
        messages.error(request, "You are not allowed to enter coordinator section without coordinator authentication.")
        return redirect('Home')

    return render(request, 'coordinator/add_faculty.html')

@csrf_exempt
def c_facultyRecord(request):

    if not request.user.is_authenticated :
        messages.warning(request,"You are not Logged in. Please Log in to access the page.")
        return redirect('Home')

    # CHECKING IF LOGGED IN PROFESSOR TRIES TO ACCESS COORDINATOR URL #VIA CHANGE THE URL TO /c_index
    if not request.user.is_superuser :
        messages.error(request, "You are not allowed to enter coordinator section without coordinator authentication.")
        return redirect('Home')

    fname = request.POST.get('firstName')
    lname = request.POST.get('lastName')
    email_id = request.POST.get('emailID')
    password_faculty = request.POST.get('passwordFaculty')

    # courseID courseName credit  batch
    # curFaculty = Prof(fname=first_name, lname=last_name, email=email_id, pswrd=password_faculty)
    # curFaculty.save()
    if fname != "" and lname != "" and email_id != "" and password_faculty != "" :
        olddata_user = User.objects.all().filter(username = email_id).values()
        if olddata_user.exists():
            messages.error(request, "This account is already enrolled.")
        else:
            u = User.objects.create_user(username=email_id, password=password_faculty, first_name=fname, last_name=lname, email=email_id)
            temp = P_pref(prof= fname, cnt = 0)
            temp.save()
            messages.success(request, "Account Added Successfully for '{} {}'".format(fname,lname))
    else:
        messages.error(request, "Please Enter Valid Fields")
        return redirect('addFaculty')

    return HttpResponseRedirect(reverse('cfacultyDetails'))

@csrf_exempt
def c_deleteFaculty(request, id):
    if not request.user.is_authenticated :
        messages.warning(request,"You are not Logged in. Please Log in to access the page.")
        return redirect('Home')

    # CHECKING IF LOGGED IN PROFESSOR TRIES TO ACCESS COORDINATOR URL #VIA CHANGE THE URL TO /c_index
    if not request.user.is_superuser :
        messages.error(request, "You are not allowed to enter coordinator section without coordinator authentication.")
        return redirect('Home')

    try:
        # u = User.objects.get(id = id )
        # p = P_pref.objects.get(prof = u.first_name)
        # p.delete()
        # u.delete()
        u = User.objects.get(id = id)
        u.delete()
        messages.success(request, "Account deleted Successfully")
        # print("user deleted")

    except User.DoesNotExist:
        messages.error(request, "Account can't be deleted Maybe it is not Exist")
        # print("user not exist")

    # curFaculty = Prof.objects.get(id=id)
    # curFaculty.delete()
    return HttpResponseRedirect(reverse('cfacultyDetails'))

def c_faculty_pref(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You are not Logged in. Please Log in to access the page.")
        return redirect('Home')

    if not request.user.is_superuser:
        messages.error(request, "You are not allowed to enter coordinator section without coordinator authentication.")
        return redirect('Home')

    allp_pref = P_pref.objects.all().order_by('-cnt').values()
    context = {
        'allp_pref' : allp_pref
    }
    return render(request, 'coordinator/faculty_pref.html', context)

# ------------------------------------------------- #### Slot PAGES ####------------------------------------------------------#

def c_slot(request):
    if not request.user.is_authenticated :
        messages.warning(request,"You are not Logged in. Please Log in to access the page.")
        return redirect('Home')

    # CHECKING IF LOGGED IN PROFESSOR TRIES TO ACCESS COORDINATOR URL #VIA CHANGE THE URL TO /c_index
    if not request.user.is_superuser :
        messages.error(request, "You are not allowed to enter coordinator section without coordinator authentication.")
        return redirect('Home')

    slotDetails = Slots.objects.all().order_by('slt','bname').values()
    slotnumbers = [1,2,3,4,5,6,7,8]
    context = {
        'allslots' : slotDetails,
        'slotnumbers' : slotnumbers,
    }
    return render(request, 'coordinator/slots_detail.html',context)

def c_add_slot(request):
    if not request.user.is_authenticated :
        messages.warning(request,"You are not Logged in. Please Log in to access the page.")
        return redirect('Home')

    # CHECKING IF LOGGED IN PROFESSOR TRIES TO ACCESS COORDINATOR URL #VIA CHANGE THE URL TO /c_index
    if not request.user.is_superuser :
        messages.error(request, "You are not allowed to enter coordinator section without coordinator authentication.")
        return redirect('Home')

    allcourse = Course.objects.all().order_by('branch').values()
    allprof = User.objects.all().exclude(is_superuser = True).order_by('first_name')
    allslot = [1,2,3,4,5,6,7,8]
    allbatches = Batch.objects.all().values().order_by('bname')
    context = {
        'selectcourses' : allcourse,
        'selectprofs' : allprof,
        'selectslots' : allslot,
        'allbacthes' : allbatches,
    }
    return render(request, 'coordinator/add_slots.html', context)

def c_slotRecord(request):

    if not request.user.is_authenticated :
        messages.warning(request,"You are not Logged in. Please Log in to access the page.")
        return redirect('Home')

    # CHECKING IF LOGGED IN PROFESSOR TRIES TO ACCESS COORDINATOR URL #VIA CHANGE THE URL TO /c_index
    if not request.user.is_superuser :
        messages.error(request, "You are not allowed to enter coordinator section without coordinator authentication.")
        return redirect('Home')

    _slot = request.POST.get('selectslot')
    _prof = request.POST.get('selectprof')
    _course_batch = request.POST.get('selectcourse')

    _course_type = request.POST.get('selecttype')
    # print(_course_type)

    _course = _course_batch[:5]
    _batch = _course_batch[6:]

    if _slot != "" and _course != "" and _prof != "" and _batch != "":
        olddata_slot_course = Slots.objects.all().filter(cid = _course).values()
        olddata_slot_batch = Slots.objects.all().filter(bname = _batch,slt = _slot).values()
        print(olddata_slot_course)
        print(olddata_slot_batch)
        if olddata_slot_course.exists() or olddata_slot_batch.exists() :
                if olddata_slot_course.exists() and (olddata_slot_course[0]['type'] == "core" or olddata_slot_course[0]['type']==_course_type) :
                    messages.error(request, "Batch is not available at that time or course is already taken in different slot")
                else:
                    curSlot = Slots(cid=_course, type = _course_type, bname=_batch, slt=_slot, prof=_prof)
                    curSlot.save()
                    messages.success(request, "Slot '{}' Added Scuccessfully".format(_slot))
        else:
            curSlot = Slots(cid=_course, type = _course_type, bname=_batch, slt=_slot, prof=_prof)
            curSlot.save()
            messages.success(request, "Slot '{}' Added Scuccessfully".format(_slot))
    else:
        messages.error(request, "Please Enter Valid Fields")
        return redirect('caddslot')

    return redirect('cslot')

def c_deleteSlot(request, id):
    if not request.user.is_authenticated :
        messages.warning(request,"You are not Logged in. Please Log in to access the page.")
        return redirect('Home')

    # CHECKING IF LOGGED IN PROFESSOR TRIES TO ACCESS COORDINATOR URL #VIA CHANGE THE URL TO /c_index
    if not request.user.is_superuser :
        messages.error(request, "You are not allowed to enter coordinator section without coordinator authentication.")
        return redirect('Home')

    try:
        curSlot = Slots.objects.get(id=id)
        curSlot.delete()
        messages.success(request, "Slot deleted Successfully")

    except Course.DoesNotExist:
        messages.error(request, "Slot can't be deleted. Maybe it is not Exist")

    return redirect('cslot')

# ------------------------------------------------- #### Program PAGES ####------------------------------------------------------#

def c_prog(request):
    if not request.user.is_authenticated :
        messages.warning(request,"You are not Logged in. Please Log in to access the page.")
        return redirect('Home')

    # CHECKING IF LOGGED IN PROFESSOR TRIES TO ACCESS COORDINATOR URL #VIA CHANGE THE URL TO /c_index
    if not request.user.is_superuser :
        messages.error(request, "You are not allowed to enter coordinator section without coordinator authentication.")
        return redirect('Home')

    progDetails = Program.objects.all().order_by('pname').values()
    context = {
        'allProgs' : progDetails,
    }
    return render(request, 'coordinator/program_detail.html', context)

@csrf_exempt
def c_addProg(request):
    if not request.user.is_authenticated :
        messages.warning(request,"You are not Logged in. Please Log in to access the page.")
        return redirect('Home')

    # CHECKING IF LOGGED IN PROFESSOR TRIES TO ACCESS COORDINATOR URL #VIA CHANGE THE URL TO /c_index
    if not request.user.is_superuser :
        messages.error(request, "You are not allowed to enter coordinator section without coordinator authentication.")
        return redirect('Home')

    return render(request, 'coordinator/add_progs.html')

def c_progRecord(request):
    if not request.user.is_authenticated :
        messages.warning(request,"You are not Logged in. Please Log in to access the page.")
        return redirect('Home')

    # CHECKING IF LOGGED IN PROFESSOR TRIES TO ACCESS COORDINATOR URL #VIA CHANGE THE URL TO /c_index
    if not request.user.is_superuser :
        messages.error(request, "You are not allowed to enter coordinator section without coordinator authentication.")
        return redirect('Home')

    prog_name = request.POST.get('progName')

    if prog_name != "":
        olddata_prog_name = Program.objects.all().filter(pname = prog_name).values()

        if olddata_prog_name.exists():
            messages.error(request, "{} Program is already enrolled".format(prog_name))
        else:
            curProg = Program(pname=prog_name)
            curProg.save()
            messages.success(request, "Porgram '{}' Added Successfully".format(prog_name))
    else:
        messages.error(request, "Please Enter Valid Fields")
        return redirect('addProg')

    return HttpResponseRedirect(reverse('cprog'))

def c_deleteProg(request, id):
    if not request.user.is_authenticated :
        messages.warning(request,"You are not Logged in. Please Log in to access the page.")
        return redirect('Home')

    # CHECKING IF LOGGED IN PROFESSOR TRIES TO ACCESS COORDINATOR URL #VIA CHANGE THE URL TO /c_index
    if not request.user.is_superuser :
        messages.error(request, "You are not allowed to enter coordinator section without coordinator authentication.")
        return redirect('Home')

    try:
        curProg = Program.objects.get(id=id)
        curProg.delete()
        messages.success(request, "Program deleted Successfully")

    except Program.DoesNotExist:
        messages.error(request, "Program can't be deleted. Maybe it is not Exist")

    return HttpResponseRedirect(reverse('cprog'))

# ------------------------------------------------- TEMPORARY VIEWS ------------------------------------------------------#

def Timetable(request):


    # if not request.user.is_authenticated:
    #     return redirect('p_login_user')

    # c = Course.objects.all().filter(branch = 'B.tech 1').update(branch = 'B.tech-ICT 2022 I')
    s = Course.objects.all().filter(branch = 'M.tech 1').update(branch = 'M.tech 2021 I')
    slot1 = get_slot(1)
    slot2 = get_slot(2)
    slot3 = get_slot(3)
    slot4 = get_slot(4)
    slot5 = get_slot(5)
    slot6 = get_slot(6)
    slot7 = get_slot(7)
    slot8 = get_slot(8)



    allslot = Available.objects.all().values()
    # context = {
    #     'allslots' : allslot,
    #     'slot1': slot1,
    #     'slot2': slot2,
    #     'slot3': slot3,
    #     'slot4': slot4,
    #     'slot5': slot5,
    #     'slot6': slot6,
    #     'slot7': slot7,
    #     'slot8': slot8
    # }

    temp_all_slots = []
    slot_lengths_batch = {
        '8': {

        },
        '10': {

        }, '12': {

        }
    }

    allbatch = Batch.objects.all().values()
    for i in Time_to_slot.objects.all().values():
        temp_slot = {i['time']: Slots.objects.all().filter(slt=i['slt']).order_by('bname').values()}
        temp_all_slots.append(temp_slot)
        curr_slot = Slots.objects.all().filter(slt=i['slt']).order_by('bname').values()
        for b_slot in curr_slot:
            if slot_lengths_batch[i['time'][2:]].get(b_slot['bname']) is not None and slot_lengths_batch[i['time'][2:]][
                b_slot['bname']].get(i['time'][0:2]) is not None:
                slot_lengths_batch[i['time'][2:]][b_slot['bname']][i['time'][0:2]] += 1
            elif slot_lengths_batch[i['time'][2:]].get(b_slot['bname']) is not None:
                slot_lengths_batch[i['time'][2:]][b_slot['bname']][i['time'][0:2]] = 1
            else:
                slot_lengths_batch[i['time'][2:]][b_slot['bname']] = {i['time'][0:2]: 1}
    slot_batch_max = {
        '8': {},
        '10': {},
        '12': {}
    }
    for key, value in slot_lengths_batch.items():
        for key1, value1 in value.items():
            slot_batch_max[key][key1] = max(value1.values())
        # slot_batch_max[key] = max(value.values())
    print(slot_lengths_batch)
    print(slot_batch_max)
    allcpref = C_pref.objects.all().values()
    alltimetoslot = Time_to_slot.objects.all().values()


    # context = {
    #     'cfname': u,
    #
    #     'allcpref': allcpref,
    #     'temp_all_slot': temp_all_slots,
    #     'allbatch' : allbatch,
    #     'slot_batch_max': slot_batch_max,
    #     # 'alltimetoslot': alltimetoslot,
    #     # 'allslot': allslot,
    #
    #     'mn8': 0,
    #     'tu8': 0,
    #     'wd8': 0,
    #     'th8': 0,
    #     'fr8': 0,
    #     'mn10': 0,
    #     'tu10': 0,
    #     'wd10': 0,
    #     'th10': 0,
    #     'fr10': 0,
    #     'mn12': 0,
    #     'tu12': 0,
    #     'wd12': 0,
    #     'th12': 0,
    #     'fr12': 0,
    # }

    # for i in alltimetoslot:
    #     context[i['time']] = i['slt']
    # print(context)

    # Dict = {1: 'Geeks', 2: 'For', 3: 'Geeks'}
    allDays = {
        'Monday': 'mn',
        'Tuesday': 'tu',
        'Wednesday': 'wd',
        'Thursday': 'th',
        'Friday': 'fr'
    }

    # Var = ["Geeks", "for", "Geeks"]
    allBatches = Batch.objects.all.values()
    allSlots = Slots.objects.all.values()
    timeToSlot = Time_to_slot.objects.all.values()

    context = {
        'allSlots': allSlots,
        'timeToSlot': timeToSlot,
        'allBatches' : allBatches,
        'mn8': 0,
        'tu8': 0,
        'wd8': 0,
        'th8': 0,
        'fr8': 0,
        'mn10': 0,
        'tu10': 0,
        'wd10': 0,
        'th10': 0,
        'fr10': 0,
        'mn12': 0,
        'tu12': 0,
        'wd12': 0,
        'th12': 0,
        'fr12': 0
    }

    for i in alltimetoslot:
        context[i['time']] = i['slt']
    print(context)

    return render(request, 'timetable/TIMETABLE.html',context, allDays)



















# ------------------------------------- ALGO FUNCTIONS ----------------------------------------------------------------- #
#
# rows, cols = (8, 8)
# available = [[str(0) for i in range(cols)] for j in range(rows)]
# batches = dict()
#
# batches["B1"] = 0
# batches["B2"] = 1
# batches["B3"] = 2
# batches["B4"] = 3
# batches["M1"] = 4
# batches["M2"] = 5
# batches["MS1"] = 6
# batches["MS2"] = 7
#
#
# def code():
#     prof = input("enter professor name :")
#     course = input("enter professor course :")
#     slot = int(input("enter professor slot :"))
#     batch = input("enter professor batch :")
#
#     slot = slot - 1
#
#     ind = batches[batch]
#
#     if available[ind][slot] != "0":
#         print(batch + " NOT AVAILABALE AT " + str(slot + 1))
#         return
#     else:
#         tmp = course + "|" + prof
#         available[ind][slot] = tmp
#         # print(str(ind) + " " + str(slot))
#         print(tmp + " succesfully added")
#
#
# def algo_main():
#     tc = int(input("ENTER THE TESTCASES :"))
#
#     while tc != 0:
#         code()
#         tc = tc - 1
#
#     for i in range(rows):
#         for j in range(cols):
#             print(available[i][j], end=" ")
#         print()
