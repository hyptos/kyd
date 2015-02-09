KYP
==============

![](https://magnum.travis-ci.com/hyptos/kyd.svg?token=gSMNMRn5ygdjm4n6o1XK)

Authors :

    Carole Bonfré
    
    Antoine Martin

Tutors : 

    Eddy Caron
    
    Yves Caniou 
 
University Claude Bernard Lyon 1 

Get started
===============

Install dependencies :

    pip install -r requirements.txt

Run all tests :

    nosetests
    
Todo
===============
    - Add more documentation
    - Add mongo insertion
    - Begin the paper of research
    - Add mongo client to query results
Tutorial
===============

How to use the application

![](http://imgur.com/Cr8gN8p)

Clean all results :

    make clean
    
Compile all results into one file :

    make compile
    
Samples : 

Launch a bench on amazon with a random file of 2048 bytes, the tests will be run 5 times by default

    python bench.py -od amazon -s 2048

Result :

![](http://imgur.com/EtAIbLG)

Launch a bench on amazon and googledrive with a random file of 4096 bytes, the tests will be run 3 times.

    python bench.py -od amazon googledrive -n 3 -s 4096

Result :

![](http://imgur.com/Lh8Qd3I)


Licence
===============
See the LICENCE file
