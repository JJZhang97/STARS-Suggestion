import STARS_mod_request
import re
import itertools
import csv
import os
import ast
class STARS():
    def __init__(self):
        self.list_courses = []
        self.schedule = [[0]*30,
                         [0]*30,
                         [0]*30,
                         [0]*30,
                         [0]*30]
        #class timing of each module
        self.l_courses = {}
        self.plan1 = []
        self.plan2 = []
        self.plan3 = []
    
    def get_courses(self):
        gate = False
        print("Please input name of module you want to take in this format: AC1101, BC1101")
        courses = input("Modules:")
        print()
        list_courses = courses.split(',')
        for course in list_courses:
            course = course.strip()
            m = re.match("^[A-Z][A-Z]\d{4}",course)
            if m == None:
                gate = True
            self.list_courses.append(course)
        if gate:
            self.list_courses = []
            self.get_courses()
            
    def fetch_strtime(self,course,index):
        #Returns the list(str_time), given the course code and the class index. Returns False if no timing is found
        timings = self.l_courses[course]
        gate = True
        i = -1
        while gate:
            i += 1
            for timeslot in timings[i]:
                if timeslot[0] == index:
                    return timings[i]
            if i >= len(timings):
                return False
    
    def convert_strtime(self,str_time,schedule,b):
        #Input:
        #str_time takes this format: "1-tue-0830-1230"   
        #schedule in which you want to store info
        #b: True to allow you to store the information, False only checks for clashes
        #Output:
        #Returns True if timeslot "clashes" with original "1", otherwise returns False
        #returns the index of the str_time
        day_dict = {"mon":0, "tue":1, "wed":2, "thu":3, "fri":4}

        index, d, t1, t2 = str_time.split("-")
        #Converts time into index of self.schedule
        def convert_time(t): 
            if t[2:] == "30":
                t = t[:2] + "50"
            c_t = int(t) - 800
            return int(c_t/50) - 1
        i1 = convert_time(t1)
        i2 = convert_time(t2)

        a = False
        while i1 < i2:
            if schedule[day_dict[d]][i1] == 1:
                a = True
            else:
                if b:
                    schedule[day_dict[d]][i1] = 1
            i1 += 1
        return a, index
    
    def del_class_index(self,course,index):
        #index is a string
        timings = self.l_courses[course]
        gate = True
        b = False
        i = -1
        while gate:
            i += 1
            try:
                for timeslot in timings[i]:
                    if timeslot[0] == index:
                        gate = False
                    elif timeslot[0] > index:
                        b = True
                if gate == False:
                    del timings[i]
                if b:
                    #If the str to be found is already deleted, breaks loop
                    gate = False    

            except Exception:
                #Handles exception where last index is deleted resulting in list index out of range
                gate = False
    
    #Stores plan and updates self.schedule
    def store_plan(self,course,index):
        timeslot_list = self.fetch_strtime(course,index)
        for timeslot in timeslot_list:
            self.convert_strtime(timeslot, self.schedule, True)
    
    def register_failed_courses(self,list_courses,plan):
        gate = True
        while gate:
            try:
                #remove indexes of class which you failed
                print("Please input 1: courses you have registered; 0: courses you have failed to register")
                print("In this format: 1,0,1")
                print(list_courses)
                response = input("-->")
                r = response.split(",")
                if len(r) != len(list_courses):
                    raise Exception
                failed_courses = []                   
                index = 0
                for res in r:
                    print(res)
                    if res == "0":
                        self.del_class_index(list_courses[index], plan[index])
                        failed_courses.append(list_courses[index])                        
                    elif res == "1":
                        self.store_plan(list_courses[index], plan[index])
                    else:
                        raise Exception
                    index += 1
            except Exception:
                print("Please enter in the valid format.")
                print()
            else:
                gate = False
        self.suggest(failed_courses)
    
    #suggest new plan after success and fail
    def suggest(self,failed_courses):
        c_list = []
        for course in failed_courses:
            c_list.append(self.l_courses[course])
        combi = itertools.product(*c_list)
        gate = True
        while gate:
            try:
                copy_schedule = []
                #Make a copy of schedule which changes
                for line in self.schedule:
                    copy_schedule.append(line[:])
                c = next(combi)
                class_index = []
                for inner1 in c:
                    for inner2 in inner1:
                        b,_ = self.convert_strtime(inner2,copy_schedule,False)
                        #If clashes
                        if b:
                            raise Exception
                    for inner_2 in inner1:
                        _,index = self.convert_strtime(inner_2,copy_schedule,True)
                    class_index.append(index)
                
                inner_gate = True
                while inner_gate:
                    print(f"""
{failed_courses}
Plan suggested: {class_index}
                    
Select an option:
1. Accepted plan and failed courses
2. Suggest New Plan
3. Exit""")
                    
                    option = input("Option selected:")
                    if option == "1":
                        self.register_failed_courses(failed_courses,class_index)
                    elif option == "2":
                        raise Exception
                    elif option == "3":
                        inner_gate = False
                    else:
                        print("Please input a valid option!")
                        print()
            
            except StopIteration:
                print("All combinations are used up!")
                print()
                gate=False
            
            except Exception:
                pass
            else:
                gate = False
    
    #Resets STARS_Planner
    def reset(self):
        self.list_courses = []
        self.schedule = [[0]*30,
                         [0]*30,
                         [0]*30,
                         [0]*30,
                         [0]*30]
        self.l_courses = []
        self.plan1 = []
        self.plan2 = []
        self.plan3 = []        
        
if __name__ == "__main__":
    gate = True
    star = STARS()
    while gate:
        print("Welcome to STARS_TryPlanner!")
        #if there's a csv file, read from csv file
        try:
            with open("save.csv","r") as csv_file:
                csv_reader = csv.reader(csv_file)
                row = 1
                for line in csv_reader:
                    if row == 1:
                        star.list_courses = line[1:]
                    elif row == 2:
                        if len(line) > 1:
                            for num in line[1:]:
                                star.plan1.append(int(num))
                    elif row == 3:
                        if len(line) > 1:
                            for num in line[1:]:
                                star.plan2.append(int(num))
                    elif row == 4:
                        if len(line) > 1:
                            for num in line[1:]:
                                star.plan3.append(int(num))
                    else:
                        l = []
                        for ll in line[1:]:
                            l.append(ast.literal_eval(ll))
                        star.l_courses[line[0]] = l
                    row += 1
        
        except FileNotFoundError:
            star.get_courses()
            star.l_courses = STARS_mod_request.load_courses(star.list_courses)
        
        gate_2 = True
        while gate_2:
            print("""Please select an action:
1. Generate Combinations
2. Store Plan
3. Overview of stored plan
4. Reset All
5. All class index available
6. Save
7. Exit STARS_TryPlanner""")
            
            choice = input("Option selected:")
            if choice == "1":
                plan_list = [star.plan1,star.plan2,star.plan3]
                n = 1
                failed_courses = star.list_courses[:]
                for plan in plan_list:
                    if plan != []:
                        gate1 = True
                        while gate1:
                            #Will it forget "failed_courses" when it loops through?
                            if len(failed_courses) == 0:
                                gate1 = False
                                break
                            temp_list_i = failed_courses[:]
                            print(f"Loaded plan {n}")
                            print("Please input 1: courses you have registered; 0: courses you have failed to register")
                            print("In this format: 1,0,1")
                            print(temp_list_i)
                            temp_list = []
                            response = input("-->")
                            res = response.split(",")
                            try:
                                if len(res) != len(temp_list_i):
                                    raise Exception
                                #check if value is not equals to 0 or 1
                                for r in res:
                                    if r == "1":
                                        pass
                                    elif r == "0":
                                        pass
                                    else:
                                        raise Exception
                                i = 0
                                for r in res:
                                    if r == "1":
                                        print(temp_list_i[i], plan[i])
                                        star.store_plan(temp_list_i[i],plan[i])
                                    else:
                                        temp_list.append(temp_list_i[i])
                                    i += 1
                                failed_courses = temp_list[:]
                                gate1 = False
                            except Exception:
                                print("Please enter a valid input!")
                                print()
                            
                    n += 1
                #Del class index of all plan
                for plan in plan_list:
                    i = 0
                    for p in plan:
                        star.del_class_index(star.list_courses[i],p)
                        i += 1
                star.suggest(failed_courses)
                     
            elif choice == "2":
                gate2 = True
                while gate2:
                    if star.plan1 == []:
                        n = 1
                    elif star.plan2 == []:
                        n = 2
                    elif star.plan3 == []:
                        n = 3
                    else:
                        print("Plan full!")
                        gate2 = False
                        break
                    print(f"Plan stored under plan {n}")
                    print(f"Please key in the index of the classes class in this format: 1,6")
                    print(star.list_courses)
                    c_index = input("Class index:")
                    c_i = c_index.split(",")
                    try:
                        for i in c_i:
                            int(i)
                        if len(c_i) == len(star.list_courses):
                            gate2 = False
                            if n == 1:
                                star.plan1 = c_i
                            elif n == 2:
                                star.plan2 = c_i
                            else:
                                star.plan3 = c_i
                        else:
                            raise Exception
                    except Exception:
                        print("Please input in the correct format!")
                        print()
                
            elif choice == "3":
                print("Overview of Stored Plan:")
                print(star.list_courses)
                print(f"""Plan1: {star.plan1}
Plan2: {star.plan2}
Plan3: {star.plan3}""")
                print()
            elif choice == "4":
                try:
                    os.remove("save.csv")
                finally:
                    gate_2 = False
                    print("STARS Planner Prototype is reseted!")
                    print()
                star.reset()
            elif choice == "5":
                for course, timeslots in star.l_courses.items():
                    print(f"{course}: {timeslots}")
                print()
            elif choice == "6":
                #save as file
                with open("save.csv", "w") as csv_file:
                    csv_writer = csv.writer(csv_file, delimiter = ",")
                    csv_writer.writerow(["List courses"]+ star.list_courses)
                    csv_writer.writerow(["Plan 1"]+star.plan1)
                    csv_writer.writerow(["Plan 2"]+star.plan2)
                    csv_writer.writerow(["Plan 3"]+star.plan3)
                    for course, timeslots in star.l_courses.items():
                        csv_writer.writerow([course]+timeslots)
            elif choice == "7":
                gate = False
                gate_2 = False
                print("Thank you for using STARS Planner Prototype")
            else:
                print("Please input a valid option!")
                print()
