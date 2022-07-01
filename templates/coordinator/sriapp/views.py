
from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect,reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout, get_user_model
from django.contrib import messages
from .models import Course, Available, Batch, Prof
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User



# ------------------------------------- DATABASE QUERY FUNCTIONS ------------------------------------------------------- #

from django.db import connection, transaction
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
    # print(qslot[0][0])
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

        crs = request.POST.get('dropdown1', None)
        slt = request.POST.get('dropdown2',None)

        if crs == 'select' or slt == 'select':
            messages.error(request, "Please select Valid Option")

        else :
            parts = crs.split(",")
            islot = slt
            ibatch = parts[2]
            icourse = parts[0]
            iprof = u
                            # slot, batch, course, prof
            res = set_slot(islot, ibatch, icourse, iprof)
            messages.warning(request, res)

    mycourses = Course.objects.all().values()
    # available = Available.objects.all().values()      #TO FETCH THE AVAILABLE TABLE
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
        'slot8': slot8
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

    u = request.user.first_name
    slot1 = get_slot(1)
    slot2 = get_slot(2)
    slot3 = get_slot(3)
    slot4 = get_slot(4)
    slot5 = get_slot(5)
    slot6 = get_slot(6)
    slot7 = get_slot(7)
    slot8 = get_slot(8)

    allslot = Available.objects.all().values()
    context = {
        'cfname' : u,
        'allslots' : allslot,
        'slot1': slot1,
        'slot2': slot2,
        'slot3': slot3,
        'slot4': slot4,
        'slot5': slot5,
        'slot6': slot6,
        'slot7': slot7,
        'slot8': slot8
    }
    return render(request, 'coordinator/c_index.html',context)

#### COURSES PAGES ####
def c_course(request):

    if not request.user.is_authenticated :
        messages.warning(request,"You are not Logged in. Please Log in to access the page.")
        return redirect('Home')

    # CHECKING IF LOGGED IN PROFESSOR TRIES TO ACCESS COORDINATOR URL #VIA CHANGE THE URL TO /c_index
    if not request.user.is_superuser :
        messages.error(request, "You are not allowed to enter coordinator section without coordinator authentication.")
        return redirect('Home')

    courseDetails = Course.objects.all().order_by('branch').values()
    context = {
        'allCourses' : courseDetails,
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

    if course_id != "" and course_batch != "" and course_name != "":
        curCourse = Course(cid=course_id, cname=course_name, branch = course_batch)
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


#### BATCHES PAGES####

def c_batch(request):
    if not request.user.is_authenticated :
        messages.warning(request,"You are not Logged in. Please Log in to access the page.")
        return redirect('Home')

    # CHECKING IF LOGGED IN PROFESSOR TRIES TO ACCESS COORDINATOR URL #VIA CHANGE THE URL TO /c_index
    if not request.user.is_superuser :
        messages.error(request, "You are not allowed to enter coordinator section without coordinator authentication.")
        return redirect('Home')

    batchDetails = Batch.objects.all().values()
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

    return render(request, 'coordinator/add_batches.html')

def c_bacthRecord(request):
    if not request.user.is_authenticated :
        messages.warning(request,"You are not Logged in. Please Log in to access the page.")
        return redirect('Home')

    # CHECKING IF LOGGED IN PROFESSOR TRIES TO ACCESS COORDINATOR URL #VIA CHANGE THE URL TO /c_index
    if not request.user.is_superuser :
        messages.error(request, "You are not allowed to enter coordinator section without coordinator authentication.")
        return redirect('Home')

    batch_id = request.POST.get('batchID')
    batch_name = request.POST.get('batchName')

    if batch_id != "" and batch_name != "":
        curBatch = Batch(bid=batch_id, bname=batch_name)
        curBatch.save()
        messages.success(request, "Batch '{}' Added Successfully".format(batch_name))
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


#### FACULTY PAGES ####

def c_facultyDetails(request):
    if not request.user.is_authenticated :
        messages.warning(request,"You are not Logged in. Please Log in to access the page.")
        return redirect('Home')

    # CHECKING IF LOGGED IN PROFESSOR TRIES TO ACCESS COORDINATOR URL #VIA CHANGE THE URL TO /c_index
    if not request.user.is_superuser :
        messages.error(request, "You are not allowed to enter coordinator section without coordinator authentication.")
        return redirect('Home')

    # u = User.objects.all().values()
    u = User.objects.all().exclude(is_superuser = True)

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
        u = User.objects.create_user(username=email_id, password=password_faculty, first_name=fname, last_name=lname, email=email_id)
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

# ------------------------------------------------- TEMPORARY VIEWS ------------------------------------------------------#

def Timetable(request):

    # if not request.user.is_authenticated:
    #     return redirect('p_login_user')

    slot1 = get_slot(1)
    slot2 = get_slot(2)
    slot3 = get_slot(3)
    slot4 = get_slot(4)
    slot5 = get_slot(5)
    slot6 = get_slot(6)
    slot7 = get_slot(7)
    slot8 = get_slot(8)

    allslot = Available.objects.all().values()
    context = {
        'allslots' : allslot,
        'slot1': slot1,
        'slot2': slot2,
        'slot3': slot3,
        'slot4': slot4,
        'slot5': slot5,
        'slot6': slot6,
        'slot7': slot7,
        'slot8': slot8
    }
    # print(context)
    return render(request, 'timetable/TIMETABLE.html',context)



















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


