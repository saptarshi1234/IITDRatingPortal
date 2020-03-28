# BRAIN WARM UP
Before thinking of the process to handle the zip feature we need to consider the following aspects on which the task depends:

1. #### Time taken to zip:
 The process of zipping a large nested directory structure of size over a gigabyte is quite resource intensive and might take time in the order of several minutes or more.
 
2. #### The number of users accessing the zip feature per day:
We can reasonably assume a low traffic on most days but a large number of users accessing the portal at the same time just before exams.

3. ####  The number of times contents are updated:
we can assume that new files are mostly added after completion of the exams and the not many uploads in a single day

Considering all these factors, following are some of the ways in which the intended feature can be implemented:
*  ##  Generating a zip file everytime a user wants to access it:
This would work only when the traffic in the site is low and as we saw , due to high number of users accessing at the same time just before exams the server might crash. So, it is not quite a good method in this case.
* ## Updating a zip file in the server after a predefined period:
The admin could choose a specified time, for instance 4 AM everyday, when the traffic is low. This would ensure that the server never crashes as we perform a limited number of operations (once per day, say) and served the saved file to a user when required. However it has a slight disadvantage that the zip file will not be in sync with the original files after an upload till the predetermined period finishes. So, the success of this lies in the actual value of the time interval.  
*  ## Updating a zip file in the server whenever a user uploads a new file:
This would remove the problems of the earlier method as it ensures that the zip file always remains up to date as it is overwritten whenever its contents are modified. Some modifications might be done for instance instead of updating the zip then and there the server could schedule them for later in the night when the traffic is low.

So, we have to choose among the last two methods depending on the actual values of number of file additions per day. The third method is the best when the files are not modified often which is the case with citadel as we have a limited number of files to upload per semester, per course.





# RESEARCH ASSIGNMENT 
## Working of a website
When we type the address(URL) of a website in our browser the following processes are carried out:
1. The browser looks up the IP address corresponding to the domain name via a DNS (Domain Name Server). An example would be the google DNS server at 8.8.8.8.
2. Then the browser sends an HTTP request containing all the queries and other information like form data to the server.
3. The server processes the request and sends back an HTTP response containing raw HTML.
4. The browser renders the HTML and continues asking for other files when required and loads the page.
5. The page is functional and the user can now access the page and perform actions on it that trigger javascript code to send requests as needed.


If the protocol is HTTPS instead of simple HTTP some other security steps have to be followed in between  to establish a secure channel between the user and the server.

## Sharing webpages on same network
If we have a folder containing raw HTML, CSS and javascript then we can share the folder as if it were a website on our local netwotk(eg-wi-fi), so that others connected to the same network can browse the pages on as they would any website.
It is easy to set up a server using the python command SimpleHttpServer
####  Usage: 
 ```
 python -m SimpleHTTPServer
```
To access the site from a connected device we need to go to the local IP address of the serving computer.
Eg: if the machine that serves has IP addr : 192.168.43.120, then we enter the address 192.168.43.120:8000/[file name] to view any file in the shared folder.


## Apache and NginX
A web server is a software that receives requests from users and serves the files to its clients through a variety of protocols such as HTTP, HTTPS, POP3, etc. Webservers are also responsible for recieving content from clients and storing them for future use, eg- uploading files.
These are popular web-servers in the community. Together, they account for about 50% of the traffic on  the internet.
The main difference between the two lies in their design architecture, the way they handle traffic and respond to different conditions.

Apache follows a process-driven approach, and creates a new thread every time to handle a connection request. The main advantage is that processes remain separated from each other as they run on separate threads.
However the above setup runs into problems when it encounters hundreds of concurrent connections and each of them require heavy processing power and compete for limited CPU and memory resulting in low server speed.


NginX, on the other hand, follows an event-driven approach and a uses non-blocking-event-driven connection algorithm, thus handling thousands of requests asynchronously within one processing thread. This allowes Nginx to work faster and better with limited resources. 



## Connections to machines on different networks
The above method will not work directly if we want to accesss the site from machines not on the same network as the server would not have any direct way to communucate with the user. To achieve it we need to host the site on a public webserver instead of on our localhost.
Some popular sites to host are AWS and google cloud.


## Types of databases and which to use
A database is, loosely speaking, a way to store structured data for future use in a way that facilitates quick lookup, retrieval and modification of data as and when required.
Broadly speaking, common databases usually fall into either SQL or NoSQL types. Each of them has their own advantages and disadvantages according to the requirements and type of data stored.
### SQL database:
SQL stands for Structured Query Language. SQL databases are relational databases, where data is stored in the form of tables with relations connecting the tables to each another. Each column of a table represents a field such as name and each row represents a complete object/record such as a student. A major aspect of relational databases is that the data type of each field must be specified from among one of the predefined data types, along with other constraints .
The major advantages of Relational databases are:
1. They ensure integrity due to strict adhering to the data types and constraints, thus are good for storing important data.
2.  Due to relations between the tables queries become quite fast and can be carried out with minimal browsing through the database. It also allows for complex queries to be executed accurately.
3. It is quite robust and standardised, and has a large community using it.

Disadvantages:
1. Its difficult to make changes to the underlying schema, the data types and structure of the database may change during the project itself which creates a problem in relational databases.
### NoSQL database:
The last disadvantage is the major reasons that NoSQL became widely popular
It stores data in form of key-value pairs, graph or as columns.
The advantages of NoSQL are:
1. It enables developers to start working on the database early without a complete knowledge of the detailed model and without defining the data types in advance. It is thus said to be flexible.
2. Sharing and partitioning a NoSQL database is quite easy where it requires additional effort in case of Relational databases.

Disadvantages:
1. Its difficult to process complex queries as a large section of the database has to be scanned due to lack of relations between the various nodes.


Thus the bottom line seems that NoSQL should be used when we are working with unstructured data and a lot of datatypes that might need to be modified in the future, and we are not quite concerned with consistency. 
Whereas SQL databases should be used when integrity is paramount, there is need to run complex queries and do not expect a lot of changes or rollbacks.

For the context given, that of storing details of professors, no such change in data type and structure is expected and we may need to process complex queries in future.
So an SQL type database would be most suitable for this case
### Models:
* #### Professor
 * name-String
 * age   - integer
 * department - foreign key

* #### Course
 * name - string
 * department - foreign key
 * professors - many to many field

* #### Intern
 * name - string
 * department - foreign key
 * current project - foreign key

* #### Department
 * name - string

* #### Project
 * professor - foreign key
 * description - string
 * start date - time field





## Javascript timer
javascript has a built-in timer and native method setTimeout() to schedule a task after a specified duration of time. The function accepts a callback and a delay argument after which the callback is executed. However since javascript is single threaded, the function is asynchronous, meaning that the callback is merely scheduled to run on the stack after the current thread completes its execution. This causes two problems: 
1. the delay argument is in reality the minimum time after which the callback is executed and not the exact time. This may cause marked delays in execution of the callback if the main thread is busy. Any code that comes after the setInterval() function will be executed first no matter the time it takes as it is scheduled earlier in the stack.
2.  Some times we may need successive delays i.e. setTimeout() inside the callbacks resulting in a complicated nested callback structure that cannot be replaced by setInterval().

Some other methods to solve these issues are:
### Using a loop that runs till a specified time passes. eg:
```javascript
function delay(ms) {
   ms += new Date().getTime();
   while (new Date() < ms){}
}
//code
delay(1000);
// code that needs to be run after delay
```
The main disadvantage here is that it freezes the browser for the time we want to pause.
### Using promises along with setTimeout()
```javascript
const delay = async t => new Promise(resolve => setTimeout(resolve, t));
```
and use this function inside an async function 
```javascript
await delay(1000);
```

## Degrading of timer accuracy due to security issues
Recently due to the use of security vulnerabilities like Meltdown and Sceptre which work by exploiting the accuracy of javascript timer, many browsers have intentionally degraded their clock performance to thwart these.
These vulnerabilities work by detecting subtle differences in the time taken to retrieve data from memory and cache. Thus by repeatedly queuing for restricted data and precisely measuring the time delay they can infer much about the confidential data itself.
Since changing the way browsers handle the cache or adding a new queue for confidential data is difficult the best solution seems to simply degrade the timer's capabilities to include errors in the order of milliseconds, as that would not cause a perceptible change in the use of these timer functions   and at the same time would remove the vulnerabilities.
