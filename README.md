# Assignment3

1.	Develop a mechanism to generate the requests your system faces.

The file https://raw.githubusercontent.com/gregory1506/Assignment3/master/create1million.py contains the code used to generate the 1 million requests. A python script asynchronous writes to a queue over the Azure Rest API. 1million entries sent to queue in ~1934seconds

2.	Design and implement a solution using a  container-based approach or a 
virtual machine-based one to process 1 million requests in an hour.  
For your receivers introduce a failure rate. 
Store the occurrence of failures. 
Justify how you chose to store and monitor failures. 

In the generation step an attribute called “failure” was introduced and was labelled as such for every 50000th entry to the queue (the assignment did not specify if the failure should be random). The failures were written to a separate queue for processing at a later time to simulate an actual failure. Because the REST API was used again, the http response status codes of non manual failures (actual https failures) was used to monitor failures. The appropriate actions was then taken accordingly. See Code snippets :

https://raw.githubusercontent.com/gregory1506/Assignment3/master/sastoken.py 
This Code generates the token required to communicate over the REST API.

https://raw.githubusercontent.com/gregory1506/Assignment3/master/config.py
The Configuration file to house the queuename, tablename and failure queue name.

https://raw.githubusercontent.com/gregory1506/Assignment3/master/read.py
Asynchronously read from the Service bus queue that holds the json requests. Once a read is confirmed it is deleted from the queue and writted to an azure table as permanent storage

https://raw.githubusercontent.com/gregory1506/Assignment3/master/server.py
This will become part of a linux service. It basically uses a bottle framework to produce a web server. Produces simple text to show the size of the Service bus Queue and the elapsed time. Wish I knew javscript/jquery to makes this info more exciting......but another time since its not part of assignment. Cane be accessed after about 5 mins of launching ARM template visa publicip:9000

https://raw.githubusercontent.com/gregory1506/Assignment3/master/worker.py
The Worker service that runs on an infinite loop to process messages on the queue. Adjusts workload based on size of queue.

The ARM template can be found here: https://raw.githubusercontent.com/gregory1506/Assignment3/master/Assignment3/azuredeploy.json 
A copy is also saved in the Irwin Williams profile of Gregory Olliviere azure account. It is called almostfinala1

3. Justify and cost your design.

 Our design uses a Service Bus Queue to house the requests and a Table to store them. Once the ARM template is lauched a A1 VM scale is generated to run a server and a worker service in the background. The scale set scales up and down based on the size of the queue. So if the queue has more than 100K items another VM is spawned with the same worker and server services running. So this way the workers on each VM can combine efforts to process the queue faster. Our testing showed 1million messages processed in 2007.5 seconds reaching a maximum of 4 A1 VM's running ubuntu server 17.10.
 Our design Costs are as follows :
 Service Bus ----> $10/month + First 13M ops/month 	Included
                    Next 87M ops (13M–100M ops)/month 	$0.80 per million operations
                    Next 2,400M ops (100M–2,500M ops)/month 	$0.50 per million operations
                    Over 2,500M ops/month 	$0.20 per million operations 

Table Storage ----> First 1 TB / Month 	$0.07 per GB
                    $0.00036 per 10,000 transactions

Virtual Machines ----> A1 $0.024/hour per VM

So for roughly 2 hrs concerning the assignment we estimate ~4USD exluding the 10USD upfront cost of the Service Bus Queues.

4. How would your design treat with a doubling of the load? 

Our current design may fall just short of proccessing 2million transactions in an Hour, but a simple alteration to the Scaling Metric could handle this case. Specifically the Queue Size threshold could be dropped to 50000 rather than 100000 currently. Also rather than just scaling up 1 VM at a time a single scale up could add 2 VM's for example.

