from .models import Report
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .report_to_pdf import convert



class query_bot:

    def get_available_reports(self, user):
        group = Group.objects.get(name="SiteManage")
        if group in user.groups.all():
            return Report.objects.all()

        groups = user.groups.all()
        all_reports = set()
        for g in groups:
            group_reports = g.report_set.all()
            for r in group_reports:
                all_reports.add(r)

        public_reports = Report.objects.filter(isprivate=False)
        for r in public_reports:
            all_reports.add(r)
        return all_reports

    def return_all_reports(self, user):
        all_reports = self.get_available_reports(user)

        payload = "report id|report title\n"
        for r in all_reports:
            data = str(r.pk).rjust(9) + "|" + str(r) + "\n"
            payload += data
        payload = payload.rstrip()
        return HttpResponse(payload, content_type="text/plain")

    def return_report_bundle(self, user, report_id):
        groups = user.groups.all()
        available_report_ids = []
        for g in groups:
            group_reports = g.report_set.all()
            for r in group_reports:
                available_report_ids.append(r.pk)
        public_reports = Report.objects.filter(isprivate=False)
        for r in public_reports:
            available_report_ids.append(r.pk)


        if int(report_id) in available_report_ids:
            print("report available")
            report = Report.objects.get(pk=report_id)
            payload = report.return_info() + "\n"

            attachments = report.attachment_set.all()
            count = 1
            for a in attachments:
                if count > 1:
                    payload += "\n"
                payload += "* Attachment #%d, File size: %d bytes, Filename: %s" % (count, a.file.size, a.file.name)

                count += 1
            payload = payload.rstrip()
            return HttpResponse(payload, content_type="text/plain")
        else:
            response = HttpResponse("Invalid report id")
            response.status_code = 403
            return response

    def return_report_download(self, user, report_id):
        all_reports = self.get_available_reports(user)
        try:
            report = Report.objects.get(pk=report_id)
            if report in all_reports:
                print("report found")
            else:
                response = HttpResponse("Invalid report id")
                response.status_code = 403;
                return response
        except Report.DoesNotExist:
            response = HttpResponse("Invalid report id")
            response.status_code = 403;
            return response
        return convert(report)

    def return_attachment_download(self, user, report_id, attachment_id):
        print(report_id)
        if attachment_id.isdigit():
            attachment_id = int(attachment_id)-1
        else:
            response = HttpResponse("Invalid attachment id")
            response.status_code = 403;
            return response
        try:
            report = Report.objects.get(pk=report_id)
            all_reports = self.get_available_reports(user)
            found = False
            for r in all_reports:
                if r.report_name == report.report_name:
                    found = True
            if found:
                pass
            else:
                response = HttpResponse("Invalid report id")
                response.status_code = 403;
                return response

            attachments = report.attachment_set.all()
            if attachment_id >= len(attachments) or attachment_id < 0:
                response = HttpResponse("Invalid attachment number")
                response.status_code = 403;
                return response
            else:
                attachment = attachments[attachment_id]
                print(attachment.file.name)
                filename = attachment.file.name.split('/')[-1]
                response = HttpResponse(attachment.file, content_type='text/plain')
                response['Content-Disposition'] = 'attachment; filename=%s' % filename
                response.status_code = 200
                return response
        except Report.DoesNotExist:
            response = HttpResponse("Invalid report id")
            response.status_code = 403;
            return response
