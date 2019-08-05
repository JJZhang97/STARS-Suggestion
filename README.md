Introduction
This is script is created for students studying in Singapore's Nanyang Technological University.
There's this thing called the STARWARS where students have to fight to register for their courses. Every second matters.
There are times when you failed to register for some of your courses during STARWARS, even after loading all 3 saved plans.
What do you do? Panic and randomly try out every single option of the course and pray that they succeed without clashing with your already registered courses?
Hence this script is written for you to overcome that situation.

How to use the script
1. run the script
2. you will be asked to enter the courses you want to register
3. you will then enter the main menu, which you will be greeted with 7 options:
        1. Generate Combinations: Generate combinations of possible class indexes
        2. Store Plan: Store your 3 plans here. enter class index of the courses you want to register.
        3. Overview of stored plan: Shows the 3 plans you have stored.
        4. Reset All: Deletes all saved plan, and resets to brand new state.
        5. All class index available: Shows all class index and their respective timeslots.
        6. Save: Saves your progress so that you can come back to it next time.
        7. Exit: Exits planner

Suggested way of using
Once you execute your script and navigate to step 3(main menu), you should store your 3 plans(Option 2).
It will ask for your class indexes for the courses you are registering for. After keying in your indexes, you will be returned to the main menu. If you want to store the other 2 plans, just choose option 2 again 2 more times. After which, you may want to choose option 3 to ensure that you have keyed in the correct indexes. If you want to make changes to the class index, you will have to choose option 4 in the main menu and start all over again.
Once you are done hit the save button(option 6) then exit(option 7) and come back to it on the actual STARWARS date.
(Note: If you have saved, please do not remove "save.csv" file in the directory as that is your saved file.
If you have removed it, it will prompt you to start everything again, unless of course you intend to do so...)

Actual STARWARS day:
(The only reason why you would want to use this is when you still have courses not registered even after trying all your 3 plans)
choose option 1. It will ask you which courses you have successfully registered in plan1. key in 1 for successfully registered courses and 0 for a failed course. Likewise, it will ask you again if you have plan 2 and plan 3 registered. Just do it for the other 2 plan. (Note, it will only ask you for the courses you have failed to register in plan 2 and 3)
It will show you the suggested combinations of class indices.
After which you will be shown 3 options:
        1. Accepted plan and failed courses: Accepts plan, and prompts you for courses you have failed to register
        2. Suggest New Plan: Suggests new plan if you don't like the current one
        3. Exit: Exit to main menu
