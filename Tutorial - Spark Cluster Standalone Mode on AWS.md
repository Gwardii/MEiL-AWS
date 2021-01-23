# Setting up a Cluster on AWS with Putty and Apache Spark / Installing Jupyter



This tutorial is based on:
https://dzone.com/articles/apache-spark-setting-up-a-cluster-on-aws
https://github.com/mrkjankowski/Tutorials/blob/master/%23Setting%20up%20a%20Cluster%20on%20AWS%20with%20Putty%20and%20Apache%20Spark.md
https://github.com/OskarBienko/Spark-cluster/blob/Spark-cluster/Deploying%20the%20Spark%20cluster.md

### 1. Create AWS Instance (Select Ubuntu Server) and download PuTTY

Set up security group. The easiest eay is to let any IP to connect to any port but remember that is also the least safe.
Necessary is to allow port 22 to connect with your desktop computer's IP and port 7077 with your slaves IP. But unless you are not affraid of lack of security, go the easiet way as I did and as it is shown:

![0](https://github.com/Gwardii/MEiL-AWS/blob/main/pictures/awsSecurity.png)


Make template (common for both types master and slave) for your instance so you will be able to make as many of them as you wish without much more effort.
I used ubuntu distribution so choose the same or feel free for any other but some commands may not work.

Copy and paste [this shell](script) script in User data (also with the prefix "#!/bin/bash"). I will describe later what this commands do.

![0](https://github.com/Gwardii/MEiL-AWS/blob/main/pictures/awsBash.png)

### 2. SSH into your instance 

 You can SSH without PuTTY but I would recommend to use it.
 
 Download your EC2 key pair file and convert it to ppk format in PuTTYGen and then lunch PuTTY.
 Make two sessions : slave and master
 The only difference between them is tunneling so start with the slave.
 Slave:
 Set path to your key pair in ppk format:
 
![0](https://github.com/Gwardii/MEiL-AWS/blob/main/pictures/puttyAuth.png)

 Set connection settings as shown. In other case PuTTY will end your connection if you don't have any activity for some time.

![](https://github.com/Gwardii/MEiL-AWS/blob/main/pictures/puttyConnection.png)

Name your session and save it:

![](https://github.com/Gwardii/MEiL-AWS/blob/main/pictures/puttySlaveSession.png)

Master:
Load your slave session and set up tunneling as shown:

![](https://github.com/Gwardii/MEiL-AWS/blob/main/pictures/puttyTunneling.png)

There are required two tunnels:
   8000 -> localhost:8888 for jupyter notebook
   8001 -> localhost:8080 for spark cluster manager
Name session and save it like before.

To SSH into your instance just choose either you connect to master or slave. Load session and write in host name:
ubuntu@"yourEC2instancePublicIP" for example ubuntu@11.111.11.11
You can use public DNS instead of IP.
Click open and you should be connected.

![](https://github.com/Gwardii/MEiL-AWS/blob/main/pictures/puttyHostName.png)
### 3. Step by step

 Not necessery but worth to be done. These commands will make apt-get up to date.

```
apt-get update
apt-get upgrade -y
```

cd moves to specified directory.
wget downloads file from the web. Be aware that the version of Spark may change so before you should visit this website:
http://ftp.man.poznan.pl/apache/spark
tar unzips downloaded file

```
cd /usr/local/
wget http://ftp.man.poznan.pl/apache/spark/spark-3.0.1/spark-3.0.1-bin-hadoop2.7.tgz
tar xvzf spark-3.0.1-bin-hadoop2.7.tgz
```

These echo commands append the file with text in paranthesis. $ means that you use a variable so separate $ sign from var name.
export set up local variable and .bashrc is executed every time you SSH.
But because the session was estabilished before we need to source it, because we will need these variables.
```
echo "export SPARK_HOME=/usr/local/spark-3.0.1-bin-hadoop2.7" >> /home/ubuntu/.bashrc
......
echo "export PATH=$""PATH:$""ANACONDA/bin" >> /home/ubuntu/.bashrc
source /home/ubuntu/.bashrc
```

We need scala and java for spark and that's how you get it.

```
apt-get -y install openjdk-8-jdk-headless
apt-get install scala -y
```

We need to install anaconda. Slave nodes does not require whole anaconda but all nodes should have same version of Python.
Pip is for installing python packages and is needed only on master.
chown command change owner of the directory. Because we use shell script from user data, all the commands are executed with root level so we need to use chown.
You can also copy paste (in putty u paste with right mouse button) all commands to terminal after SSH, but some of commands may need sudo prefix. They simply need root level.

```
cd /home/ubuntu/
wget https://repo.anaconda.com/archive/Anaconda3-5.3.1-Linux-x86_64.sh -O anaconda.sh
bash anaconda.sh -b -p anaconda
source .profile
conda install pip -y
chown -R ubuntu $SPARK_HOME
```

### 4. Startup Master
Following commands need to be done in terminal

On master you need to install two packages with specified version:

```
sudo chown -R ubuntu $ANACONDA
pip install twisted==18.7.0
pip install py4j==0.10.9
```

Now you can start your master node. Just type:

```
$SPARK_HOME/sbin/start-master.sh

```
Now start jupyter:

```
jupyter notebook
```

Copy paste link with token to browser on your computer and change localhost:8888 to localhost:8000 (tunnel)

![](https://github.com/Gwardii/MEiL-AWS/blob/main/pictures/jupyter.png)

### 5. Startup Slave

Type "localhost:8001" into your browser and connect.
Copy the spark url (with spark prefix)

![](https://github.com/Gwardii/MEiL-AWS/blob/main/pictures/sparkUrl.png)

SSH to your slave node and type:

```
$SPARK_HOME/sbin/start-slave.sh "paste here spark url (right click)"
```
Refresh localhost:8001 and check if it worked.

![](https://github.com/Gwardii/MEiL-AWS/blob/main/pictures/1-4000.png)
Voilà!

