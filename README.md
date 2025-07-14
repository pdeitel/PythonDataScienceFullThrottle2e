©️ Copyright 2025 by Deitel & Associates, Inc. and Pearson Education, Inc. All Rights Reserved. 

# PythonDataScienceFullThrottle2e
This is the new repository for my  **Python Data Science Full Throttle: Introductory Artificial Intelligence (AI), Big Data and Cloud Case Studies** live training on [O'Reilly Online Learning](https://learning.oreilly.com/live-events/python-data-science-full-throttle-with-paul-deitel-introductory-artificial-intelligence-ai-big-data-and-cloud-case-studies/0636920289197/).

We're working on the second editions of our Python books and videos now. Early access to some of those new materials will be available to you through this course and eventually my Python Fundamentals LiveLessons Sneak Peek. We'll be updating the videos in place in the current product at: https://learning.oreilly.com/api/v1/continue/9780135917411/ 

# Getting the Code
Download or clone this repository's contents onto your system. **These files are for your personal use and may not be redistributed or reposted.**

# Running the Code
If you want to run the code, keep in mind that various examples require API keys that you'll need to aquire and add to the files. The notebooks indicate which keys you need and where to get them.

## Zero-Install MyBinder Environment
I have set up the GitHub repository with a `Dockerfile` that enables you to load a zero-install environment in MyBinder.org:

> `https://mybinder.org/v2/gh/pdeitel/PythonDataScienceFullThrottle2e/main?urlpath=lab`

## Docker
Docker users can build a local container from the `Dockerfile` in the GitHub repository. These instructions assume you have Docker Desktop installed with support for the `docker compose` command and that you've downloaded or cloned this repository to your system. Comment out the `Dockerfile` line:  

> `COPY . /home/jovyan/`
> 
by inserting a `#` before the line as in  

> `# COPY . /home/jovyan/`

(or simply delete that line.) From a **Terminal** window (Mac) or a **Command Prompt** or **Powershell** window (Windows) change to the root folder of the repository, then execute: 

> `docker compose up`

Once this finishes building the container, which can take several minutes depending on your connection speed, you'll see a line of text similar to the following:

> `http://127.0.0.1:8888/lab?token=fb59401a105a0c5a45c52eff8e1a8469f508cad1f3a8be06`

Copy this line and paste it into your preferred web browser to launch JupyterLab.

# Questions
If you have any questions, open an issue in the Issues tab or email us: deitel at deitel dot com.

# Our Books on Which These Examples Are Based \[NEW EDITIONS UNDER DEVELOPMENT\]
The content of this course is based on our book <a href=https://amzn.to/2Kd8dQk target="_blank">Python for Programmers</a>, which is a subset of our book <a href=https://amzn.to/2KfCptN target="_blank">Intro to Python for Computer Science and Data Science: Learning to Program with AI, Big Data and the Cloud.</a> 
   
![Cover image for Python for Programmers](https://deitel.com/wp-content/uploads/2020/01/python-for-programmers.jpg)

The authors and publisher of this material have used their best efforts in preparing this material. These efforts include the development, research, and testing of the theories and programs to determine their effectiveness. The authors and publisher make no warranty of any kind, expressed or implied, with regard to these programs or to the documentation contained in this material. The authors and publisher shall not be liable in any event for incidental or consequential damages in connection with, or arising out of, the furnishing, performance, or use of these programs.
