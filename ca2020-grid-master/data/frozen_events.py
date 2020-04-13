import datetime


# Frozen events with date '2020-02-25' which will be changed to today's date
FROZEN_EVENTS_OLD_DATE = [
    ['Craig Landt RDT Meeting', 'meeting_room_g_1', '', '2020-02-25 11:00:00+00:00', '2020-02-25 12:30:00+00:00'],
    ['Masters Group Project', 'meeting_room_g_3', '', '2020-02-25 12:00:00+00:00', '2020-02-25 13:00:00+00:00'],
    ['SDME Structural', 'meeting_room_g_3', '', '2020-02-25 14:00:00+00:00', '2020-02-25 15:00:00+00:00'],
    ['SDME structural', 'meeting_room_g_3', '', '2020-02-25 16:00:00+00:00', '2020-02-25 17:00:00+00:00'],
    ['SDME Structural', 'meeting_room_g_3', '', '2020-02-25 15:00:00+00:00', '2020-02-25 16:00:00+00:00'],
    ['PDP Meeting', 'meeting_room_g_4', '', '2020-02-25 12:15:00+00:00', '2020-02-25 13:15:00+00:00'],
    ['Masters Group', 'meeting_room_g_4', '', '2020-02-25 11:00:00+00:00', '2020-02-25 12:00:00+00:00'],
    ['Group meeting', 'meeting_room_g_4', '', '2020-02-25 15:30:00+00:00', '2020-02-25 16:30:00+00:00'],
    ['Group 11 - PDB', 'meeting_room_g_4', '', '2020-02-25 14:15:00+00:00', '2020-02-25 15:15:00+00:00'],
    ['SPAICE Project workshop', 'meeting_room_g_5', '', '2020-02-25 08:00:00+00:00', '2020-02-25 20:00:00+00:00'],
    ['MEng Design', 'meeting_room_g_6', '', '2020-02-25 14:00:00+00:00', '2020-02-25 15:00:00+00:00'],
    ['green log.', 'meeting_room_g_6', '', '2020-02-25 11:15:00+00:00', '2020-02-25 12:15:00+00:00'],
    ['DBMS Group', 'meeting_room_g_6', '', '2020-02-25 15:00:00+00:00', '2020-02-25 16:00:00+00:00'],
    ['Electromagnetism Project', 'meeting_room_g_7', '', '2020-02-25 11:30:00+00:00', '2020-02-25 12:15:00+00:00'],
    ['One to One', 'meeting_room_g_7', '', '2020-02-25 10:00:00+00:00', '2020-02-25 11:15:00+00:00'],
    ['Project meeting', 'meeting_room_g_7', '', '2020-02-25 15:15:00+00:00', '2020-02-25 16:15:00+00:00'],
    ['B39VS-S2', 'meeting_room_g_7', 'System Project', '2020-02-25 13:15:00+00:00', '2020-02-25 15:15:00+00:00'],
    ['B57AT-S2', 'maker_bay_1', 'Mechanical Engineering in Context 2', '2020-02-25 14:15:00+00:00', '2020-02-25 20:15:00+00:00'],
    ['F18GW-S2', 'inspire_and_collaborate_2', 'Mathematics Workshop', '2020-02-25 09:15:00+00:00', '2020-02-25 10:15:00+00:00'],
    ['F18GW-S2', 'inspire_and_collaborate_2', 'Mathematics Workshop', '2020-02-25 10:15:00+00:00', '2020-02-25 11:15:00+00:00'],
    ['B38VR-S2', 'flex_lab_2', 'Group Robotics Project', '2020-02-25 11:15:00+00:00', '2020-02-25 12:15:00+00:00'],
    ['B37VB-S2', 'flex_lab_2', 'Praxis Programming', '2020-02-25 15:15:00+00:00', '2020-02-25 18:15:00+00:00'],
    ['B31DE-S2', 'flex_lab_2', 'Advanced Digital Electronics', '2020-02-25 10:15:00+00:00', '2020-02-25 11:15:00+00:00'],
    ['B30SQ-S2', 'flex_lab_1', 'Communication Devices and Systems', '2020-02-25 11:15:00+00:00', '2020-02-25 14:15:00+00:00'],
    ['B37VR-S2', 'flex_lab_1', 'Robotics group project', '2020-02-25 15:15:00+00:00', '2020-02-25 17:15:00+00:00'],
    ['B38VR-S2', 'creative_studio', 'Group Robotics Project', '2020-02-25 10:15:00+00:00', '2020-02-25 11:15:00+00:00'],
    ['F27SB-S2', 'digital_lab', 'Software Development 2', '2020-02-25 11:15:00+00:00', '2020-02-25 13:15:00+00:00'],
    ['B59DF-S2', 'digital_lab', 'Design and Manufacture 4', '2020-02-25 09:15:00+00:00', '2020-02-25 11:15:00+00:00'],
    ['F28DM-S2', 'digital_lab', 'Database Management Systems', '2020-02-25 14:15:00+00:00', '2020-02-25 15:15:00+00:00']
]


def change_date(frozen_events_old_date):
    '''Changes the date to today
    '''
    frozen_events_changed = []
    for event in frozen_events_old_date:
        event[3] = str(datetime.datetime.now().date()) + ' ' + event[3].split()[1]
        event[4] = str(datetime.datetime.now().date()) + ' ' + event[4].split()[1]
        frozen_events_changed.append(event)
    return frozen_events_changed


def get_frozen_events():
    '''Returns a list of frozen events
    '''
    return change_date(FROZEN_EVENTS_OLD_DATE)


# Frozen events with the current date
FROZEN_EVENTS = get_frozen_events()
