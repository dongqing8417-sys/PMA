import sqlite3
from datetime import time
from prompt.prompt import Prompt
from LLMs.LLMs import LLMs
import logging

class Memory:
    def __init__(self, agent_name):

        self.agent_name = agent_name.replace(" ", "").lower()

        self.db_name = f'Memories_{self.agent_name}.db'
        self.db_summary_name = f'Memories_summary_{self.agent_name}.db'
        self._create_memory_table()
        self._create_memory_summary_table()

    def _create_memory_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Memories(
            id INTEGER PRIMARY KEY,
            memory_content TEXT,
            memory_type TEXT,
            memory_importance INTEGER,
            memory_feeling TEXT,
            memory_place TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def _create_memory_summary_table(self):
        conn = sqlite3.connect(self.db_summary_name)
        cursor = conn.cursor()
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS MemorySummary(
                    id INTEGER PRIMARY KEY,
                    start_time TIMESTAMP,
                    end_time TIMESTAMP,
                    memory_content TEXT,
                    reflection TEXT,
                    importance INTEGER,
                    feeling TEXT
                )
                ''')
        conn.commit()
        conn.close()


    def add_memory_summary(self, start_time, end_time, content, reflection, importance, feeling):
        conn = sqlite3.connect(self.db_summary_name)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO MemorySummary (start_time, end_time, memory_content, reflection, importance, feeling)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (start_time, end_time, content, reflection, importance, feeling))
        conn.commit()
        conn.close()



    def arrange_memory(self, agent, event):
        prompt = Prompt("memory")
        params = {
            "agent_bio": agent.bio,
            "agent_event": event
        }
        fill_prompt = prompt.to_string(params)
        memory = LLMs(agent.model, fill_prompt).ask(True)
        return memory

    # def add_memory(self, memory_content, memory_type, meomory_importance, memory_feeling, memory_place, timestamp):
    #     conn = sqlite3.connect(self.db_name)
    #     cursor = conn.cursor()
    #     cursor.execute('''
    #     INSERT INTO Memories (memory_content, memory_type, memory_importance, memory_feeling, memory_place, timestamp)
    #     VALUES (?, ?, ?, ?, ?, ?)
    #     ''', (memory_content, memory_type, meomory_importance, memory_feeling, memory_place, timestamp))
    #     conn.commit()
    #     conn.close()
    #
    # # def retrieve_memory(self, memory_type=None, limit=None, min_importance=None):  #  min_importance 
    # #     conn = sqlite3.connect(self.db_name)
    # #     cursor = conn.cursor()
    # #     query = 'SELECT id, memory_content, memory_type, memory_importance, memory_feeling, memory_place, timestamp FROM Memories'
    # #     params = []
    # #
    # #     # 
    # #     conditions = []
    # #     if memory_type:
    # #         conditions.append('memory_type = ?')
    # #         params.append(memory_type)
    # #     if min_importance is not None:
    # #         conditions.append('memory_importance >= ?')
    # #         params.append(min_importance)
    # #
    # #     if conditions:
    # #         query += ' WHERE ' + ' AND '.join(conditions)
    # #
    # #     query += ' ORDER BY timestamp DESC'
    # #     if limit:
    # #         query += ' LIMIT ?'
    # #         params.append(limit)
    # #
    # #     cursor.execute(query, params)
    # #     memories = cursor.fetchall()
    # #     conn.close()
    # #     return memories
    #
    # def retrieve_memory(self, memory_type=None, limit=None, min_importance=None, order_by_timestamp_asc=True):
    #     conn = sqlite3.connect(self.db_name)
    #     cursor = conn.cursor()
    #     query = 'SELECT id, memory_content, memory_type, memory_importance, memory_feeling, memory_place, timestamp FROM Memories'
    #     params = []
    #
    #     # 
    #     conditions = []
    #     if memory_type:
    #         conditions.append('memory_type = ?')
    #         params.append(memory_type)
    #     if min_importance is not None:
    #         conditions.append('memory_importance >= ?')
    #         params.append(min_importance)
    #
    #     if conditions:
    #         query += ' WHERE ' + ' AND '.join(conditions)
    #
    #     # 
    #     query += ' ORDER BY timestamp DESC' if not order_by_timestamp_asc else ' ORDER BY timestamp ASC'
    #     if limit:
    #         query += ' LIMIT ?'
    #         params.append(limit)
    #
    #     cursor.execute(query, params)
    #     memories = cursor.fetchall()
    #     conn.close()
    #     return memories

    def format_time(self, timestamp):
        if isinstance(timestamp, time):
            #  datetime.time  HH:MM
            return timestamp.strftime("%H:%M")
        elif isinstance(timestamp, str):
            #  HH:MM  HH:MM:SS 
            parts = timestamp.split(":")
            if len(parts) == 3:
                #  HH:MM:SS 
                return f"{parts[0]}:{parts[1]}"
            elif len(parts) == 2:
                #  HH:MM 
                return timestamp
        #  None 
        raise ValueError("Invalid time format")

    def add_memory(self, memory_content, memory_type, memory_importance, memory_feeling, timestamp):
        formatted_time = self.format_time(timestamp)
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO Memories (memory_content, memory_type, memory_importance, memory_feeling, timestamp)
        VALUES (?, ?, ?, ?, ?)
        ''', (memory_content, memory_type, memory_importance, memory_feeling, formatted_time))
        conn.commit()
        conn.close()

    def retrieve_memory(self, memory_type=None, limit=None, min_importance=None, order_by_timestamp_asc=True,
                        specific_time=None):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        query = 'SELECT id, memory_content, memory_type, memory_importance, memory_feeling, memory_place, timestamp FROM Memories'
        params = []

        # 
        conditions = []
        if memory_type:
            conditions.append('memory_type = ?')
            params.append(memory_type)
        if min_importance is not None:
            conditions.append('memory_importance >= ?')
            params.append(min_importance)

        #  specific_time 
        if specific_time:
            conditions.append("strftime('%H:%M', timestamp) = ?")
            params.append(specific_time)

        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)

        #  id 
        query += ' ORDER BY id ASC' if order_by_timestamp_asc else ' ORDER BY id DESC'

        if limit:
            query += ' LIMIT ?'
            params.append(limit)

        cursor.execute(query, params)
        memories = cursor.fetchall()
        conn.close()
        return memories


    def retrieve_important_memories(self, min_importance=3):
        # 3
        return self.retrieve_memory(min_importance=min_importance)

    def get_last_memory_content(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
        SELECT memory_content FROM Memories ORDER BY timestamp DESC LIMIT 1
        ''')
        last_memory = cursor.fetchone()
        conn.close()
        if last_memory:
            return last_memory[0]
        return None

    def print_all_memories(self):
        # 
        memories = self.retrieve_memory()

        if not memories:
            logging.info("No memories found.")
            print("No memories found.")
            return

        # 
        for memory in memories:
            logging.info(f"memory: {memory}")
            print("memory:", memory)
            logging.info(f"ID: {memory[0]}")
            print(f"ID: {memory[0]}")
            logging.info(f"Content: {memory[1]}")
            print(f"Content: {memory[1]}")
            logging.info(f"Type: {memory[2]}")
            print(f"Type: {memory[2]}")
            logging.info(f"Importance: {memory[3]}")
            print(f"Importance: {memory[3]}")
            logging.info(f"Feeling: {memory[4]}")
            print(f"Feeling: {memory[4]}")
            logging.info(f"Place: {memory[5]}")
            print(f"Place: {memory[5]}")
            logging.info(f"Timestamp: {memory[6]}")
            print(f"Timestamp: {memory[6]}")
            logging.info("-" * 40)
            print("-" * 40)

    def format_memory_for_agent(self, memory):
        # 
        memory_string = (
            f"On {memory[6]}, at {memory[5]}, the agent experienced {memory[1]} "
            f"which was categorized as a {memory[2]} memory with an importance of {memory[3]}. "
            f"The agent felt {memory[4]} about it."
        )
        return memory_string

    def format_memories_for_agent(self, memories):
        # 
        formatted_memories = [self.format_memory_for_agent(memory) for memory in memories]
        return formatted_memories

    def format_simple_memory_for_agent(self, memory):
        if memory[1] == 'sleep' or memory[0] == 'sleep':
            return None
        if len(memory)==6:
            memory_string = f"At {memory[5]}, I {memory[0]}."
        elif len(memory)==7:
            memory_string = f"At {memory[6]}, I {memory[1]}."
        else:
            logging.info(f"Memory causing error: {memory}")
            print(f"Memory causing error: {memory}")
            raise  # 

        return memory_string


    def format_simple_memories_for_agent(self, memories):
        # 
        formatted_memories = [self.format_simple_memory_for_agent(memory) for memory in memories if memory]
        return formatted_memories

    def retrieve_memory_summary(self):
        conn = sqlite3.connect(self.db_summary_name)
        cursor = conn.cursor()
        cursor.execute('SELECT start_time, end_time, memory_content, reflection, importance, feeling FROM MemorySummary')
        memories = cursor.fetchall()
        conn.close()
        return memories

    def format_simple_memories_summary(self):
        """
         memory_summary 
        """
        memories = self.retrieve_memory_summary()
        formatted_memories = []

        for memory in memories:
            start_time, end_time, content, reflection, importance, feeling = memory
            formatted_memory = f"From {start_time} to {end_time}, I {content}."
            formatted_memories.append(formatted_memory)
        return formatted_memories

    def get_memories_for_agent(self, memory_type=None, limit=None):
        # 
        memories = self.retrieve_memory(memory_type, limit)

        # 
        formatted_memories = [self.format_memory_for_agent(memory) for memory in memories]

        return formatted_memories  # 

    def delete_memory(self, memory_id=None, time_point=None):
        if memory_id is None and time_point is None:
            raise ValueError(" memory_id  time_point ")

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        if memory_id is not None:
            cursor.execute('''
            DELETE FROM Memories WHERE id = ?
            ''', (memory_id,))
        elif time_point is not None:
            if isinstance(time_point, str):
                current_time_str = time_point
            else:
                current_time_str = time_point.strftime("%H:%M")

            cursor.execute('''
            DELETE FROM Memories WHERE timestamp < ?
            ''', (current_time_str,))

        conn.commit()
        conn.close()

    def print_memory_summary(self):
        """
         Memory_Summary 
        """
        memories = self.retrieve_memory_summary()

        if not memories:
            logging.info("No summaries found in Memory_Summary table.")
            print("No summaries found in Memory_Summary table.")
            return

        for memory in memories:
            logging.info("Summary Record:")
            print("Summary Record:")
            logging.info(f"Start Time: {memory[0]}")
            print(f"Start Time: {memory[0]}")
            logging.info(f"End Time: {memory[1]}")
            print(f"End Time: {memory[1]}")
            logging.info(f"Content: {memory[2]}")
            print(f"Content: {memory[2]}")
            logging.info(f"Reflection: {memory[3]}")
            print(f"Reflection: {memory[3]}")
            logging.info(f"Importance: {memory[4]}")
            print(f"Importance: {memory[4]}")
            logging.info(f"Feeling: {memory[5]}")
            print(f"Feeling: {memory[5]}")
            logging.info("-" * 40)
            print("-" * 40)