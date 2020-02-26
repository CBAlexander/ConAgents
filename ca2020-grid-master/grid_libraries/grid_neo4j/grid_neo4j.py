import pandas as pd
from neo4j import GraphDatabase
from datetime import datetime


class GridNeoConnector():
    # Dataset paths
    MAP_DATASET = 'import/building.csv'
    EVENT_DATASET = 'import/event.csv'
    CQL_SCRIPT = 'import/import.cql'

    def __init__(self, logger):
        self.logger = logger
        self.driver = self.connectToNeo()

    def connectToNeo(self):
        uri = 'bolt://172.17.0.1:7688'
        usr = 'neo4j'
        pwd = 'gridproject2019!'

        try:
            graphDB_driver = GraphDatabase.driver(uri, auth=(usr, pwd))
        except Exception as e:
            self.logger.error(e)
        self.logger.info("Connected to Neo4J")
        return graphDB_driver

    def toDate(self, date, hour):
        return datetime.utcfromtimestamp(int(date)).strftime('%Y-%m-%d')+' '+str(int((hour/60)/60))+':'+str(int((hour%(60*60)/60))).zfill(2)+':00'

    def csv_to_neo4j(self):

        # CSV map extraction
        df = pd.read_csv(self.MAP_DATASET)
        room_column = df.name.tolist()
        room_connection = df.connected_to.tolist()

        buff = []
        for i in range(len(room_column)):
            buff.append([room_column[i], room_connection[i].split(',')])

        # Execute the CQL queries
        with self.driver.session() as graphDB_Session:
            crea_query = ""

            # Create the rooms
            for j in range(len(buff)):
                crea_query = 'MERGE (:room {name:"'+buff[j][0]+'"});'
                graphDB_Session.run(crea_query)

            # Links them
            for k in range(len(buff)):
                for l in range(len(buff[k][1])):
                    crea_query = 'MATCH (a:room {name:"'+buff[k][0]+'"}),(b:room {name:"'+buff[k][1][l]+'"}) '
                    crea_query = crea_query + 'MERGE (a)-[c:connected_to]->(b) '
                    crea_query = crea_query + 'RETURN c;'
                    graphDB_Session.run(crea_query)

        print("Database loaded")

    def get_rooms(self):
        cql_get_rooms = "MATCH (r:room) RETURN r.name"
        room_list = []
        with self.driver.session() as graphDB_Session:
            results = graphDB_Session.run(cql_get_rooms)
            for record in results:
                room_list.append(record["r.name"])
            return room_list

    def find_shortest_path(self, starting_room, targeted_room, stairs):

        path = []
        cqlShortestPath_stairs = 'MATCH path=shortestPath((:room {{name:"{0}"}})-[*..10]-(:room {{name:"{1}"}})) WHERE NONE(x IN NODES(path) WHERE (x.name = "accessible_lift")) RETURN path'
        cqlShortestPath_elevator = 'MATCH path=shortestPath((:room {{name:"{0}"}})-[*..10]-(:room {{name:"{1}"}})) WHERE NONE(x IN NODES(path) WHERE (x.name = "stairs")) RETURN path'

        with self.driver.session() as graphDB_Session:

            # Find the shorstest path between two rooms
            if(stairs):
                shortestPath = graphDB_Session.run(cqlShortestPath_stairs.format(starting_room, targeted_room))
            else:
                shortestPath = graphDB_Session.run(cqlShortestPath_elevator.format(starting_room, targeted_room))

            for record in shortestPath:
                nodes = record['path'].nodes
            for node in nodes:
                path.append(node.get('name'))
            return path

    def find_event_given_title(self, event_name):
        cqlevent = 'MATCH (a:event) WHERE toLower(a.title) CONTAINS "{0}" RETURN a.title, a.location, a.description, a.start, a.end'
        with self.driver.session() as graphDB_Session:
            result = graphDB_Session.run(cqlevent.format(event_name)).values()
            return result

    def find_event_given_date(self, event_date):
        cqlevent = 'MATCH (a:event) WHERE a.start CONTAINS "{0}" RETURN a.title, a.location, a.description, a.start, a.end'
        with self.driver.session() as graphDB_Session:
            result = graphDB_Session.run(cqlevent.format(event_date)).values()
            # logger.info(cqlevent.format(event_date))
            return result

    def find_event_given_room(self, name):
        cqlevent = 'MATCH (b:room {{name:"{0}"}})-[:located_at]-(a:event) RETURN a.title, a.location, a.description, a.start, a.end'
        with self.driver.session() as graphDB_Session:
            result = graphDB_Session.run(cqlevent.format(name)).values()
            # self.logger.info(cqlevent.format(name))
            return result

    def find_event_given_person(self, person_name):
        cqlevent = 'MATCH (a:event) WHERE toLower(a.description) CONTAINS "{0}" RETURN a.title, a.location, a.description, a.start, a.end'
        with self.driver.session() as graphDB_Session:
            result = graphDB_Session.run(cqlevent.format(person_name.lower().strip())).values()
            return result

    # Remove events from response that are older than current time.
    def remove_old_events(self, events):
        return_events = []
        for event in events:
            print(event)
            if datetime.strptime(event[4][:-6], '%Y-%m-%d %H:%M:%S') >= datetime.now():
                return_events.append(event)
        return return_events

    # /!\ Do not keep the sorting. Better call this function before 'sort_events'
    def merge_event_lists(self, events1, events2):
        events1_tuple = []
        events2_tuple = []

        if events1 is not None:
            for event in events1:
                events1_tuple.append(tuple(event))

        if events2 is not None:
            for event in events2:
                events2_tuple.append(tuple(event))

        if events1 is not None and events2 is not None:
            return list(set(events1_tuple) & set(events2_tuple))
        elif events1 is None:
            return events2
        elif events2 is None:
            return events1
        else:
            return None

    # sort events in ascending order (regarding the end time of the event)
    def sort_events(self, events):
        return events.sort(key=lambda x: datetime.strptime(x[2], '%Y-%m-%d %H:%M:%S'))

    def close(self):
        self.driver.close()


if __name__ == '__main__':

    # csv_to_cql()

    # # CQL queries
    # starting_room = '"Entrance"'
    # targeted_room = '"Maker Bays1"'
    # stairs = True

    # name_of_event = '"Meeting"'
    # date_of_event = '"2019-03-25"'
    # name_of_room = '"Boardroom"'
    # name_of_organizer = '"Oliver Lemon"'

    from utils import log
    LOG_NAME = "grid-neo"
    logger = log.get_logger(LOG_NAME)

    driver = GridNeoConnector(logger)

    # csv_to_cql()
    driver.csv_to_neo4j()

    # find_shortest_path(starting_room, targeted_room, stairs)
    # find_event_given_room(name_of_room)
    # find_event_given_name(name_of_event)

    # date_events = find_event_given_date(date_of_event)

    # person_events = find_event_given_person(name_of_organizer)

    # merged_events = merge_event_lists(date_events, person_events)
    # print(merged_events)
    # # print(find_event_given_person('"Oliver"'))

    driver.close()
