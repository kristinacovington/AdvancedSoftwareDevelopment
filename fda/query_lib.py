import re
import os

class query_bot:

    query_url = "http://127.0.0.1:8000/report/query/"
    def get_report_id(self, report_id):
        while not report_id.isdigit():
            report_id = input("Input the numerical report ID desired or type 'q' to quit: ")
            if report_id == 'q':
                break
        return report_id

    def get_attachment_id(self, attachment_id):
        attachment_id = 'a'
        while not attachment_id.isdigit():
            attachment_id = input("Input the numerical attachment ID desired or type 'q' to quit: ")
            if attachment_id == 'q':
                break
        return attachment_id

    def request_all_reports(self,client, query_id):
        request_url = self.query_url + query_id
        r1 = client.get(request_url)
        return r1.content

    def request_report_info(self, client, query_id, report_id='a'):
        while True:
            report_id = self.get_report_id(report_id)
            if report_id == 'q':
                return False
            request_url = self.query_url +  query_id + "/" + report_id
            r1 = client.get(request_url)
            if r1.status_code == 403:
                print("Invalid report id")
                report_id = 'a'
                continue
            elif r1.status_code == 200:
                break
        return r1.content

    def pick_download_folder(self, download_folder, report_id):
        desired_path = download_folder + "\\report" + str(report_id) + "\\"
        print(desired_path)
        if os.path.exists(desired_path):
            pass
        else:
            os.mkdir(desired_path)
        return desired_path

    def download_report(self, download_folder, client, query_id, report_id='a'):
        while True:
            report_id = self.get_report_id(report_id)
            if report_id == 'q':
                return False

            request_url = self.query_url +  query_id + "/" + report_id
            r1 = client.get(request_url)
            if r1.status_code == 403:
                print("Invalid report id")
                report_id = 'a'
                continue
            elif r1.status_code == 200:
                download_folder = self.pick_download_folder(download_folder, report_id)
                d = r1.headers['content-disposition']
                filenames = re.findall("filename=(.+)", d)
                filename = filenames[0].replace("\"","")
                local_filename = download_folder + filename
                with open(local_filename, 'wb') as f:
                    print("Download started for file %s..." % filename)
                    for chunk in r1.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                print("...Download finished")
                return True
        return False

    def download_attachment(self, download_folder, client, query_id, report_id='a', attachment_id='a'):
        while True:
            report_id = self.get_report_id(report_id)
            if report_id == 'q':
                return False

            attachment_id = self.get_attachment_id(attachment_id)
            if attachment_id == 'q':
                return False

            request_url = self.query_url +  query_id + "/" + report_id + "/" + attachment_id
            r1 = client.get(request_url)
            if r1.status_code == 403:
                print(r1.content)
                report_id = 'a'
                attachment_id = 'a'
                continue
            elif r1.status_code == 200:
                download_folder = self.pick_download_folder(download_folder, report_id)
                d = r1.headers['content-disposition']
                filenames = re.findall("filename=(.+)", d)
                filename = filenames[0].replace("\"","")
                local_filename = download_folder + filename
                with open(local_filename, 'wb') as f:
                    print("Download started for file %s..." % filename)
                    for chunk in r1.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                print("...Download finished")
                return True
            else:
                print("Unspecified error. Try again")
                continue
        return False







