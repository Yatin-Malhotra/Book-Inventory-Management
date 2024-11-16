Basic Info:

    A basic inventory management system for books. 

    The 3 operations that the system allows are:
    - Adding Books
    - Filtering Books (based on author, title, and isbn)
    - Exporting Data (either CSV or JSON)

Instructions on how to use the system:

    run the following command to install the requirements:
        pip install -r requirements.txt

    After you have the requirements installed, do the following to run the application:
        python3 app.py

    Now you have a link in the terminal, open that link (http://127.0.0.1:5000).

Design Decisions:
    Code:
        I am only checking for the latest ISBN's, i.e., ISBN-13. In the check, I
        have made sure that the ISBN number starts from 978 and the rest are
        digits. So, it is important to make sure that when the code is run, only
        numbers are used, no hyphens.

    UI:
        I have decided to make the design rather plain and simple as it meets the 
        requirements and does not overwhelm a new user. I have also ensured that any
        success or failures are showcased right below the button for that section,
        where success is highlighted in green and error is highlighted in red.

    NOTE: Features for accessibility (such as different languages, font size changes, etc.) have not been added and there is no color blind mode.

Demo: https://youtu.be/2FL3ALw7niw