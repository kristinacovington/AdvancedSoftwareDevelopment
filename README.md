# cs3240-s17-team01
CS 3240 Project 2017
Lokahi Fintech Crowdfunding

## Heroku server is up!

You can still make changes and run it in local server as normal

To make changes in heroku:

    $ heroku git:remote -a glacial-ridge-29106

    $ git add .
  
    $ git commit -am "insert commit message here"
  
    $ git push heroku master
  
  Then you can access it at: https://glacial-ridge-29106.herokuapp.com/home/
  
  All other commands are mostly the same i.e:
  
    $ heroku run python manage.py migrate
    
    $ heroku run python manage.py createsuperuser
    
    etc...

I set up an super user already:

    username: administrator
    password: administratorpassword
  
Note you do have to push to this github repo and the heroku repo separately (hence why we have 2 .git folders)
The Heroku repo is located under the /MyDjangoApp2/ folder 


## Core Features:

A. Accounts and Groups
A Company User can sign up for an account via a webpage. This allows them to interact with the system in the
Computer User role. Company Users create reports
2. An Investor User can sign up for an account via a webpage. This allows them to interact with the system in the
Investor User role. Investor Users can search for reports and only add files to existing reports. Investor users do
not create reports.
3. One Site Manager (SM) account initially exists in the application (do not use the Django Admin user for your
SM).
4. Users can be organized into groups, each with a unique name. Groups exist for the primary purpose of sharing
access to report info that is otherwise private, i.e. not accessible by other users.
5. A user does not have to be in a group or can be in one or more groups.
6. Any user can create a new group.
7. A member of a group can add another user to that group (without the permission of the SM).
8. A member of a group can remove his or herself from a group (other members cannot delete another member
from a group)

B. Site Manager (SM) user role:
1. SM users can give other users SM status.
2. SMs can create groups, assign any user to any group
3. SMs can delete any user from any group.
4. SMs can suspend and restore a user's access to his or her account.
5. SMs can access, edit, and delete any user's reports, even if they are private 

C. Reports:
1. Reports are associated with the Company User that created them.
2. A Report must include the following components, supplied by the Computer User who creates it. (see report
sample at end of document)
    1. Timestamp when report created (automated date/time the report is created).
    2. Company Name. (one line of text)
    3. Company Phone. (one line of text)
    4. Company Location (one line of text)
    5. Company Country (one line of text or a drop down list)
    6. Sector (one line or a drop down list)
    7. Industry (one line of text or a drop down list)
    8. Current Project(s) (multiple lines of text)
    9. One or more files (optional, a report does not have to have a file attached however, the option must be
    available). Any file format can be uploaded. The user should be able to indicate if the uploaded file is
    encrypted. (The system should not encrypt the file or store the information to allow it to be decrypted. But
    it must know whether a given file is encrypted or not.)
    10. Whether the report is public or private (public reports can be seen by any user of the system, private can
    be seen by only those given access).
3. Additional fields are allowable, perhaps to support additional features. For example:
    1. Location (such as, geographical location) (perhaps for some advanced search?)
    2. User-supplied keywords (perhaps for search or organizing display of reports?)
    3. Etc. (be creative, what might be needed in a system like Lokahi Fintech Crowdfunding?)
    4. Private reports will not be searchable or visible in any way to users who do not have access to that report (except
    a SM user).
    5. Reports can only be deleted by the SM user.
    
D. Display and Search through the Web Interface:
1. A user can list all reports (accessible to that user) in a user-friendly way. All fields of the report will be displayed,
including a list of files for that report.
2. A user can list fewer reports by using search.
3. Search results are controlled by matching search criteria to one or more fields.
4. All users should be able to search by Date of Report, Company Name, CEO Name, Sector, Industry, Company
Location, Company Country, Current Projects
5. Combining searches with ANDs, ORs, or other non-trivial search control is highly desirable (such as, search by
Company Name, date range of when the report(s) were created and in a selected Location or search by Sector
and Company Location).
6. Access rules for private reports will be enforced, except that SM users can see all reports.
7. Basic search functionality is required, but more advanced or sophisticated search features will be recognized and
rewarded.
8. When displaying a report, unencrypted files should be available for viewing or downloading. Encrypted files can
only be downloaded by the File Download Application (see next item).

F. File Download Application (FDA)
1. The FDA is a stand-alone application that will be run on networked computer (your local computer) and
communicate with the Django web application.
2. A user of this program will be able to:
1. Authenticate using the credentials of a valid registered web-app user (such as, name and password).
2. See a list of reports. (This does not have to be as sophisticated as for the web-interface.)
3. Choose a report, display it, and allow the user to download the file or files for that report.
4. Decrypt files if they are encrypted.
5. Encrypt files (so they may be uploaded with a report).

G. Private Messages
1. Display of and interaction with private messages is allowed to be separated in the UI from displaying and
interacting with reports.
2. When a user logs in, she or he should be able to easily see if there are private messages.
3. When creating a private message for another, the message's creator can optionally make it encrypted.
4. Private messages that are encrypted are not automatically decrypted when the recipient sees them. The recipient
must take some action to decrypt it.
5. The system should store and manage information needed for a user to create a private message for a 2nd user
that only that 2nd user can decrypt. This information should be stored as securely as possible.
6. A recipient can delete any of his or her private messages.
7. Private messages are seen only by the recipient (not a SM user)

H. Security Requirements
(The following are more constraints or general features than specific requirements. Teams have liberty in how they define
the security requirements and design features of their system.)
1. A Company User and/or Investor User can choose files attached to reports to be encrypted. Other text entered
into reports is plaintext.
2. Encrypted files can downloaded and decrypted by the stand-alone program (FDA). This program will somehow
get the key needed to decrypt the file.
3. We would like you to make use of: public key encryption for encryption and signing. Hash functions should be
used somehow to allow a reader of a report and/or file to verify its integrity.
4. In planning the system, some requirements should be defined that address security issues (authorization,
authentication, integrity, confidentiality, accessibility, etc.).



