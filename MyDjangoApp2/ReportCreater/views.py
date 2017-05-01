from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .report_to_pdf import convert
from .models import ReportForm, Report, Attachment
from django.contrib.auth.models import Group
from django.utils.html import escape
from django.contrib.auth.models import User
import re
import datetime
from .query_lib import query_bot

# Create your views here.
def download(request, report_id):
    try:
        report = Report.objects.get(pk=report_id)
    except Report.DoesNotExist:
        return Http404("Report does not exist")
    return convert(report)

query_dict = {
        '1':'View All Reports Available',
        '2':'View Report and Attatchments',
        '3':'Download Report',
        '4':'Download Attachment',
        '5':'Download Report and All Attachments',
        '6':'Download All Attachments',
        '7':'Encrypt File',
        '8':'Decrypt File',
        'q':'Quit'
}
def query_handler(request, query_id, extra_id1=0, extra_id2=0):
    user = request.user
    if not user.is_authenticated():
        return HttpResponse("Invalid User")

    if query_id not in list(query_dict.keys()):
        return HttpResponse("Invalid query request")

    qb = query_bot()
    if query_id == '1':
        reports = qb.return_all_reports(user)
        return reports
    elif query_id == '2':
        report_id = extra_id1
        report_bundle = qb.return_report_bundle(user,report_id)
        return report_bundle
    elif query_id == '3':
        report_id = extra_id1
        download = qb.return_report_download(user,report_id)
        return download
    elif query_id == '4':
        print("query received")
        report_id = extra_id1
        attachment_id = extra_id2
        download = qb.return_attachment_download(user,report_id,attachment_id)
        return download
    elif query_id == '5':
        pass
    elif query_id == '6':
        pass
    elif query_id == '7':
        pass
    elif query_id == '8':
        pass

def form(request):
    isFailure = ""
    # if this is a POST request we need to process the form data
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    if not request.user.profile.company:
        isFailure = "You do not have the priviledge to make reports"
        return render(request, 'fail.html', {
            'failure': isFailure,
        })
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:\
        print('add report')
        print(request.POST)
        form = ReportForm(request.POST)
        print(request.FILES)
        form.attachments = request.FILES
        groups = request.POST.getlist('Groups')
        isprivate = request.POST.get('isprivate')

        if form.is_valid():
            print('valid form')
            report_data = form.cleaned_data
            print(report_data)
            del report_data['groups']
            del report_data['file_field']
            report = Report(**report_data)
            report.save()
            report.set_hash()
            files = request.FILES.getlist('file_field')
            if len(files) > 0:
                print("%d files uploaded" % len(files))
                seqid = 1
                for f in files:
                    a = report.attachment_set.create(file=f, seqid=seqid)
                    seqid += 1
                    a.set_hash()
                    print(f)
            else:
                print('no files uploaded')

            if isprivate and len(groups) > 0:
                for g in groups:
                    print(g)
                    group = Group.objects.get(name=g)
                    report.groups.add(group)
            else:
                print('no groups added')
            report.save()
            return convert(report)
        else:
            isFailure = "That form name has already been taken. Please try again."
            return render(request, 'report_form.html', {
                'form': form,
                'groups': groups,
                'failure': isFailure,
            })
        print(request.FILES)
    else:
        form = ReportForm()

    groups = request.user.groups.all()
    return render(request, 'report_form.html', {
        'form': form,
        'groups': groups,
        'failure': isFailure,
    })
def report_view(request, report_id):

    isFailure = ""
    isSiteManage = False
    user = request.user
    print(user)
    if not user.is_authenticated():
        return HttpResponseRedirect('/login/')
    qb = query_bot()
    all_reports = qb.get_available_reports(request.user)
    try:
        report = Report.objects.get(pk=report_id)
        canView = False
        for r in all_reports:
            if report.report_name == r.report_name:
                canView = True
        if canView:
            group = Group.objects.get(name="SiteManage")
            if group in request.user.groups.all():
                isSiteManage = True
            else:
                isSiteManage = False
            edit_url = "/report/edit/" + str(report.pk)

            attachments = report.attachment_set.all()
            attachments_info = []
            count = 1
            for a in attachments:
                attachments_info.append("Attachment #%d, File size: %d bytes, Filename: %s" % (count, a.file.size, a.file.name))
                count += 1
            report_query = 3
            attachment_query = 4
            return render(request, 'report_view.html',
                          {'report': report, "isSiteManage": isSiteManage, "edit_url": edit_url,
                           "attachments": attachments, "report_query":report_query,"attachment_query":attachment_query})
        else:
            print("report not allowed")
            isFailure = "You are not authorized to view this report"
            return render(request, 'fail.html', {
                'failure': isFailure,
            })
            #response = HttpResponse("You are not authorized to view this report")
            #response.status_code = 403
            #return response
    except Report.DoesNotExist:
        isFailure = "Report does not exist."
        return render(request, 'fail.html', {
            'failure': isFailure,
        })
        #response = HttpResponse("Invalid report ID")
        #response.status_code = 403
        #return response

def all_reports_view(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    #kristina to implement

    qb = query_bot()

    group = Group.objects.get(name="SiteManage")
    if group in request.user.groups.all():
        allreports = Report.objects.all()
    else:
        allreports = qb.get_available_reports(request.user)

    return render(request, 'viewreports.html', {
        'reports' : allreports,
    })
def delete_report(request, report_id):
    user = request.user
    print(user)
    if not user.is_authenticated():
        return HttpResponseRedirect('/login/')
    group = Group.objects.get(name="SiteManage")
    if not group in request.user.groups.all():
        #return HttpResponse("You can't delete reports")
        isFailure = "You can't delete reports"
        return render(request, 'fail.html', {
            'failure': isFailure,
        })
    try:
        report = Report.objects.get(pk=report_id)
        report.delete()
        return HttpResponseRedirect('/report/view')
    except Report.DoesNotExist:
        isFailure = "Invalid report ID"
        return render(request, 'fail.html', {
            'failure': isFailure,
        })
        #response = HttpResponse("Invalid report ID")
        #response.status_code = 403
        #return response

def report_edit(request, report_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    isFailure = ""
    try:
        report = Report.objects.get(pk=report_id)
    except Report.DoesNotExist:
        #return Http404("Report does not exist")
        isFailure = "Report does not exist"
        return render(request, 'fail.html', {
            'failure': isFailure,
        })
    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        #form.attachments = request.FILES
        report_groups = request.POST.getlist('Groups')
        isprivate = request.POST.get('isprivate')
        print(request.POST)
        if form.is_valid():
            print("valid form")
            report_data = form.cleaned_data

            phone_number = report_data['phone_number']
            if not re.match('^(\d{3})-(\d{3})-(\d{4})$', phone_number):
                isFailure = "Phone number must be in format xxx-xxx-xxxx. Please try again."
                return render(request, 'report_form.html', {
                    'form': form,
                    'groups': groups,
                    'failure': isFailure,
                })


            del report_data['groups']
            del report_data['file_field']

            report.report_name = report_data['report_name']
            report.company_name = report_data['company_name']
            report.phone_number = report_data['phone_number']
            report.company_location = report_data['company_location']
            report.company_country = report_data['company_country']
            report.sector = report_data['sector']
            report.industry = report_data['industry']
            report.isprivate = report_data['isprivate']
            report.groups.clear()
            if isprivate and len(report_groups) > 0:
                print(len(report_groups))
                for g in report_groups:
                    group = Group.objects.get(name=g)
                    report.groups.add(group)
            else:
                report.isprivate = False
            report.save()
            return HttpResponseRedirect('/report/view/' + report_id)
        else:
            isFailure = "That form name has already been taken. Please try again."
            return render(request, 'editreport.html', {
                'failure': isFailure,
                'report_name': report.report_name,
                'form': form,
            })
        #return HttpResponseRedirect('/fail/')
    else:
        report_groups = report.groups.all()
        user_groups = request.user.groups.all()
        form = ReportForm(instance=report)
    return render(request, 'editreport.html', {
        'failure': isFailure,
        'report_name': report.report_name,
        'form': form,
        'user_groups': user_groups,
        'report_groups': report_groups,
    })
