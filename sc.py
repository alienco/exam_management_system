'''for teacher login Username="admin",Password="12345"
DESCRIPTION:
A teacher can make a test deciding no. of questions,
has to keep updated the student tables and assign them a username and password 
Each question will be MCQ
For every question a student can achieve max 4 marks and min -2 marks 
If all the marked option by the student is correct he will be given full 4 marks in that question.
In any other case he will be given -2 marks.
A student can give a test,analyse his performance in the past tests.
user defined functions:
   tmat=teacher makes a test
   sgat=student gives a test
   tms=teacher manages students
   sa=student identify their performance
   two=teachers window opened
   swo=students window open'''
def tmat():     #tmat=teacher makes a test
  print("Test name must be unique")
  n="testname"+input("Enter test name:")
  m.execute("create table "+n+"(q_no varchar(5),q varchar(1000),A varchar(100)\
    ,B varchar(100),C varchar(100),D varchar(100),c_ans varchar(4))")
  p=int(input("Enter no. of questions you want to add in a test:"))
  print("If question is more than one corect type answer otions it it in \
order\nIf correct options are A,B,D Enter ABD in Enter Corect Option/s:")
  for i in range(1,p+1):
    q=input("Enter Question no. "+str(i)+":")
    a=input("Enter Option A:")
    b=input("Enter Option B:")
    c=input("Enter Option C:")
    d=input("Enter Option D:")
    c_ans=input("Enter Corect Option/s:")
    s="Q"+str(i)
    m.execute("insert into "+n+"(q_no,q,A,B,C,D,c_ans) values(%s,%s,%s,%s,%s,%s,%s)",(s,q,a,b,c,d,c_ans))
    mydb.commit()
  print("You created the test sucessfully.")
  m.execute("show tables like 'stname%'")
  z=tuple(m)
  for i in z:
    m.execute("insert into "+i[0]+"(test_name) values ( %s)",(n,))
    mydb.commit()
  two()

def sgat():      #sgat=student gives a test
  r=0     #stores no. of questions attempted correctly
  w=0     #stores no. of questions attempted incorrectly
  print('Unattempted tests:')
  m.execute("select test_name from "+u+" where status='U'")
  for i in m:
   print(i[0])
  n=input("Enter the name of the test you want to perform:")    #n=Stores test name
  m.execute("select * from "+n)
  print("This paper contains MCQ's\nIf your answers are A,B,D Enter ABD \
in Enter your answer/s from A,B,C,D:\n+4:If all the options are correctly marked in order\n-2:Any other case")
  for i in m:
    (q_no,q,a,b,c,d,c_ans)=i  #q_no stores question no.,q stores question, 
    print(q_no ,end=' ')      #abcd stores four option respectively,c_ans stores correct option
    print(q)
    print("A:",a)
    print("B:",b)
    print("C:",c)
    print("D:",d)
    f=input("Enter your answer/s from A,B,C,D:")    #f stores option entered by student
    if(f==c_ans):
      r+=1
    else:
      w+=1
  m.execute("update "+u+" set cq=%s,wq=%s,marks=%s,status='A' where test_name=%s",(r,w,r*4-w*2,n))
  mydb.commit()
  print("You have attempted all the question")  
  print("Press 9 to go back\nPress 0 to exit")
  n=int(input("Enter Your Choice:"))
  if(n==9):
    sow()
  elif(n==0):
    exit()

def sa():
  m.execute("select * from "+u)
  for i in m:
    (t,c,w,ma,s)=i
    if(s=='A'):
      print("Test name:",t,"Correct questions:",c,"Wrong questions:",w,"Marks:",ma)
    else:
      print(t,"not attempted yet.")
  print("Press 9 to go back\nPress 0 to Exit")
  n=int(input("Enter Your Choice:"))
  if(n==9):
    sow()
  elif(n==0):
    exit()

def sow():
  print("\nPress 1 to give a test\nPress 2 to \
analyse your previous test performance\nPress 0 to exit")
  n=int(input("Enter your choice:")) 
  if(n==1):
      sgat()
  elif(n==2):
      sa()
  elif(n==0):
      exit()

def tms():      #tms=teacher manages students
  print("\nPress 1 to see no. of students already registed\nPress 2 to \
increase no. of entries of students\nPress 9 to go back\nPress 0 to exit")
  n=int(input("Enter Your Choice:"))
  if(n==1):
    m.execute("select * from login")
    for i in m:
      print("\nStudent name:",i[0],"\nUsername:",i[1],"\nPassword:",i[2])
    tms()
  elif(n==2):
    n=int(input("\nEnter no. of entries you like to make:"))
    for i in range(1,n+1):
      n=input("Enter Name Of Student:")
      u="stname"+input("Assign him a Username:")
      p=input("Assign him a Password:")
      m.execute("insert into login(name,username,password) values(%s,%s,%s)",(n,u,p))
      mydb.commit()
      m.execute("create table "+u+"(test_name varchar(50) unique,cq int,wq \
          int,marks int,status varchar(1) default 'U')")
         #cq=correct no. of question,wq=wrong no. of question

      m.execute("show tables like 'testname%'")
      z=tuple(m)
      for j in z:
        m.execute("insert into "+u+"(test_name)values(%s)",j)
        mydb.commit()
    print("No. of students updated Sucessfully.")
    two()
  elif(n==9):
    two()
  elif(n==0):
    exit()

def two():       #two=teacher windows open
   print("\nPress 1 to make a test\nPress 2 to see previous tests you \
had taken\nPress 3 to manage students\nPress 0 to exit")
   n=int(input("Enter your choice:"))
   if(n==1):
    tmat()
   elif(n==2):
     m.execute("show tables like 'testname%'")
     z=tuple(m)
     for i in z:
       print(i[0])
     two()
   elif(n==3):
    tms()
   elif(n==0):
    exit()

#main
import mysql.connector as cnt
mydb=cnt.connect(host="localhost",user="root",database="oems")
m=mydb.cursor()
print("Press 0 if you are a teacher\nPress 1 if you are a student")
n=int(input("Enter your choice:"))
if(n==0):
  for i in range(2,-1,-1):
    if(input("Enter Username:")=="admin" and input("Enter Password:")=="12345"):
      two()
      break
    else:
      print("Incorrect Username and Password combination.\nYou have",i,"attempts left")
  if(i==0):
    exit()
elif(n==1):
  print("Enter username in the format \
stname<username provided by teacher>\nEnter password as it is.")
  m.execute("select username,password from login")
  a=tuple(m)
  for i in range(2,-1,-1):
    j=None
    u=input("Enter Username:")
    p=input("Enter Password:")
    for j in a:
      if((u,p)==j):
        print("Congratulations!,You have sucessfully logged in")
        sow()  
    print("Incorrect Username and Password combination.\nYou have",i,"attempts left")
  print("Invalid Username and Password combination\n\
Contact administration for more information")
  exit()
