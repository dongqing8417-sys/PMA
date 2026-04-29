import pickle
import sqlite3
import os
from datetime import datetime


def save_progress(agent_list, current_time, step_number, cycle_number, completed_agent_index):
    db_name = 'progress.db'
    agent_list_blob = pickle.dumps(agent_list)
    current_time_str = current_time if isinstance(current_time, str) else current_time.strftime("%H:%M")

    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()

        #  id 
        cursor.execute('''CREATE TABLE IF NOT EXISTS progress (
                            id INTEGER PRIMARY KEY,
                            agent_list BLOB,
                            current_time TEXT, 
                            step_number INTEGER,
                            cycle_number INTEGER,
                            completed_agent_index INTEGER
                        )''')

        #  id = 1 
        cursor.execute('''INSERT OR REPLACE INTO progress (id, agent_list, current_time, step_number, cycle_number, completed_agent_index)
                          VALUES (1, ?, ?, ?, ?, ?)''',
                       (agent_list_blob, current_time_str, step_number, cycle_number, completed_agent_index))


def load_progress():
    db_name = 'progress.db'
    if not os.path.exists(db_name):
        raise FileNotFoundError(f" '{db_name}' ")


    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()

        # 
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='progress'")
        if not cursor.fetchone():
            raise FileNotFoundError("'progress'")

        # 
        cursor.execute(
            "SELECT agent_list, current_time, step_number, cycle_number, completed_agent_index FROM progress WHERE id = 1")
        row = cursor.fetchone()

        if not row:
            raise FileNotFoundError("")

        # 
        agent_list_blob, current_time, step_number, cycle_number, completed_agent_index = row
        agent_list = pickle.loads(agent_list_blob)

    return agent_list, current_time, step_number, cycle_number, completed_agent_index

# def save_progress(agent_list, current_time, step_number):
#     db_name = 'progress.db'
#     conn = sqlite3.connect(db_name)
#     cursor = conn.cursor()
#
#     # 
#     cursor.execute('''CREATE TABLE IF NOT EXISTS progress (
#                         agent_name TEXT,
#                         current_time TEXT,
#                         step_number INTEGER,
#                         state BLOB
#                     )''')
#
#     #  agent_list agent 
#     for agent in agent_list:
#         agent_name = str(agent.name)  #  agent  name 
#         state_blob = pickle.dumps(agent)  #  agent 
#
#         # print("type:")
#         # print(type(agent_name))
#         # print(type(current_time))
#         # print(type(step_number))
#         # print(type(state_blob))
#         if isinstance(current_time,str):
#             current_time_str = current_time
#         else:
#             current_time_str = current_time.strftime("%H:%M")
#
#         cursor.execute('REPLACE INTO progress (agent_name, current_time, step_number, state) VALUES (?, ?, ?, ?)',
#                        (agent_name, current_time_str, step_number, state_blob))
#
#     conn.commit()
#     conn.close()


# def save_progress(agent_list, current_time, step_number, cycle_number, completed_agent_index):
#     db_name = 'progress.db'
#     conn = sqlite3.connect(db_name)
#     cursor = conn.cursor()
#
#     #  `cycle_number`  `completed_agent_index`
#     cursor.execute('''CREATE TABLE IF NOT EXISTS progress (
#                         agent_list BLOB,
#                         current_time TEXT,
#                         step_number INTEGER,
#                         cycle_number INTEGER,
#                         completed_agent_index INTEGER
#                     )''')
#
#     agent_list_blob = pickle.dumps(agent_list)
#
#     if isinstance(current_time, str):
#         current_time_str = current_time
#     else:
#         current_time_str = current_time.strftime("%H:%M")
#
#     cursor.execute(
#         'REPLACE INTO progress (agent_list, current_time, step_number, cycle_number, completed_agent_index) VALUES (?, ?, ?, ?, ?)',
#         (agent_list_blob, current_time_str, step_number, cycle_number, completed_agent_index))
#
#     conn.commit()
#     conn.close()


# def load_progress():
#     db_name = 'progress.db'
#     if not os.path.exists(db_name):
#         raise FileNotFoundError(f" {db_name} ")
#
#     conn = sqlite3.connect(db_name)
#     cursor = conn.cursor()
#
#     # 
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='progress'")
#     table_exists = cursor.fetchone()
#
#     if not table_exists:
#         conn.close()
#         raise FileNotFoundError("")
#
#     # 
#     cursor.execute("SELECT agent_list, current_time, step_number, cycle_number, completed_agent_index FROM progress")
#     row = cursor.fetchone()
#     if not row:
#         conn.close()
#         raise FileNotFoundError("")
#
#     # 
#     agent_list_blob, current_time, step_number, cycle_number, completed_agent_index = row
#     agent_list = pickle.loads(agent_list_blob)
#
#     conn.close()
#
#     return agent_list, step_number, cycle_number, completed_agent_index


# def load_progress():
#     #  FileNotFoundError
#     db_name = 'progress.db'
#     if not os.path.exists(db_name):
#         print(f" {db_name} ")
#
#     conn = sqlite3.connect(db_name)
#     cursor = conn.cursor()
#
#     #  progress 
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='progress'")
#     table_exists = cursor.fetchone()
#
#     if not table_exists:
#         conn.close()
#         raise FileNotFoundError("")
#
#     #  progress 
#     cursor.execute("SELECT agent_name, current_time, step_number, state FROM progress")
#     rows = cursor.fetchall()
#     if not rows:
#         conn.close()
#         raise FileNotFoundError("")
#
#     # 
#     agent_list = []
#     current_time = None
#     step_number = None
#     for row in rows:
#         agent_name, current_time, step_number, state_blob = row
#         agent = pickle.loads(state_blob)
#         agent_list.append(agent)
#     conn.close()
#
#     return agent_list, step_number