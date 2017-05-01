import requests
import os
from query_lib import query_bot
from output_lib import output_bot
import encrypt_lib

def getDownloadFolder():
    dir = os.getcwd()
    download_path = dir + "\download\\"
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    return download_path

def authorizeUser(client):
    login_url = "http://127.0.0.1:8000/login_fda/"
    user = input("Username: ")
    password = input("Password: ")
    if password == "":
        return False, b''
    try:
        r0 = client.get(login_url)
    except requests.exceptions.RequestException:
        print("Could not reach the file server, terminating program.")
        exit(0)
    try:
        csrftoken = client.cookies['csrftoken']
        login_data = {'username': user, 'password': password, 'csrfmiddlewaretoken': csrftoken}
    except KeyError:
        print("Cookie could not be retrieved. Post request cannot be made. Terminating program.")
        exit(0)

    r1  = client.post(login_url,data=login_data)

    if r1.status_code == 500:
        print("Error code 500, possible that server could not be reached. Terminating program.")
        exit(0)
    elif r1.status_code == 403:
        print("HTTP Status Code 403: Forbidden")
        return False, b''
    elif r1.status_code == 200:
        key = encrypt_lib.decrypt_string(r1.content, password)
        return True, key
    else:
        print(r1.status_code)
        return False, b''

def downloadFile(url,download_folder):
    local_filename = download_folder + "report_" + url.split('/')[-1] +  ".pdf"
    r = requests.get(url)
    with open(local_filename, 'wb') as f:
        print("Download started...")
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    print("...Download finished")
    return

def handleQuery(query_id, client, download_folder):
    if query_id not in list(query_dict.keys()):
        print("\nQuery ID '" + query_id + "' is not avaiable. Try again\n")
        return False
    print("\nQuery ID %s accepted..." % query_id)
    qb = query_bot()
    ob = output_bot()

    if query_id == '1':
        reports = qb.request_all_reports(client, query_id)
        ob.print_content(reports)
    elif query_id == '2':
        report_bundle = qb.request_report_info(client, query_id)
        if report_bundle == False:
            print("Request Cancelled")
        else:
            ob.print_content(report_bundle)
    elif query_id == '3':
        result = qb.download_report(download_folder, client, query_id)
        if result:
            pass
        else:
            print("Download cancelled")
    elif query_id == '4':
        qb.download_attachment(download_folder, client, query_id)
    elif query_id == '5':
        pass
    elif query_id == '6':
        pass
    elif query_id == '7':
        pass
    elif query_id == '8':
        pass
    elif query_id == 'q':
        print("...Exiting Program")
        exit(0)
    print("...Query ID %s handled\n" % query_id)

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
def getQuery():
    print("Chose one of the following command IDs:")
    for query_id, query_name in query_dict.items():
        print(query_id + ": " + query_name)
    query_id = input("Enter ID here: ")
    return query_id

if __name__ == "__main__":
    download_folder = getDownloadFolder()

    client = requests.session()
    print("Enter credentials, type q to quit")
    authorized = False
    while True:
        authorized, user_private_key = authorizeUser(client)
        if authorized:
            break
        else:
            print("Authorization failed, please try a again or type q to quit")
    print("Login succeeded\n")
    #
    # print("sending query of 1")
    # query_url = "http://127.0.0.1:8000/report/query/"
    # handleQuery(query_url, "1")

    while(True):
        query_id = getQuery()
        handleQuery(query_id, client, download_folder)


   # downloadFile("http://127.0.0.1:8000/download/1", download_folder)

