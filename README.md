# AutoGrading

![](./logo/logo2.png)
AutoGrading project for RCOS
[project link on rcos.io](https://rcos.io/projects/huimingcheng/autograding/profile)

## Technology Stack

- Back end: python3, c++, MySql
- Front end: html, css, markdown

- Useful external library(ies): OpenCV


## Team members

Joined in September, 2017:
Huiming Cheng, Rujie Geng, Pengqin Wu, Yirong Cai


Joined in Feburary, 2018:
Alex Zhu, Zixiang Zhang, Hongrui Zhang, Haolun Zhang, Haotian Wu, Zhepeng Luo

## Current status

We finished the core functionalities of the project. Now we are working on making the code more robust, and being able to handle more general cases. We have been seeking improvments in these following directions:

- Handwritting recognition.
Some inputs are not neatly written and cause the grader to produce inaccurate results, or simply run into invalid states. To be more specific, we are working out an efficient way of splitting letters that are stuck together.

- More ways of accepting input.
Currently, in the demos we only get input from a scanner - provides the grader with a clean and bright image. The team is striving to get the grader working with inputs from cell phone cameras. With this done the application will be able to be deployed on a server and allow users to access the grader remotely, and without looking up and down for a scanner. 

- Documentation, code quality and design pattern.
Despite the main part of the grading code is done, we still need to seek ways to improve the code by making it OOP and use design patterns to allow further extensions on functionalities. Apart from this, members are encouraged to put down comments and documentation about their own sections, making the code manageable.

## Future Goals

- Scanner-Independent
- Variable ways of accepting input
- Deploying on web server
- Modular, clean and low coupling code
