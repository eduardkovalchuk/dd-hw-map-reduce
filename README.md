# dd-hw-map-reduce
implementation of map reduce

There are two types of nodes: a Master and  a Slave.
Task (with implemented Map and Reduce classes) is submitted to the master, the master sends task to slaves (where data is located) and triggers execution of "map phase" on slaves. After execution on slaves result goes back to the master and then shuffle and reduce conducted.

