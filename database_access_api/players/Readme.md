# Players

In this package we will add the necessary methods to comunicate with the tables that contain the 
information of the players/referees. 

The tables that will use these methods are:

* jugadores: In this table we have the necessary data of the players and referees.
* campeonatos_arbitros: In this table we have the match between the championships and the referees. 
* campeonatos_jugadores: In this table we have the match between the championships and the players.
* jugadores_campeonato: In this table we have the results of each player in each championship.
* jugadores_pruebas: In this table we have the results of each player in each game. (Maybe not to use now).

## The package has the next methods.
### Generic
* build_id: Build a unique ID to identified at each player.

### Jugadores
* add: To add a new player, after to build its id.
* get_id: To download the data of a player using its ID. 
* get_phone: To download the data of a player using its phone number.
* get_email: To download the data of a player using its email.
* get_dni: To download the data of a player using its DNI.
* get_name: To download the data of a player using its name.
* get_id_list:  To download a list of IDs to build a correct ID. 
* update_email: To update the email of the player.
* update_phone: To update the phone of the player.
* update_nick: To update the nick of the player.
* update_talla: To update the size of the player.
* update_discapacidades: To update the dis-capacities of the player.
* update_observations, add_observations: To update the notes of the players. 


