import psycopg2, datetime

def query_uplink_data(cursor):
    # Query the data from the device_up table
    try:
        cursor.execute("SELECT * FROM device_up")
    except psycog2.Error as e:
        print(e.pgerror)

    # Print the data once the query is finished
    print(cursor.fetchone())
    return

def fake_uplink_data(conn, cursor, device_id):
    id = "e671fc03-43f3-49fa-9e7d-8479c8ef2e21"
    # Add fake data from the device_up table
    time = datetime.datetime(2020, 3, 1, 17, 18, 00, 00000, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=360, name=None)) # TODO update as we go
    device_name = "test" + device_id
    application_id = 1
    application_name = "SethTest-Arduino" # current application name from LoRa
    frequency = 90430000 # Random frequency in US Band
    dr = 0  # It's the same as the normal nodes
    adr = True # We do this with our normal nodes
    f_cnt = 1 # TODO increase this as we go
    f_port = 1
    tags = ""
    # TODO add data as bytes
    data = ""
    # TODO add rx_info and object as json
    rx_info = {}
    object_b = {}
    try:
        # TODO verify this
        sql = """INSERT INTO device_up(id, received_at, dev_eui, device_name, application_id, application_name, frequency, dr, adr, f_cnt, f_port, tags, data, rx_info, object) 
                                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )"""
        #sql = """INSERT INTO device_up(id, received_at, device_id, device_name, application_id, application_name, frequency, dr, adr, f_cnt, f_port, tags, data, rx_info, object) 
        #                        VALUES(%s, %d, %s, %d, %s, %d, %d, %d, %d, %d, )"""
        cursor.execute(sql, (id, time, device_id, device_name, application_id, application_name, frequency, dr, adr, f_cnt, f_port, tags, data, rx_info, object_b))
    except psycopg2.Error as e:
        print(e.pgerror)

    # Commit the new data to the database
    conn.commit()
    return


def main():
    conn = psycopg2.connect(host="localhost", port=5432, database="loraserver_as", user="postgres", password="postgres")
    cur = conn.cursor()

    # TODO maybe spin a thread that will run continuously
    query_uplink_data(cur)

    # TODO flood database with fake entries
    fake_uplink_data(conn, cur, "8898787874924710")
    #fake_uplink_data(conn, cur, "\x8898787874924710")
    #fake_uplink_data(conn, cur, "\x8898787874924710")

    # Close the cursor and then database
    cur.close()
    conn.close()

if __name__ == '__main__':
    main()
