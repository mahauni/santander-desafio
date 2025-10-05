from neo4j import GraphDatabase

from app.core.config import settings

URI = settings.NEO4J_URI
AUTH = (settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD)

driver = GraphDatabase.driver(URI, auth=AUTH)


# def load_csv_with_neo4j_load(session, csv_path: str):
#     """Alternative: Use Neo4j's LOAD CSV (file must be accessible to Neo4j)"""
#     # Note: CSV file must be in Neo4j's import directory or use file:// URL
#     query = """
#     LOAD CSV WITH HEADERS FROM 'file:///' + $filename AS row
#     CREATE (p:Person {
#         name: row.name,
#         age: toInteger(row.age),
#         email: row.email
#     })
#     """
#     session.run(query, filename=os.path.basename(csv_path))
#     print("Loaded data using Neo4j LOAD CSV")
#
#
# def create_indexes(session):
#     """Create indexes for better query performance"""
#     try:
#         session.run("CREATE INDEX person_name IF NOT EXISTS FOR (p:Person) ON (p.name)")
#         session.run(
#             "CREATE INDEX person_email IF NOT EXISTS FOR (p:Person) ON (p.email)"
#         )
#         print("Indexes created")
#     except Exception as e:
#         print(f"Index creation error (may already exist): {e}")
#
#
# def clear_database(session):
#     """Clear all nodes and relationships"""
#     query = "MATCH (n) DETACH DELETE n"
#     session.run(query)
#     print("Database cleared")
#
#
# def preload_data(driver: Driver):
#     """Preload all CSV data into Neo4j"""
#     with driver.session() as session:
#         # Optional: Clear existing data
#         # clear_database(session)
#
#         # Create indexes first
#         create_indexes(session)
#
#         # Load data from CSVs
#         load_persons_from_csv(session, "data/persons.csv")
#         load_relationships_from_csv(session, "data/relationships.csv")
#
#         # Alternative method:
#         load_csv_with_native_csv(session, 'data/persons.csv')
#
#         print("Data preload completed")
