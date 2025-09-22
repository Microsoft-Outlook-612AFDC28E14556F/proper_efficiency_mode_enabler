# proper_efficiency_mode_enabler
A python script which can enable efficiency mode for running processes in windows.

# Note
This program does not use methods such as the following;  
`start /belownormal "ProcessName" "path\to\executable.exe"`  
`Start-Process -FilePath "path\to\executable.exe" -WindowStyle Normal -Priority BelowNormal`  
`wmic process where name="processname.exe" CALL setpriority "below normal"`  
As far as I can tell such methods set or attempt to set the process priority which as far as I can see, is not the same thing as efficiency mode.
If you look at the code, and (at least somewhat) know how to read it, you'll see clearly that the mechanism by which effieicncy mode is enabled for the processes is much more complex than a single command or line of code.

# DISCLAIMERS
Yes, this script was partly written by an AI. I know this is desplicable.  
No, I don't fully comprehend what it does ( I don't care to, because I dislike windows. )  
Most of the heavy lifting actually wasn't done by myself or AI, it was done by Matt_the_ok on a Microsoft owned forum. Below is the link to his code.  
https://learn.microsoft.com/en-us/answers/questions/2155580/how-do-i-force-a-python-script-to-run-in-efficienc  
I did not request permission from Matt_the_ok before using his code. Nor did I make any attempt at communication.

# Features
- Requires minimal input. For example, if you want to make your Steam processes run in efficiency mode you can just type "steam" when the program requests input.
- Automatically finds processes which match the input criteria and sets them to efficiency mode by getting a list of your running processes and using regex to determine if they're relevant.

# Preface
I shouldn't have to state this, but I will anyways. Especially since this little script is random code your getting from the internet and it was programmed by AI and people who don't know what they're doing you should check over the code and make sure it doesn't do anything obviously bad like, I don't know - delete System32, have bad (or any) interactions with the internet.

# Installation & Usage (example)
1. Download the file `custom_efficiency_mode.py` in this repo.
2. Ensure you have the pip packages installed. I had to install `wmi` and `psutil`.
3. Launch a terminal (perferrably as admin)
4. Launch task manager and think about what you want to be in efficiency mode.
5. Execute the script, and type a substring of the name(s) of the process(es) you want to put into efficiency mode.
6. Observe in task manager that the process(es) are in effeciency mode marked by a green leaves icon and the text 'Efficiency...' in the status column.

# Contributing
I'm not much of a programmer. I recommend forking rather than making pull requests or better yet, just take the code, and do what you want with it. Someone more knowledgable could adapt this into other languages, making a whole proper app out of it, add it to their existing program, whatever.

Ok, first draft README.md done.
