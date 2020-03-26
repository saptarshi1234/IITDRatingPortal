# IITDRatingPortal

This is a prof and course review portal specifically for IITD.
Students can sign up with their kerberos emails and post reviews on the professors and courses of IIT Delhi.

## Details about the system
Only students with valid IITD issued emails can sign up for this portal.
Email-verification is done by sending an email containing the registration link to their kerberos accounts.
After logging in, the users have the option to link their accounts with their social media -- Google, Github and Twitter.
Henceforth they can log in directly with their social accounts.

Registered users can find a list of the courses taught and the professors teaching them and can post their reviews(with their
usernames visible or anonymously)..
and can also upvote other reviews.  There is however no provision for downvoting.

There is a provision for an admin who monitors the site.
The Admin can see the identity authors of all the reviews( even anonymous ones) and can delete the reviews that are offensive.
A warning is sent to the author when a review is deleted.
The Admin also has the power to ban users for repetitive offensive reviews.. for 15 days , 30 days or indefinitely.
The users are automatically ' unbanned' after their spcified poriod
All banned users are listed in the Admin's profile and they can be unbanned before their ban duration is over if the Admin deems 
it necessary.

All users can report a review to the admin.
Reported reviews appear on the admin's profile.

## Implementation Details
### models
The important models used are :
1. Professor:
    * Name
    * Department
    * Age
2. Course:
    * Name
    * Department
    * List of professors teaching
3. User:
    (Default django user)
4. UserProfile:
    * User(one to one field)
    * Respect Points
    * Ban info
5. Course Review:
    * Author
    * List of users that liked (Many to many field) 
    * Course
    * Reported info
6. Course Review:
    * Author
    * List of users that liked (Many to many field) 
    * Professor
    * Reported info
    

## Usage Instruction 
Use Python version 3.6 or higher
install the following packages preferably in a virtual environment
1. django (3.0.4)
2. django-allauth
3. six

The results of pip freeze are given in the file /IITDRatingPortal/pip_freeze_results.txt

