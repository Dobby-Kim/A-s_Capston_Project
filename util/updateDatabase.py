import pyodbc
from dotenv import load_dotenv
import os

load_dotenv()

SERVER = os.getenv('SERVER')
DATABASE = os.getenv('DATABASE')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

seat_states = [
    (26010101, 1),
    (26010102, 2),
    (26010103, 1),
    (26010104, 2),
    (26010105, 2),
    (26010106, 2),
    (26010107, 1),
    (26010108, 1),
    (26010109, 1),
    (26010110, 2),
    (26010111, 1),
    (26010112, 1),
    (26010113, 2),
    (26010114, 1),
    (26010115, 1),
    (26010116, 1),
    (26010117, 1),
    (26010118, 2)
    ]


def generate_seat_states_list(space_name, seat_states):
    """
    Generates a list of tuples (seatID, seatState) based on the spaceName and a list of seat states.

    Parameters:
    space_name (str): The name of the space
    seat_states (list of int): A list of seat states

    Returns:
    list of tuples: A list where each tuple contains (seatID, seatState)
    """
    
    # Mapping of space names to their spaceIDs
    space_ids = {
        'parksangjo': 260101,
        'kingolounge': 261101,
        'ebstudyroom1': 261102,
        'ebstudyroom2': 261103
    }

    # Get the spaceID for the given space name
    space_id = space_ids.get(space_name)
    if space_id is None:
        raise ValueError(f"Unknown space name: {space_name}")

    # Generate the list of (seatID, seatState) tuples
    seat_states_list = []
    for index, state in enumerate(seat_states, start=1):
        seat_id = f"{space_id}{str(index).zfill(2)}"
        seat_states_list.append((int(seat_id), state))

    return seat_states_list


def generate_update_query(space_name, unprocessed_seat_states):
    
    """
    Parameters:
    seat_states (list of tuples): A list where each tuple contains (seatID, new_seat_state)

    Returns:
    str: A SQL query string
    """
    
    seat_states = generate_seat_states_list(space_name, unprocessed_seat_states)
    
    case_statements = []
    seat_ids = []
    available_seats_count = 0

    for seat_id, state in seat_states:
        case_statements.append(f"WHEN {seat_id} THEN {state}")
        seat_ids.append(str(seat_id))
        if state == 0:  # Assuming seatState '0' indicates an available seat
            available_seats_count += 1

    case_clause = " ".join(case_statements)
    seat_ids_clause = ", ".join(seat_ids)

    query_seat_data_table = f"""
    UPDATE SeatDataTable
    SET seatState = CASE seatID
        {case_clause}
    END
    WHERE seatID IN ({seat_ids_clause});
    """

    # Query to update SpaceTable
    query_space_table = f"""
    UPDATE SpaceTable
    SET available_seat = {available_seats_count}
    WHERE name = '{space_name}';
    """

    return query_seat_data_table, query_space_table


def send_query_to_database(seat_states, spaceName):
    query_seat_data_table, query_space_table = generate_update_query(seat_states, spaceName)

    server = SERVER # 예: 'example.database.windows.net'
    database = DATABASE  # 예: 'mydatabase'
    username = USERNAME  # 예: 'username'
    password = PASSWORD  # 비밀번호

    # 데이터베이스에 연결
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server +
                        ';DATABASE=' + database +
                        ';UID=' + username +
                        ';PWD=' + password)

    cursor = cnxn.cursor()



    # 세부 좌석별 상태 변경 쿼리 실행
    cursor.execute(query_seat_data_table)

    # 커밋 (데이터 변경이 있는 경우)
    cnxn.commit()

    # 전체좌석 앉을 수 있는 개수 변경 쿼리 실행
    cursor.execute(query_space_table)

    # 커밋 (데이터 변경이 있는 경우)
    cnxn.commit()

    # 데이터 가져오기 (SELECT 쿼리의 경우)
    # rows = cursor.fetchall()
    # for row in rows:
    #     print(row)

    # 연결 종료
    cursor.close()
    cnxn.close()
