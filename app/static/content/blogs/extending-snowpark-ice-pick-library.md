Extending Snowpark Ice Pick Library
================================================

Apr 10, 2023

![Ice Pick Logo](/static/img/blogs/snowpark-ice-pick-library/ice_pick_padded.png)

On a project I found myself creating a script for extracting DDL for various Snowflake objects for the 3rd or 4th time.  
Currently, extracting the DDL with Python is a somewhat clunky process, where you'll need to use **Snowpark** to execute SQL
statements since there is no native Snowpark support to get metadata like the DDL of an object.  
However, by extending the Snowpark library we can add additional functionality, such as getting DDL,
that has a “native” Snowpark feel. This is what I've attempted to achieve with the **ice pick** library.  

The two key challenges to creating the extension are:
- giving the extension a native feel  
- finding the appropriate abstractions for the functionality I wanted to add  

---

**Ice pick docs:**  
[https://ice-pick.readthedocs.io/en/latest/notebooks/tutorial.html](https://ice-pick.readthedocs.io/en/latest/notebooks/tutorial.html)  

**Ice pick repo:**  
[https://github.com/PrestonBlackburn/ice_pick](https://github.com/PrestonBlackburn/ice_pick)  

---

## Snowpark background

Snowpark has a lot of great functionality built-in, and allows users to easily interact with Snowflake using Python (and other languages).  
With Snowpark, you can push down compute to Snowflake to reduce data transfer costs. **DataFrames** make up the core of Snowpark, 
and represent a set of data and methods to operate on that **data**.  

While Snowpark is focused on data manipulation, **ice pick** extends Snowpark to provide support for manipulating **Snowflake objects**.  
In the case of a table object, base Snowpark manipulates the data in a table, and the ice pick extension helps get and manage metadata about that table.  

---

## Extending The Snowpark Session

To integrate the library with Snowpark and give it a native feel, I decided the most natural approach was to extend the **Snowpark Session** class.  
By extending the Session, ice pick functions can be called the same way Snowpark functions are called.  

For example:  

In Snowpark to create a `DataFrame` object instance:  

```python
df = session.table("TEST.SCHEMA_1.CUSTOMER")
results = df.collect()
```

In Ice Pick to create a SchemaObject instance:
```python
table_obj = session.create_schema_object('TEST', 'SCHEMA_1', 'CUSTOMER', 'TABLE')
ddl = table_obj.get_ddl()
```

In both cases, the session is used to create an instance of an object. To extend the Snowpark session I used a technique called monkey patching. 
Monkey patching allows you to dynamically change or add a behavior to code at run-time. The upsides to this approach are that it gives the extension
a native feel since we are actually adding methods to the Snowpark Session. However, there are a few downsides including, that it can be dangerous 
if fundamental changes are made to the Snowpark Session class, and that it may be better to make changes upstream in the Snowpark library itself. 
For the second point, eventually, it would be nice to update Snowpark to include this functionality instead of relying on an extension, but a lot 
of the additional functionality may be out of scope for Snowpark. Snowpark is focused on providing an alternative to Pyspark, and adding support 
for Schema Objects and higher-level functions does not fit within that scope (my thoughts, not those of Snowflake).

## Ice Pick Abstractions

So far the two main classes I've added are the **SchemaObject** and the **SchemaObjectFilter**.  

- The `SchemaObject` represents an object that lives in a Snowflake Schema.  
  Generally schema-level objects have similar rules (with a few exceptions), so they will be interacted with in the same way.  
  Snowflake references many of these objects as “database” objects (see [Snowflake docs reference](https://docs.snowflake.com/en/sql-reference/sql/desc)),  
  but I chose to separate out schema objects to preserve a common path format amongst the schema objects.  
  Database objects also include schemas which do not follow the naming convention of all other schema objects:  
  `"database.schema.object"`.  

- The `SchemaObjectFilter` exists to return specific or many `SchemaObjects`.  
  This makes it convenient to get bulk properties of SchemaObjects such as DDL, grants, descriptions, etc.  
  With just a couple of lines of code you can retrieve the DDL for all schema-level objects in a Snowflake account.  

---

## Example Usage

Along with building the ice pick library I also wanted to work on my code documentation.  
For documentation I've created a **Read the Docs** page using Sphinx:  
[Ice Pick - Read The Docs Page](https://ice-pick.readthedocs.io/en/latest/)  

![read the docs example](/static/img/blogs/snowflake-ice-pick-library/read_the_docs_ice_pick.png)  

I'd highly recommend checking out this YouTube video if you are interested in learning more about getting started with Sphinx:  
[Document Your Scientific Project With Markdown, Sphinx, and Read the Docs | PyData Global 2021](https://www.youtube.com/watch?v=qRSb299awB0)  

---

## Final Thoughts

I plan on continuing to build out ice pick to improve my Snowflake development experience (and hopefully other peoples!).  
I'm working on adding some higher-level functions, such as an **`auto_union`** function to make it easier to union tables with different and overlapping columns.  
If you have any ideas or want to contribute feel free to reach out or create a pull request!  
