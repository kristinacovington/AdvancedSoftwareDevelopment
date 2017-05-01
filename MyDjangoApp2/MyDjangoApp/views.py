from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login
import urllib
# importing loading from django template
from django.template import loader
from django import forms
from .forms import RemoveMemberForm, CreateGroupForm, UserForm, UserLoginForm, UserRegistrationForm, ProfileForm, \
    SearchReportForm, ManageUserAccessForm
from .models import Profile, create_user_profile
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Permission
from .models import GroupProfile, PrivateKey, ServerKeychain, ServerKey
from django import template
from . import encrypt_lib
from ReportCreater.models import Report
from ReportCreater.query_lib import query_bot
from django.contrib.auth.models import Group
from Crypto.PublicKey import RSA
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
import re

# our view which is a function named index



def view_profile(request, user_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    template = loader.get_template('view_profile.html')

    # creating the values to pass
    user = User.objects.get(username=user_id)

    return render(request, 'view_profile.html', {
        'user_id': user_id,
        'firstname': user.first_name,
        'lastname': user.last_name,
        'bio': user.profile.bio,
        'location': user.profile.location,
        'company': user.profile.company,

    })


def group_view(request, group_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    # gid = group_id[7:-1]
    # gid = re.sub('%20', '', gid)
    # getting our template
    template = loader.get_template('group.html')
    # creating the values to pass
    context = {
        'name': 'Kristina Covington',
        'company': 'Yes',
        'group': group_id
    }
    '''
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            x = 0
    else:
        form = GroupForm()
    '''

    group_members = get_users(group_id)
    isFailure = ""

    if request.method == 'POST':

        remove_member_form = RemoveMemberForm(request.POST)
        members = request.POST['members']
        remove = request.POST['remove']
        if remove_member_form.is_valid():

            if remove == request.user.username:
                group = Group.objects.get(name=group_id)
                try:
                    group.user_set.remove(request.user)
                except User.DoesNotExist:
                    isFailure = "Can only remove self from group unless have site manage priviledges or attempting to remove a user that does not exist. Please try again."
                    return render(request, 'group.html', {
                        'group': group_id,
                        'group_members': group_members,
                        'remove_member_form': remove_member_form,
                        'failure': isFailure,
                    })
                    # return HttpResponseRedirect('/home/')
            elif remove is not "":
                site_managers = get_users("SiteManage")
                try:
                    user_to_remove = User.objects.get(username=remove)
                except User.DoesNotExist:
                    isFailure = "User attemping to remove does not exist. Please try again."
                    return render(request, 'group.html', {
                        'group': group_id,
                        'group_members': group_members,
                        'remove_member_form': remove_member_form,
                        'failure': isFailure,
                    })

                if request.user in site_managers:
                    group = Group.objects.get(name=group_id)
                    try:
                        group.user_set.remove(user_to_remove)
                    except User.DoesNotExist:
                        isFailure = "User attempting to remove does not exist. Please try again."
                        return render(request, 'group.html', {
                            'group': group_id,
                            'group_members': group_members,
                            'remove_member_form': remove_member_form,
                            'failure': isFailure,
                        })

            if members is not "":
                group = Group.objects.get(name=group_id)
                try:
                    user_to_add = User.objects.get(username=members)
                except User.DoesNotExist:
                    isFailure = "User attempting to add does not exist. Please try again."
                    return render(request, 'group.html', {
                        'group': group_id,
                        'group_members': group_members,
                        'remove_member_form': remove_member_form,
                        'failure': isFailure,
                    })
                group.user_set.add(user_to_add)
                isFailure = ""
            return HttpResponseRedirect('/home/')
        else:
            isFailure = ""

            return render(request, 'group.html', {
                'group': group_id,
                'group_members': group_members,
                'remove_member_form': remove_member_form,
                'failure': isFailure,
            })

    else:
        remove_member_form = RemoveMemberForm()

    return render(request, 'group.html', {
        'group': group_id,
        'group_members': group_members,
        'remove_member_form': remove_member_form,
        'failure': isFailure,

    })

    # rendering the template in HttpResponse
    # but this time passing the context and request
    # return HttpResponse(template.render(context, request))

    # return render(request, 'group.html', {'form': form})


# our view which is a function named index
def home(request):

    # getting our template
    template = loader.get_template('home.html')
    if not User.objects.all():
        siteManager = User.objects.create_superuser(username='administrator',
                                                    email='ksc3bu@virginia.edu',
                                                    password='administratorpassword')
        siteManager.save()
        siteManager.profile.company = True
        siteManager.profile.blockedAccess = False
        siteManager.profile.privatekey_set.create(key=b"string", name="File Encryption")
        siteManager.profile.save()
        group = Group.objects.get_or_create(name="SiteManage")[0]
        group.user_set.add(siteManager)
        group.save()
        siteManager.save()

    if not ServerKey.objects.all():
        server_keychain = ServerKeychain.objects.create(active=True, keychain_size=1)
        server_keychain.save()
        server_key = ServerKey.objects.create(name="Primary", keychain=server_keychain)
        key = RSA.generate(2048)
        privatekey = key.exportKey()
        server_key.set_key(privatekey)
        server_key.save()


    isSiteManage = False
    # group = Group.objects.get(name="SiteManage")
    allGroups = Group.objects.all()
    allUsers = User.objects.all()
    for group in request.user.groups.all():
        if group.name == "SiteManage":
            isSiteManage = True
    # creating the values to pass

    return render(request, 'home.html', {
        'siteManage': isSiteManage,
        'allGroups': allGroups,
        'allUsers': allUsers,
    })

    # rendering the template in HttpResponse
    # but this time passing the context and request

    # return HttpResponse(template.render(context, request))


def create_group(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    # getting our template
    template = loader.get_template('creategroup.html')

    # creating the values to pass
    context = {
        'name': 'Kristina Covington',
        'company': 'Yes',
        'group': 'Sample Group'
    }
    isFailure = False
    allUsers = User.objects.all()

    if request.method == 'POST':

        create_group_form = CreateGroupForm(request.POST)




        if create_group_form.is_valid():

            report_data = create_group_form.cleaned_data
            group_name = report_data["name"]
            members = report_data["members"]

            if not re.match("^[A-Za-z0-9_-]*$", group_name):
                isFailure = "Group name can only contain letters, numbers, underscores or dashes. Please try again."
                return render(request, 'creategroup.html', {
                    'create_group_form': create_group_form,
                    'failure': isFailure,
                })

            try:
                group = Group.objects.get_or_create(name=group_name)[0]
            except User.DoesNotExist:
                isFailure = "Group has already been created with that name. Please try again."
                return render(request, 'creategroup.html', {
                    'create_group_form': create_group_form,
                    'failure': isFailure,
                })
            group.save()
            group.user_set.add(request.user)
            # group.profile.index = 1
            group_profile = GroupProfile(group=group)
            try:
                group_profile.save()
            except:
                isFailure = "Group has already been created with that name. Please try again."
                return render(request, 'creategroup.html', {
                    'create_group_form': create_group_form,
                    'failure': isFailure,
                })
            # member_list = [members.strip() for x in members.split(',')]
            # for member in member_list:
            # member_list = [members.strip() for x in members.split(',')]
            # for member in member_list:

            try:
                user_to_add = User.objects.get(username=members)
                group.user_set.add(user_to_add)
            except:
                isFailure = "User does not exist. Please try again."
                return render(request, 'creategroup.html', {
                    'create_group_form': create_group_form,
                    'failure': isFailure,
                })

            return HttpResponseRedirect('/creategroup/')
        else:
            return HttpResponseRedirect('/fail/')
    else:
        create_group_form = CreateGroupForm()

    return render(request, 'creategroup.html', {
        'create_group_form': create_group_form,
        'failure': isFailure,
        'allUsers': allUsers,
    })

    # rendering the template in HttpResponse
    # but this time passing the context and request

    # return HttpResponse(template.render(context, request))


def login_user(request):
    # creating the values to pass
    context = {
        'name': 'Kristina Covington',
        'company': 'Yes',
        'group': 'Sample Group'
    }
    isFailure = False
    if request.method == 'GET':
        print("get request")
    if request.method == 'POST':
        print(request.POST)
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            print(username)
            print(password)
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None and not user.profile.blockedAccess:
                auth_login(request, user)
                isFailure = False

                return HttpResponseRedirect('/home/')
            else:
                isFailure = True

                return render(request, 'login.html', {
                    'form': form,
                    'failure': isFailure,

                })
    else:
        form = UserLoginForm()

    # rendering the template in HttpResponse
    # but this time passing the context and request

    return render(request, 'login.html', {
        'form': form,
        'failure': isFailure,
    })


def login_fda(request):
    print(request.method)
    if request.method == 'GET':
        print("get request from FDA")
        form = UserLoginForm()
        return render(request, 'login.html', {'form': form})
    elif request.method == 'POST':
        print(request.POST)
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            if password == "":
                return HttpResponse(status=403)
            print(username)
            print(password)
            user = authenticate(username=username, password=password)

            if user is not None:
                auth_login(request, user)
                keychain = ServerKeychain.objects.get(active="True")
                serverkey = keychain.serverkey_set.get(name="Primary")
                print(serverkey.get_key())
                userkey = user.profile.privatekey_set.all()
                print(userkey[0].get_key())
                encrypted_key = encrypt_lib.encrypt_string(
                    user.profile.privatekey_set.get(name="File Encryption").get_key(), password)
                return HttpResponse(status=200, content=encrypted_key)
            else:
                return HttpResponse(status=403)
        else:
            form = UserLoginForm()
            return render(request, 'login.html', {'form': form})
    else:
        form = UserLoginForm()
        return render(request, 'login.html', {'form': form})


def update_profile(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect('/home/')
        else:
            return HttpResponseRedirect('/fail/')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def logout_view(request):
    # getting our template
    template = loader.get_template('logged_out.html')

    # creating the values to pass
    context = {
        'name': 'Kristina Covington',
        'company': 'Yes',
        'group': 'Sample Group'
    }

    logout(request)
    # rendering the template in HttpResponse
    # but this time passing the context and request
    return HttpResponse(template.render(context, request))


def register_view(request):
    # getting our template
    template = loader.get_template('register.html')

    # creating the values to pass
    context = {
        'name': 'Kristina Covington',
        'company': 'Yes',
        'group': 'Sample Group'
    }
    isFailure = ""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            password = userObj['password']

            if not re.match("^[A-Za-z0-9_-]*$", username):
                isFailure = "Username can only contain letters, numbers, underscores or dashes. Please try again."
                return render(request, 'register.html', {
                    'form': form,
                    'failure': isFailure,
                })

            if len(password) < 7:
                isFailure = "Password must be at least 6 characters long. Please try again."
                return render(request, 'register.html', {
                    'form': form,
                    'failure': isFailure,
                })

            email = userObj['email']
            company = userObj['company']
            first_name = userObj['first_name']
            last_name = userObj['last_name']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                # make key
                # make user
                User.objects.create_user(username, email, password)
                user = authenticate(username=username, password=password)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                user.profile.company = company
                user.profile.blockedAccess = False
                private_key = RSA.generate(2048)
                user.profile.privatekey_set.create(key=private_key.exportKey(), name="File Encryption")
                user.profile.save()

                # login(request, user)
                # group = Group.objects.get_or_create(name=userObj['group'])[0]
                # group.save()
                # group.user_set.add(user)
                return HttpResponseRedirect('/login/')
            else:
                isFailure = "That username/email has already been taken. Please try again."
                return render(request, 'register.html', {
                    'form': form,
                    'failure': isFailure,
                })
    else:
        form = UserRegistrationForm()

    # rendering the template in HttpResponse
    # but this time passing the context and request

    return render(request, 'register.html', {

        'form': form,
        'failure': isFailure,
    })


def success(request):
    # getting our template
    template = loader.get_template('success.html')

    # creating the values to pass
    context = {
        'name': 'Kristina Covington',
        'company': 'Yes',
        'group': 'Sample Group'
    }

    # rendering the template in HttpResponse
    # but this time passing the context and request
    return HttpResponse(template.render(context, request))


def fail(request):
    # getting our template
    template = loader.get_template('fail.html')

    # creating the values to pass
    context = {
        'name': 'Kristina Covington',
        'company': 'Yes',
        'group': 'Sample Group'
    }

    # rendering the template in HttpResponse
    # but this time passing the context and request
    return HttpResponse(template.render(context, request))


def search_results(request):
    template = loader.get_template('search_results.html')
    context = {
        'name': 'Kristina Covington',
        'company': 'Yes',
        'group': 'Sample Group'
    }
    return HttpResponse(template.render(context, request))


def about_us(request):
    template = loader.get_template('aboutus.html')
    context = {
        'name': 'Kristina Covington',
        'company': 'Yes',
        'group': 'Sample Group'
    }
    return HttpResponse(template.render(context, request))


def help(request):
    template = loader.get_template('help.html')
    context = {
        'name': 'Kristina Covington',
        'company': 'Yes',
        'group': 'Sample Group'
    }
    return HttpResponse(template.render(context, request))


def search(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    if "POST" == request.method:

        form = SearchReportForm(request.POST)
        if form.is_valid():
            keyword = request.POST.get('keyword')

            # orArr = keyword.split(" or ")
            andArr = keyword.split(" AND ")
            keyword = keyword.lower()

            qb = query_bot()
            reports = qb.get_available_reports(request.user)  # can only view reports for groups you are in
            found = False
            items = list(reports)
            if keyword != "":
                for report in reports:
                    for term in andArr:
                        # report is a Report object
                        # print(report.company_name)
                        if term in report.current_projects.lower() or \
                                        term in report.company_country.lower() or \
                                        term in report.company_name.lower() or \
                                        term in report.company_location.lower() or \
                                        term in report.phone_number.lower() or \
                                        term in report.sector.lower() or \
                                        term in report.industry.lower() or \
                                        term in report.report_name.lower():
                            found = True
                        else:
                            if items.__contains__(report):
                                items.remove(report)

            if found:
                # store and pass the found file name(s)
                # display it/them in the search_results form
                return render(request, 'search.html', {'q': found, 'results': items, 'form': form})
            else:
                return render(request, 'search.html', {'q': False, 'form': form})
    else:
        #  form = loader.get_template('search.html')
        form = SearchReportForm()
        qb = query_bot()
        reports = qb.get_available_reports(request.user)
        return render(request, 'search.html', {'form': form, 'results': reports})


def get_groups(user):
    return user.groups.all()


def get_users(group_name):
    return User.objects.filter(groups__name=group_name)


register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


def site_manager(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    # getting our template
    template = loader.get_template('sitemanager.html')
    isSiteManage = False
    group = Group.objects.get(name="SiteManage")
    allGroups = Group.objects.all()
    allUsers = User.objects.all()
    if group in request.user.groups.all():
        isSiteManage = True
    # creating the values to pass
    context = {
        'siteManage': isSiteManage
    }

    if request.method == 'POST':

        create_group_form = CreateGroupForm(request.POST)
        group_name = request.POST['name']

        members = request.POST['members']

        if create_group_form.is_valid():

            group = Group.objects.get_or_create(name=group_name)[0]
            group.save()
            group.user_set.add(request.user)
            # group.profile.index = 1
            group_profile = GroupProfile(group=group)
            group_profile.save()
            # member_list = [members.strip() for x in members.split(',')]
            # for member in member_list:
            # member_list = [members.strip() for x in members.split(',')]
            # for member in member_list:
            user_to_add = User.objects.get(username=members)
            group.user_set.add(user_to_add)

            return HttpResponseRedirect('/home/')
        else:
            return HttpResponseRedirect('/fail/')
    else:
        create_group_form = CreateGroupForm()

    return render(request, 'sitemanager.html', {
        'create_group_form': create_group_form,
        'siteManage': isSiteManage,
        'allGroups': allGroups,
        'allUsers': allUsers,
    })
    # rendering the template in HttpResponse
    # but this time passing the context and request


def manage_user_access(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    # getting our template
    template = loader.get_template('manage_user_access.html')
    isSiteManage = False
    group = Group.objects.get(name="SiteManage")
    allGroups = Group.objects.all()
    allUsers = User.objects.all()
    if group in request.user.groups.all():
        isSiteManage = True
    # creating the values to pass
    context = {
        'siteManage': isSiteManage
    }
    isFailure = False
    if request.method == 'POST':

        manage_user_access_form = ManageUserAccessForm(request.POST)
        # group_name = request.POST['name']
        members = request.POST['members']
        block = request.POST['block']

        if manage_user_access_form.is_valid():

            # group = Group.objects.get_or_create(name=group_name)[0]
            # group.save()
            # group.user_set.add(request.user)
            # group.profile.index = 1
            # group_profile = GroupProfile(group=group)
            # group_profile.save()
            # member_list = [members.strip() for x in members.split(',')]
            # for member in member_list:
            # member_list = [members.strip() for x in members.split(',')]
            # for member in member_list:
            # user_to_add = User.objects.get(username=members)
            # group.user_set.add(user_to_add)

            try:
                user = User.objects.get(username=members)
            except User.DoesNotExist:
                isFailure = True
                return render(request, 'manage_user_access.html', {
                    'manage_user_access_form': manage_user_access_form,
                    'siteManage': isSiteManage,
                    'allUsers': allUsers,
                    'failure': isFailure,
                })
            if block == "Yes":
                user.profile.blockedAccess = True
            else:
                user.profile.blockedAccess = False
            user.save()
            return HttpResponseRedirect('/manageUserAccess/')
        else:
            isFailure = True
            return render(request, 'manage_user_access.html', {
                'manage_user_access_form': manage_user_access_form,
                'siteManage': isSiteManage,
                'allUsers': allUsers,
                'faillure': isFailure,
            })
    else:
        manage_user_access_form = ManageUserAccessForm()

    return render(request, 'manage_user_access.html', {
        'manage_user_access_form': manage_user_access_form,
        'siteManage': isSiteManage,
        'allUsers': allUsers,
        'faillure': isFailure,
    })
    # rendering the template in HttpResponse
    # but this time passing the context and request


def view_groups(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    template = loader.get_template('viewgroups.html')

    isSiteManage = False
    # group = Group.objects.get(name="SiteManage")
    allGroups = Group.objects.all()
    allUsers = User.objects.all()
    for group in request.user.groups.all():
        if group.name == "SiteManage":
            isSiteManage = True
    # creating the values to pass

    return render(request, 'viewgroups.html', {
        'siteManage': isSiteManage,
        'allGroups': allGroups,
        'allUsers': allUsers,
    })


def messages(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    return HttpResponseRedirect("/messageFunc/inbox")


