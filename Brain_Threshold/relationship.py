import sqlite3
import os
import logging


class Relationship:
    def __init__(self, agent_name):
        self.agent_name = agent_name.replace(" ", "").lower()
        self.db_name = f'Relationship_{self.agent_name}.db'

        self._create_relationship_table()
        self._create_interactions_table()

    def _create_relationship_table(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Relationships(
                id INTEGER PRIMARY KEY,
                name TEXT,
                relationship_type TEXT,
                intimacy_level INTEGER,
                impression TEXT,
                date DATE DEFAULT (DATE('now')),  --  date 
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def _create_interactions_table(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Interactions(
                id INTEGER PRIMARY KEY,
                relationship_id INTEGER,
                agent_name TEXT,
                other_agent_name TEXT,
                interaction_content TEXT,
                interaction_type TEXT,
                date DATE DEFAULT (DATE('now')),  --  date 
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (relationship_id) REFERENCES Relationships(id)
                )
            ''')
            conn.commit()

    # 
    def _get_connection(self):
        return sqlite3.connect(self.db_name)

    def add_relationship(self, name, relationship_type, intimacy_level, impression, date, time):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO Relationships (name, relationship_type, intimacy_level, impression, date, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, relationship_type, intimacy_level, impression, date, time))
            conn.commit()

    def add_interaction(self, relationship_id, agent_name, other_agent_name, interaction_content, interaction_type, date, time):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO Interactions (relationship_id, agent_name, other_agent_name, interaction_content, interaction_type, date, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
            relationship_id, agent_name, other_agent_name, interaction_content, interaction_type, date, time))
            conn.commit()

    def retrieve_relationships(self, relationship_type=None, name=None, limit=None):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            query = 'SELECT id, name, relationship_type, intimacy_level, impression, date, timestamp FROM Relationships'
            params = []
            conditions = []

            if relationship_type:
                conditions.append('relationship_type = ?')
                params.append(relationship_type)

            if name:
                conditions.append('name = ?')
                params.append(name)

            if conditions:
                query += ' WHERE ' + ' AND '.join(conditions)

            query += ' ORDER BY timestamp DESC'

            if limit:
                query += ' LIMIT ?'
                params.append(limit)

            cursor.execute(query, params)
            relationships = cursor.fetchall()

            # 
            if not relationships:
                return None

            return relationships

    def retrieve_interactions(self, relationship_id=None, agent_name=None, other_agent_name=None, interaction_type=None,
                              limit=None):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            query = 'SELECT id, relationship_id, agent_name, other_agent_name, interaction_content, interaction_type, date, timestamp FROM Interactions'
            params = []
            conditions = []

            #  relationship_id 
            if relationship_id:
                conditions.append('relationship_id = ?')
                params.append(relationship_id)

            #  agent_name 
            if agent_name:
                conditions.append('agent_name = ?')
                params.append(agent_name)

            #  other_agent_name 
            if other_agent_name:
                conditions.append('other_agent_name = ?')
                params.append(other_agent_name)

            #  interaction_type 
            if interaction_type:
                conditions.append('interaction_type = ?')
                params.append(interaction_type)

            #  WHERE 
            if conditions:
                query += ' WHERE ' + ' AND '.join(conditions)

            #  ORDER BY 
            query += ' ORDER BY timestamp DESC'

            #  limit 
            if limit:
                query += ' LIMIT ?'
                params.append(limit)

            # 
            cursor.execute(query, params)
            return cursor.fetchall()

    def format_relationship(self, relationship, agent1, agent2):
        if relationship[0][4]=="":
            r = NewRelationship()
            impression = r.get_initial_impression(agent1,agent2)

            relationship_list = list(relationship[0])
            relationship_list[4] = impression
            relationship[0] = tuple(relationship_list)

        logging.info(f"relationship: {relationship}")
        print("relationship:", relationship)
        return (
            f"Relationship with {relationship[0][1]}: We are {relationship[0][2]} with an intimacy level of {relationship[0][3]}. "
            f"The impression of him/her is: {relationship[0][4]}."
        )

    def update_relationship(self, relationship_name, time, intimacy_level=None, impression=None):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            timestamp = str(time)
            if intimacy_level is not None:
                cursor.execute('''
                UPDATE Relationships
                SET intimacy_level = ?, timestamp = ?
                WHERE name = ?
                ''', (intimacy_level, timestamp, relationship_name))

            if impression is not None:
                cursor.execute('''
                UPDATE Relationships
                SET impression = ?, timestamp = ?
                WHERE name = ?
                ''', (impression, timestamp, relationship_name))

            conn.commit()

    def delete_relationship(self, relationship_name):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            DELETE FROM Relationships WHERE name = ?
            ''', (relationship_name,))
            conn.commit()

    def format_relationships(self):
        relationships = self.retrieve_relationships()
        if not relationships:
            return "The agent has no recorded relationships."

        formatted_relationships = [
            f"Relationship with {rel[1]}: They are a {rel[2]} with an intimacy level of {rel[3]}. "
            f"The agent's impression of them is: {rel[4]}."
            for rel in relationships
        ]

        return "\n".join(formatted_relationships)

    def print_all_relationships(self):
        relationships = self.retrieve_relationships()
        if not relationships:
            logging.info("No relationships found.")
            print("No relationships found.")
            return

        logging.info("All relationships:")
        print("All relationships:")
        for rel in relationships:
            logging.info(f"ID: {rel[0]}")
            print(f"ID: {rel[0]}")
            logging.info(f"Name: {rel[1]}")
            print(f"Name: {rel[1]}")
            logging.info(f"Relationship Type: {rel[2]}")
            print(f"Relationship Type: {rel[2]}")
            logging.info(f"Intimacy Level: {rel[3]}")
            print(f"Intimacy Level: {rel[3]}")
            logging.info(f"Impression: {rel[4]}")
            print(f"Impression: {rel[4]}")
            logging.info(f"Date: {rel[5]}")
            print(f"Date: {rel[5]}")
            logging.info(f"Timestamp: {rel[6]}")
            print(f"Timestamp: {rel[6]}")
            logging.info("-" * 40)
            print("-" * 40)

    def check_relationship_exists_by_name(self, name):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT 1 FROM Relationships WHERE name = ? LIMIT 1
            ''', (name,))
            return cursor.fetchone() is not None

    def print_all_interactions(self):
        interactions = self.retrieve_interactions()  # 
        if not interactions:
            logging.info("No interactions found.")
            print("No interactions found.")
            return

        logging.info("All interactions:")
        print("All interactions:")
        for interaction in interactions:
            logging.info(f"ID: {interaction[0]}")
            print(f"ID: {interaction[0]}")
            logging.info(f"Relationship ID: {interaction[1]}")
            print(f"Relationship ID: {interaction[1]}")
            logging.info(f"Agent Name: {interaction[2]}")
            print(f"Agent Name: {interaction[2]}")
            logging.info(f"Other Agent Name: {interaction[3]}")
            print(f"Other Agent Name: {interaction[3]}")
            logging.info(f"Interaction Content: {interaction[4]}")
            print(f"Interaction Content: {interaction[4]}")
            logging.info(f"Interaction Type: {interaction[5]}")
            print(f"Interaction Type: {interaction[5]}")
            logging.info(f"Date: {interaction[6]}")
            print(f"Date: {interaction[6]}")
            logging.info(f"Timestamp: {interaction[7]}")
            print(f"Timestamp: {interaction[7]}")
            logging.info("-" * 40)
            print("-" * 40)

    def delete_interactions_by_time(self, time_point):
        """
         timestamp  interaction 

        
        time_point (str):  'YYYY-MM-DD HH:MM:SS'
        """
        if isinstance(time_point,str):
            current_time_str = time_point
        else:
            current_time_str = time_point.strftime("%H:%M")

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            DELETE FROM Interactions
            WHERE timestamp < ?
            ''', (current_time_str,))
            conn.commit()


class NewRelationship:
    def __init__(self):
        # 
        self.relationships = {
            'Zhao Chun': {
                'Zhao Qi': 'My younger brother; we often share meals and conversations.',
                'Qian Xia': 'She runs the caf; friendly but her new ideas are sometimes too modern for me.',
                'Sun Qiu': 'She is a regular customer; she often buys ingredients from my shop.',
                'Li Dong': 'A reliable doctor; we occasionally discuss health and community matters.',
                'Zhou Qin': 'She manages the park; always energetic when we cross paths during my walks.'
            },
            'Qian Xia': {
                'Zhou Qin': 'My cousin and close friend; we often share ideas and support each other.',
                'Zhao Chun': 'A reliable shop owner; we occasionally discuss business matters.',
                'Sun Qiu': 'She runs the restaurant; I respect her work but sense some tension between us.',
                'Li Dong': "He criticizes my caf for not aligning with his strict health views; it's affecting my business.",
                'Zhao Qi': 'He always declines my event invitations; seems distant but I hope he joins us someday.',
                'Wang Hua': 'A newcomer; she visited my caf once. She seems quiet and thoughtful.'
            },
            'Sun Qiu': {
                'Li Dong': 'My husband; he supports me both personally and professionally.',
                'Qian Xia': 'She runs the caf that attracts some of my customers; I am cautious about her modern approaches.',
                'Zhao Chun': 'A reliable shop owner; I often purchase ingredients from his store.',
                'Zhou Qin': 'She manages the park; we have met a few times during community events.',
                'Zhao Qi': 'I dont know much about him; he is the librarian.'
            },
            'Li Dong': {
                'Sun Qiu': 'My wife; she works very hard in her business, and I always support her.',
                'Qian Xia': 'She promotes unhealthy habits at her caf; we disagreed over community health practices.',
                'Zhou Qin': 'She manages the park where I run; we often talk about health and the environment.',
                'Zhao Qi': 'We dont interact much; I know he is the librarian.',
                'Zheng Shu': 'A new resident; he visited the clinic recently, seems a bit anxious.',
                'Zhao Chun': 'A reliable shop owner; we occasionally discuss health and community matters.'
            },
            'Zhou Qin': {
                'Qian Xia': 'My cousin and best friend; we often plan events together and share ideas.',
                'Zhao Qi': 'The librarian; a thoughtful person. We often discuss literature and philosophy in the park.',
                'Li Dong': 'The town doctor; he enjoys running in the park. We often talk about health and community events.',
                'Zhao Chun': 'The shop owner; we occasionally meet in the park and exchange greetings.',
                'Sun Qiu': 'The restaurant owner; we have interacted during community events.',
                'Wang Hua': 'A newcomer; she often walks in the park. We have started talking about life and career plans.'
            },
            'Zhao Qi': {
                'Zhao Chun': 'My older brother; despite our different personalities, we support each other and often share meals and discuss life.',
                'Zhou Qin': 'The park administrator; we often discuss literature and philosophy. She is one of the few who understand my thoughts.',
                'Qian Xia': 'She often invites me to her caf events; I find them too crowded and prefer to stay away.',
                'Li Dong': 'The town doctor; we have little interaction and just know of each other.',
                'Sun Qiu': 'The restaurant owner; I dont know much about her, just that she runs the restaurant in town.',
                'Wang Hua': 'A newcomer; she has a strong interest in literature. We recently started discussing books in the park.',
                'Zheng Shu': 'A new resident; he visited the library to borrow books. He seems interested in science fiction.'
            },
            'Zheng Shu': {
                'Zhao Qi': 'Met at the library; he recommended some science fiction books.',
                'Li Dong': 'I visited his clinic recently; he seems reliable but I was a bit anxious.',
                'Wang Hua': 'A fellow newcomer; we often share our experiences adapting to the town.'
            },
            'Wang Hua': {
                'Zhao Qi': 'The town librarian; we met in the park and started discussing literature and books.',
                'Zhou Qin': 'The park administrator; she is friendly and helped me adapt to town life.',
                'Zheng Shu': 'Another newcomer; we met near my house and often share our feelings about adapting to the new environment.',
                'Qian Xia': 'The caf owner; I visit her caf once. She is always busy but friendly.'
            }
        }

    def get_initial_impression(self, person1, person2):
        """ person1  person2  'No initial impression available.'"""
        return self.relationships.get(person1, {}).get(person2, "Don't know him/her.")
# # # LiHua
# zhangsan_relationships = Relationship("zhangsan")
# r = zhangsan_relationships.retrieve_relationships(name ="Li Hua")
# logging.info(zhangsan_relationships.format_relationship(r))
# zhangsan_relationships.update_relationship(relationship_name="Li Hua", impression="She is very beautiful and interesting. She is a coffee shop employee and we have a good relationship")
# r = zhangsan_relationships.retrieve_relationships(name ="Li Hua")
# logging.info(zhangsan_relationships.format_relationship(r))
#
#
# lihua_relationships = Relationship("lihua")
# # 
# r = lihua_relationships.retrieve_relationships(name="Zhang San")
# logging.info("Before update:", lihua_relationships.format_relationship(r))
# #  impression 
# lihua_relationships.update_relationship(
#     relationship_name="Zhang San",
#     impression="She is very intelligent and dedicated to her research. I enjoy chatting with her"
# )
# # 
# r = lihua_relationships.retrieve_relationships(name="Zhang San")
# logging.info("After update:", lihua_relationships.format_relationship(r))
#
