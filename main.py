import psycopg2, threading

def query_uplink_data(cursor):
    # Query the data from the device_up table
    try:
        cursor.execute("SELECT * FROM device_up")
    except psycog2.Error as e:
        print(e.pgerror)

    # Print the data once the query is finished
    print(cursor.fetchall())
    return

def fake_uplink_data(conn, cursor, device_id):
    # Add fake data from the device_up table
    time = "0" # TODO add new time 
    device_name = "test" + device_id
    application_id = 0
    application_name = "FakeTest"
    frequency = 240000
    dr = 0
    adr = True # TODO verify this
    f_cnt = 1 # TODO increase this as we go
    f_port = 1
    # TODO add tags
    # TODO add data
    rx_info = {}
    object_b = {}
    try:
        # TODO verify this
        cursor.execute("INSERT INTO device_up", (time, device_id, device_name, application_id, application_name, frequency, dr, adr, f_cnt, f_port, tags, data, rx_info, object_b))
    except psycog2.Error as e:
        print(e.pgerror)

    # Commit the new data to the database
    conn.commit()
    return


def main():
    conn = psycopg2.connect("dbname=loraserver_as user=postgres password=password")
    cur = conn.cursor()

    # TODO maybe spin a thread that will run continuously
    query_uplink_data(cur)

    # TODO flood database with fake entries
    fake_uplink_data(conn, cur, "0000000000")

    # Close the cursor and then database
    cur.close()
    conn.close()
