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
* _new_id: Build a unique ID to identified at each player, use the name and surname. 
* _invalid_data: To test if some data are previous loaded into the data base.
* _locate_id: to be sure that we have a different player ID, we count how many players
have the same letters in their id_player.

### Jugadores
* add: To add a new player, after to build its id.
* get: To recover a player using any of the uniques datas
  * email
  * phone
  * dni
  * id_player
* update: To update a field of a player, we will use the id_player to locate the player. We can update more than one 
fields at the same time.

