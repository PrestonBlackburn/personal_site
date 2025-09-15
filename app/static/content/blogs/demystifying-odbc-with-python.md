**Demystifying ODBC with Python**
=================================

Oct 16, 2024

![captionless image](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*5uJ26DUrddTzRJ6aYsxG_Q.png)

Open Database Connectivity (ODBC) — that extra download you needed to connect your database — has been a standard for accessing databases since the 90s. I’ve used ODBC drivers quite a bit for my day to day data engineering work, but hadn’t given them much thought other than “I need a database connection”. Its time to change that.

What do ODBC drivers actually do, and what would it look like to create an ODBC driver with Python?

I’m not settling for the abstract [Wikipedia definition](https://en.wikipedia.org/wiki/Open_Database_Connectivity):

> _In computing, Open Database Connectivity (ODBC) is a standard application programming interface (API) for accessing database management systems (DBMS) An application written using ODBC can be ported to other platforms, both on the client and server side, with few changes to the data access code._

Let’s look at some docs, diagrams, and code to figure out what is actually going on.

You can follow along by walking through the code in this repo: [ODBC explained with python](https://github.com/PrestonBlackburn/odbc-explained-with-python)

To fully understand ODBC, we’ll also need to look at communication with a database as a whole. When we need to reference database specific features we’ll use Postgres.

Below is a diagram showing the high level flow of database communication using ODBC with Postgres or a generic database. With that flow in mind we’ll start by looking at the protocols/standards that drive the implementations for each at the various stages in the communication flow.

![Postgres vs generic database communication flow](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*NNHxKKilG5IAuoAdMbgbSw.jpeg)

_*Note — typically the db interface and odbc driver are implemented in C/C++ for Python, but everything in this walkthrough will be pure python._

Background
----------

**The ODBC Standard**

ODBC, as a standard, defines a set of functions and types that must be implemented by an ODBC driver. There are a few versions of the ODBC spec, but we’ll just focus on the core features to better understand ODBC as a whole. Specifically, we’ll focus on the scenario where the ODBC driver processes calls and passes them to a separate database engine.

A summary of the ODBC spec functions and types can be found here:

*   [ODBC Function Summary](https://learn.microsoft.com/en-us/sql/odbc/reference/syntax/odbc-function-summary?view=sql-server-ver16)
*   [ODBC API Reference](https://learn.microsoft.com/en-us/sql/odbc/reference/syntax/odbc-api-reference?view=sql-server-ver16)

If we look through the ODBC functions we’ll find a lot of functions we’re not used to seeing in Python. One of the more familiar functions might be the **SQLExecuteDirect** function. In the docs we see that it “_executes a preparable statement, using the current values of the parameter marker variables if any parameters exist in the statement_.” Instead of a typical object returned in python, various SQL codes are returned by **SQLExecuteDirect**.

```
SQLRETURN SQLExecDirect(  
     SQLHSTMT     StatementHandle,  
     SQLCHAR *    StatementText,  
     SQLINTEGER   TextLength);  
```

If we continue digging into the ODBC functions we start to see more glimpses of lower level counterparts to typical functions we would use in python such as **connect**, **cursor**, and **execute**. Where Python’s **connect** may be mapped at some level to the ODBC **SQLAllocHandle** and **SQLSetEnvAttr**. Or something like the ODBC **SQLFreeStmt** seems related to calling something like cursor.close() in Python.

_SQLFreeStmt stops processing associated with a specific statement, closes any open cursors associated with the statement, discards pending results, or, optionally, frees all resources associated with the statement handle._

To better understand this mapping we also need to mention the Python higher level database API defined in [PEP 249 — the Python Database API Specification](https://peps.python.org/pep-0249/)

**Python — PEP 249**

Normally in Python, we work with higher level APIs defined in PEP 249. This specification is implemented at the python library level. For example the Python library pyodbc implements the python PEP 249 API and uses the ODBC functions provided by various ODBC drivers.

Example pyodbc PEP 249 API:

```
import pyodbc 
conn = pyodbc.connect('DSN=mydatasource;UID=user;PWD=password')
cursor = conn.cursor() 
cursor.execute("SELECT * FROM Employees") 
for row in cursor.fetchall(): 
  print(row) 
conn.close()
```

For a basic example of PEP 249 implementation, if we take a look at the pyodbc repo, we can see various PEP 249 standards, like the cursor object, implemented using C with various ODBC functions like the **SQLFetch —** [cursor.cpp file](https://github.com/mkleehammer/pyodbc/blob/master/src/cursor.cpp)

Now we have a general idea of how we can map from Python PEP 249 to the ODBC methods, but we are missing our ODBC driver. To implement our own ODBC driver, we need to drill down further and look at the communication protocol of the database itself. In the case of Postgres, this is the Postgres frontend/backend protocol.

**Postgres — Frontend/Backend Protocol**

Now we’ll start at the Postgres database itself and work towards its ODBC implementation. We know that we need to communicate with Postgres to tell it what query processing to do, then we need to communicate with Postgres to get our results back out. This is the purpose of the Postgres Frontend/Backend Protocol. This protocol uses message based communication over TCP between clients and servers.

The official Postgres libpq C library implements the postgres protocol. However, since I’m not very familiar with C, and I promised everything would be native Python, let’s create a our own (much simpler) implementation of the protocol using Python.

The Postgres protocol has a lot of different features, but we’ll just focus on the bare minimum to query Postgres using the protocol. To do this we’ll need to understand some basics.

Some great resources if you want to dive into the protocol:

*   [Postgres on the wire — A look at the PostgreSQL wire protocol](https://beta.pgcon.org/2014/schedule/attachments/330_postgres-for-the-wire.pdf)
*   [The PostgreSQL Protocol: The good, the Bad and the Future](https://www.youtube.com/watch?v=nh62VgNj6hY)

First we to look at two main message formats. The two types of messages we are concerned with are the startup packet and the regular packet.

A startup packet looks like:

```
| int32 len | int32 protocol version | payload | 
```

An example of the startup packet before being encoded as bytes might be:

```
36196608user0postgres0database0postgres00
```

*   36 would be the length of the message in bytes including itself
*   196608 is the protocol version
*   The username is postgres
*   The database name is postgres
*   0s are terminators

A regular packet looks like:

```
| chart tag | int32 len | payload | 
```

An example of the regular packet before being encoded as bytes might be:

```
Q39select * from information_schema.tables0
```

*   Q is the message type
*   39 would be the length of the message in bytes including itself
*   _select * from information_schema.tables_ is our query
*   0s are terminators

When we first connect to Postgres over a TCP socket we’ll send the startup packet. Once connection is established we can send and receive regular packets. For the sake of simplicity the only messages we will focus on are listed below:

*   **Q**: Query
*   **T**: Row Description
*   **D**: Data Row
*   **C**: Command Complete
*   **Z**: Ready for Query

Now we have everything we need to create our own python native ODBC implementation. Since the code for the full implementation ended up being somewhat long, we’ll just go through some key or interesting pieces.

**Implementation**
------------------

We’ll start by looking at the implementation of the Postgres protocol in Python. This is the lowest level of abstraction, and consists of a lot of reading and writing bytes to and from Postgres.

The code for the native postgres python implementation can be found in the [simple_pg_protocol.py](https://github.com/PrestonBlackburn/odbc-explained-with-python/blob/main/src/db_utils/simple_pg_protocol.py) file on GitHub

To get the postgres protocol to work nicely with python PEP 249 and ODBC spec, I ended up creating a **ConnectionHandle** class, which just spawns a new TCP socket. Basically the socket ends up being the “handle” in the ODBC implementation and the “Connection” in PEP 249.

Postgres Protocol

```
@dataclass
class ConnectionHandle:
    sock: socket.socket = field(default_factory= lambda: socket.socket(socket.AF_INET, socket.SOCK_STREAM))
```

ODBC Handle Implementing ConnectionHandle

```
def SQLConnect(
        sqlhdbc: ConnectionHandle,
        server_name: str, # ex: 'localhost'
        server_name_length: int, # ex: 9
        user_name: str, # ex: 'postgres'
        user_name_length: int, # ex: 8
        authentication: str, # ex: 'none'
        authentication_length: int # ex: 4
) -> ReturnCode:
    _logger.debug("Running SQLConnect ODBC Function")
    try:
        parameters = {
            'host': server_name,
            'port': 5432,
            'user': user_name,
            'database': 'postgres',
        }
        startup(parameters, sqlhdbc)
        return_code = ReturnCode("SQL_SUCCESS")
    except Exception as e:
        _logger.error(e)
        return_code = ReturnCode("SQL_ERROR")
    return return_code
```

PEP 249 Implementing ConnectionHandle

```
class Connection:
    def __init__(self, params:dict):
        self.params = params
        self.handle = pg.startup(params, pg.ConnectionHandle())
```

The biggest challenge at the Postgres protocol level is just making sure you receive all of the message content from the Database without starting to read the next message. It can be pretty hard to troubleshoot when the byte stream is shifted slightly off and you need to trace back where something got shifted.

In all implementations I wrapped the socket with a generator to help facilitate the message reading. With a generator we don’t need to wait for all of the results to be available before doing whatever downstream tasks we want on the rows.

Source Code: [simple_pg_protocol.py](https://github.com/PrestonBlackburn/odbc-explained-with-python/blob/main/src/db_utils/simple_pg_protocol.py)

```
def fetch_message(handle: ConnectionHandle) -> Generator[bytes, None, None]:
    sock = handle.sock
    message_length = 1
    while message_length > 0:
        char_tag = recv_exact(sock, 1)
        _logger.debug(f"got char_tag from sock: {char_tag.decode('utf-8')}")
        length = recv_exact(sock, 4)
        payload_len = int.from_bytes(length, 'big') - 4 # 4 bytes for length
        _logger.debug(f"got length from sock: {payload_len}")
        part = recv_exact(sock, payload_len)
        _logger.debug(f"got part from sock: {part}")
        message_length = len(char_tag) + len(length) + len(part)
        yield char_tag + length + part
```

The postgres protocol returns additional info with its messages that I decided were out of scope, but would be important in a real implementation. The field type and data size are returned as part of the row information, and in a full implementation those types should be used to cast the message response to the correct data types.

At this point we could get all of the information out of Postgres that we need. We can query the database and get the response. However we are not following python’s PEP 249 and we have not implemented the ODBC spec. We can now see how in a real world scenario and ODBC and PEP 249 implementation on top of what we have done can add additional overhead and there could be potential performance considerations. These performance considerations are why we rarely see any (are there any?) implementations of ODBC in pure Python.

Example ODBC Function in Python

Source Code: [odbc_driver.py](https://github.com/PrestonBlackburn/odbc-explained-with-python/blob/main/src/db_utils/odbc_driver.py)

```
def SQLExecDirect(
        sqlhstmt: ConnectionHandle,
        statement: str,
        statement_length: int
) -> ReturnCode:
    _logger.debug("Running SQLExecDirect ODBC Function")
    try:
        execute(sqlhstmt, statement)
        return_code = ReturnCode("SQL_SUCCESS")
    except Exception as e:
        _logger.error(e)
        return_code = ReturnCode("SQL_ERROR")
   
    return return_code
```

Most things lined up, but I did end up needing to create the **get_data** function to support the **SQLGetData** ODBC function. Another caveat is that in one case I return the handle instead of an ODBC response code, which technically doesn’t follow the ODBC protocol, but simplifies things for me. The bulk of the lifting is done by the postgres protocol client implementation, so adding the ODBC response codes was the main task.

Now that we have our ODBC driver, we can implement our Python PEP 249 on top of it. The primary implementations here are the connection object and cursor objects. These functions also map fairly closely to the ODBC specification

PEP 249 Implementation using ODBC functions

Source Code: [pep_249_odbc_manager.py](https://github.com/PrestonBlackburn/odbc-explained-with-python/blob/main/src/db_utils/pep_249_odbc_manager.py)

```
import db_utils.odbc_driver as odbc
from typing import List
def connect(params:dict):
    return Connection(params)
class Cursor:
    def __init__(self, handle: odbc.ConnectionHandle) -> None:
        self.rowcount = None
        self.description = None
        self.handle = handle
        self.columns = []
       
    def close(self) -> None:
        odbc.SQLDisconnect(self.handle)
        return
   
    def execute(self, query:str) -> None:
        odbc.SQLExecDirect(self.handle, query, len(query))
        self.results_generator = odbc.SQLFetch(self.handle)
        return
   
    def fetchone(self) -> tuple:
        # Not implemented
        pass
   
    def fetchall(self) -> List[tuple]:
        columns, rows = odbc.SQLGetData(self.results_generator)
        if columns != []:
            self.columns = columns
        return rows
class Connection:
    def __init__(self, params:dict):
        self.params = params
        self.host = params['host']
        self.handle = odbc.ConnectionHandle()
        odbc.SQLConnect(
            self.handle,
            params['host'],
            len(params['host']),
            params['user'],
            len(params['user']),
            'none',
            4
        )
    def close(self) -> None:
        odbc.SQLDisconnect(self.handle)
        return
   
    def commit() -> None:
        # we won't be using this method
        # assume "autocommit"
        return
   
    def cursor(self) -> Cursor:
        return Cursor(self.handle)
```

We can also implement PEP 249 without ODBC and instead directly use the postgres protocol

Source Code: [pep_249.py](https://github.com/PrestonBlackburn/odbc-explained-with-python/blob/main/src/db_utils/pep_249.py)

```
import db_utils.simple_pg_protocol as pg
from typing import List
def connect(params:dict):
    return Connection(params)
class Cursor:
    def __init__(self, handle: pg.ConnectionHandle) -> None:
        self.rowcount = None
        self.description = None
        self.handle = handle
        self.columns = []
       
    def close(self) -> None:
        pg.disconnect(self.handle)
        return
   
    def execute(self, query:str) -> None:
        pg.execute(self.handle, query)
        self.results_generator = pg.fetch_message(self.handle)
        return
   
    def fetchone(self) -> tuple:
        columns, row = pg.get_row(self.results_generator)
        if columns != []:
            self.columns = columns
        return row
   
    def fetchall(self) -> List[tuple]:
        columns, rows = pg.get_data(self.results_generator)
        if columns != []:
            self.columns = columns
        return rows
class Connection:
    def __init__(self, params:dict):
        self.params = params
        self.handle = pg.startup(params, pg.ConnectionHandle())
    def close(self) -> None:
        pg.disconnect(self.handle)
        return
   
    def commit() -> None:
        # we won't be using this method
        # assume "autocommit"
        return
   
    def cursor(self) -> Cursor:
        return Cursor(self.handle)
```

The diagram below compares a typical postgres odbc communication stack with our python native postgres communication stack. Every layer except the database can be written in Python, and maybe there should be an official native Python implementations for educational purposes or to simplify things where performance is not a concern.

![Typical Postgres implementation vs our Python implementation](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*rEIusLMvhkc_zXgStfNySg.jpeg)

There you have it — we have our own (simple) Python native ODBC Postgres driver. Hopefully this has given you a more concrete idea of what ODBC is, and what is really happening when you download that ODBC driver to connect to your database. It definitely gives me a new appreciation for open source maintainers of database tools like libpq, pyodbc, and psycopg.

**Going Further**

Along with understanding ODBC, there are also a few trends in Python / data engineering that I’ve seen that we can get a better grasp on now that we better understand database communication flows.

It seems like there are more and more python native database connectors that don’t rely on ODBC. The [**psycopg**](https://www.psycopg.org/) library uses the Postgres C library [libpq](https://www.postgresql.org/docs/9.5/libpq.html) and the [**pymssql**](https://www.pymssql.org/) uses the [FreeTDS](https://www.freetds.org/) C library. In cases like these when you don’t need ODBC it should be more performant to use the Python C library wrapper modules instead of reaching for an ODBC driver. A rule of thumb should be to look for a Python native db connector before using a library like [**pyodbc**](https://github.com/mkleehammer/pyodbc).

After implementing this database communication workflow, I can better see why the [Apache Arrow format](https://arrow.apache.org/overview/) is gaining popularity. The Arrow format’s goal is to have standardized, columnar, in memory types. It can help standardize the type mapping from something like Postgres to Python and allow for interop between other systems using the same format. Having an option for moving columnar formatted data over the network instead of the row based format we used could result in some large speed ups for things like analytical queries.