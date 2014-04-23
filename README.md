Welcome to my Project! [See TODO for list of projects completed]

Currently running a version of my webserver @ mattao.com (Sometimes the server times out and crashes so I have to periodically restart it.  Can't figure out why yet)

Domain name registered through godaddy.com

Domain points to an EC2 server where I have the web server running on port 80

---

STEPS FOR SETTING UP ON A CLOUD SERVICE (Amazon Web Services):
1) Sign up for an account at aws.amazon.com
2) Go to your EC2 Dashboard
3) Click on "Launch Instance"
4) Select the recommended Amazon Linux AMI (Amazon Machine Language)
5) Use all default settings, but make sure the AMI size is micro, otherwise you'll get charged
6) Make sure you save your keypair in a safe location, you will need this to ssh to the server
7) Once the instance is created (May take some time), go to your EC2 Dashboard->Instances on the left
8) Select the instance you just created, then at the top click "Connect"
9) Amazon will show you the instructions to ssh into your server.  Follow em
10) Once connected to the server, you are going to need to update python to 2.7, see
http://www.lecloud.net/post/61401763496/install-update-to-python-2-7-and-latest-pip-on-ec2
11) run your server to listen on port 80, sudo python server.py -p 80
12) Now, if you go to your public IP (you can find that in your ec2 dashboard), you will be forwarded to your web server!  Congratulations
