# Title: Get Massey GPA
# Description: A simple script which automatically calculates your Massey GPA
# Note: Does not currently take into account the credits, as all my papers are 15 points
# Author: Daniel Roberts
# Date: 8/7/14

from requests import session
import re

username = input("Enter your username: ")
password = input("Enter your password: ")

grademap = {'A+':9,'A':8,'A-':7,'B+':6,'B':5,'B-':4,'C+':3,'C':2,'D':0,'E':0,'DNC':0}

# determined using Chromes developer tools, network tab with logging
payload = {
    'uname':username,
    'pass':password,
    'module':'User',
    'op':'login',
    'url':'/index.php',
    'x':'26',
    'y':'8'
}

with session() as c:
    c.post('https://secure.mymassey.com//user.php', data=payload)   # login and store auth. cookies
    request = c.get('https://secure.mymassey.com/modules.php?op=modload&name=NS-Study&file=index&req=exam_results') # navigate to grades page
    grades = re.findall('<td class="examResult_Grade"><span.*?>(?:<BR />)?(.*)</span></td>', request.text)
    gradepoints =  [grademap.get(grade, None) for grade in grades if grade in grademap.keys()]  # make list of the valid grades gradepoints
    gradecount = len(gradepoints)
    gpa = sum(gradepoints) / gradecount
    print("Valid Grades Found: {}, GPA: {:1.3f}".format(gradecount,gpa))
