# RethinkDB REST API

Exposes RethinkDB as a firebase-like REST API

### Dependencies

- Python
- Flask
- RethinkDB
 
### Set up

1. Download the ``main.py`` file and put it on your machine.
2. Put your [RethinkDB connection](https://github.com/freshtacos/rethinkdb-api/blob/master/src/main.py#L14) information on the script.
3. Set up the [routes table](https://github.com/freshtacos/rethinkdb-api/blob/master/src/main.py#L17) with your corresponding tables and indexes.
4. Generate a [complex key](https://github.com/freshtacos/rethinkdb-api/blob/master/src/main.py#L11).
5. Run the ``main.py`` file with Flask.

### Http Methods

| Method        | Description                              |
| ------------- | ---------------------------------------- |
| GET /%s       | gets the JSON of all documents in the table |
| GET /%s/%s    | gets the JSON of the last item in the path, or ``null`` if the value doesn't exist |
| POST /%s/%s   | either updates the table with the JSON body, or creates a new entry |
| DELETE /%s/%s | deletes the item(s) from the table       |

### Examples

- Get all documents in the ``people`` table:

  - GET /people?key=KEY

- Get Joe's information from the people table:

  - GET /people/joe/?key=KEY

- Joe doesn't exist in the table, so let's put him in:

  - POST /people/joe/?key=KEY

  - JSON body:

    - ```json
      {
      	"name": "Joe",
      	"last_name": "Smith"
      }
      ```

- Maria's last name is incorrect. Let's update it:

  - POST /people/maria/?key=KEY

  - JSON body:

    - ```json
      {
      	"last_name": "Jones"
      }
      ```

- We don't need John anymore; let's delete his entry:

  - DELETE /people/john/?key=KEY

### Structures

Each request is structured as: /TABLE/PATH/OF/THE/ITEM/?key=KEY, which is identical to the Firebase REST API.

Let's assume we have a folder structured like this:

- Directory
  - Membership
    - Active_Users
    - Inactive_Users

To get all Active Users, we would do: GET /directory/membership/active_users/?key=KEY
