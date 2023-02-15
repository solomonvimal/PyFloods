# PyFloods
Python module for floods

I made this repository a long time ago, to save time for folks who are getting started with HEC-RAS Controller and Python. 

It is not well-written or well-maintained, but does offer some useful starting points - if you use this repo, I encourage you to develop it further and contribute to it.

# Reference
The book titled 'Breaking the HEC-RAS Code' by Chris Goodell (https://tinyurl.com/Chris-HEC-RAS-book) is what I used to learn about the functions of the HEC-RAS Controller. You can do without the book if you are able to follow the Python code in this repository (HEC_RAS_controller.py) and the key (HEC-RAS function IDs) in this google sheet (https://tinyurl.com/ras-controller-functions). 

Chris Goodell maintains a forum for users of his book. If you are stuck with anything related to the Controller or HEC-RAS in general, you may post your questions there. I sometimes check the questions there that are related to Python.


# Mouse Automation

Another small tip that I think might help you along the way is that everything about the RAS-Controller works somewhat like mouse clicks on the HEC-RAS GUI itself, so you might want to simply automate the mouse movements with some Python module like 'win32api' if you have no way of doing it with native HEC-RAS controller methods. Here is an example code:


    import win32api, win32con 
    def click(x,y): 
        win32api.SetCursorPos((x,y)) 
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0) 
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0) 
    click(10,10)
