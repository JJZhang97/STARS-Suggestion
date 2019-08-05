#Load mods time schedule and store it.
import requests
from bs4 import BeautifulSoup
#possible to have more than 1 timeslot for a single class, eg Comm fund 2
#returns courses in this format {"AC1101":[["1-tue-0830-1030","1-wed-1530-1730"],["2-wed-0830-1030","2-thu-1530-1730"]]}
def load_courses(list_courses):
    courses_dict = {}
    for course in list_courses:
        payload = {}
        payload['r_search_type'] = 'F'
        payload['boption'] = 'Search'
        payload['acadsem'] = "2019" + ';' + "1"
        payload['r_subj_code'] = course
        payload['staff_access'] = 'false'
        
        source = requests.post("https://wish.wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display1",data=payload).text
        soup = BeautifulSoup(source, "lxml")
        # print(soup.prettify())
        even = soup.find_all("tr", bgcolor="#CAE2EA")
        odd = soup.find_all("tr", bgcolor="#EBFAFF")
        t = even + odd
        
        t_list = []
        for tag in t:
            line_number = 0
            new = True
            timeslot = ""
            for line in tag:
                line = str(line)
                if line_number == 1:
                    if line[7] == "<":
                        new = False
                    else:
                        timeslot += line[7:12] + "-"
                elif line_number == 7:
                    timeslot += line[7:10].lower() + "-"
                elif line_number == 9:
                    timeslot += line[7:16]
                      
                line_number += 1
            if new:
                t_list.append([timeslot])
            else:
                t_list[-1].append(timeslot)
         
        t_list.sort()
        i = 1
        for timeslot in t_list:
            temp_list = []
            for tim in timeslot:
                t = tim.split("-")
                if len(t) == 4:
                    del t[0]
                t.insert(0,str(i))
                alt_timeslot = "-".join(t)
                temp_list.append(alt_timeslot)
            t_list[i-1] = temp_list
            i += 1
        
        courses_dict[course] = t_list
    return courses_dict
