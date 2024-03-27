# Hosts

In this package, we will add the necessary functions to manage the table "sedes" that will contain the Hosts' data. 

## Database

In this case, I will not define a RAW and Silver layer, because we expect that we will load teh data correctly from the 
beginning, and we will not need a record from old data.

## Actions
As every time, we would:

* Add. A new host.
* Update. An old host.
* Look for. Hosts. 

## id_sede

This data must be unique; it will be built with the "provincial" field plus a number. 

If the province has more than one word in the name, 
we will build the ID  after to capitalize all the words and delete the spaces.

