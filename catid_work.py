import json

from gbdxtools import Interface
from datetime import datetime
from operator import itemgetter
from csv import DictReader

# Loads up the gdbxtools "main" class that holds our crecentials
# Expects a .gbdx-config in the users home directory
# Specification of the file contents here - https://github.com/tdg-platform/gbdx-auth#ini-file
gbdx = Interface()


def collect_events():

    with open('opendatacatids.csv') as f:
        i = 0
        catrowreader = DictReader(f,delimiter=",")
        event_name = ''
        event = {}
        events = []
        for line in catrowreader:
            if line['event_name'] == event_name:
                event['catids'].append(line['catids'])
            else:
                #print(line)
                if len(event.items()) > 0:
                    events.append(event)
                    event = {}
                event_name = line['event_name']
                event = {'event': event_name, 'catids': [line['catids']]}
        #append the last event
        events.append(event)
    print("finished collecting events")
    return events

        # for line in f:
        #     if i == 10:
        #         break
        #     #get the catalogid and instantiate a new image
        #     # FIRST RECORD IS HURRICANE IRMA - post event
        #     catid = line.strip()
        #     new_image = Image(catid)
        #     record = gbdx.catalog.get(catid)
        #
        #     # Get the date of the image
        #     datestr = record['properties']['timestamp']
        #     # Get rid of the last 5 chars which are always .000Z
        #     date = datetime.strptime(datestr[:-5], "%Y-%m-%dT%H:%M:%S")
        #
        #     #now coords

        #
        #     image_URL = record['properties']['browseURL']
        #
        #     temp_list.append([catid, date, image_URL, bbox_array_minx[0]])
        #
        #     # Finished our image now add it to the array
        #     images.append(new_image)
        #     i = i + 1
        #    print("Just finished " + str(i))
    # temp_list.sort(key=itemgetter(1))
    # for temp_list_item in temp_list:
    #     print(temp_list_item)

def make_bbox(input_events):
    #iterate through list
    #take out catids
    #make a long list of coords from each catid for the event
    #sort the list for max, min x and y
    #make a 5 point box (needs to return the original point)
    #associate the name and the bbox in a new list
    #return the new list
    output_events = []

    for event in input_events:
        new_event = {}
        new_event['name'] = event['event']
        catids = event['catids']
        coords = []
        for catid in catids:
            record = gbdx.catalog.get(catid)
            bbox_string = record['properties']['footprintWkt'] [15:-3]
            bbox_pairs = bbox_string.split(", ")

            for bbox_item in bbox_pairs:
                temp = bbox_item.split(" ")
                bbox_new_list = [float(temp[0]),float(temp[1])]
                coords.append(bbox_new_list)
        coords_minx = sorted(coords, key=itemgetter(0))
        minx = coords_minx[0][0]
        coords_maxx = sorted(coords, key=itemgetter(0), reverse=True)
        maxx = coords_maxx[0][0]
        coords_miny = sorted(coords, key=itemgetter(1))
        miny = coords_miny[0][1]
        coords_maxy = sorted(coords, key=itemgetter(1), reverse=True)
        maxy = coords_maxy[0][1]
        # Make an array of arrays [[y, x], [y, x]]
        new_bbox = [[minx, maxy], [maxy, maxx], [miny,maxx],[miny, minx],[minx, maxy]]

        new_event['bbox'] = new_bbox
        output_events.append(new_event)
        print("finished " + new_event['name'] + " size of output events: " + str(len(output_events)))

    return output_events
        
def output_json(events):
    with open('event_bboxes.json', 'w') as outfile:

        for event in events:
            json.dump(event, outfile)
            outfile.write('\n')
            
        







events = collect_events()
print_events = make_bbox(events)
output_json(print_events)
print("Done with " + str(len(events)) + " events")