from gbdxtools import Interface
from datetime import datetime
from operator import itemgetter

# REALIZED THIS WOULDN'T WORK IN TIME SO THIS IS NOT FINISHED!!

#my own little class to handle all the attributes on the images
from image import Image

# Loads up the gdbxtools "main" class that holds our crecentials
# Expects a .gbdx-config in the users home directory
# Specification of the file contents here - https://github.com/tdg-platform/gbdx-auth#ini-file
gbdx = Interface()


def run_numbers():
    #pull in catids
    #get bbox and date for each catid and associate it with the catid
    #sort on date and then x1
    #then a bunch of if statements to determine project

    # The array to hold our images
    images = []

    #DELETE ME BEFORE FINISHING
    temp_list = []
    with open('open-data-catids.txt') as f:
        i = 0
        for line in f:
            if i == 10:
                break
            #get the catalogid and instantiate a new image
            # FIRST RECORD IS HURRICANE IRMA - post event
            catid = line.strip()
            new_image = Image(catid)
            record = gbdx.catalog.get(catid)

            # Get the date of the image
            datestr = record['properties']['timestamp']
            # Get rid of the last 5 chars which are always .000Z
            date = datetime.strptime(datestr[:-5], "%Y-%m-%dT%H:%M:%S")

            #now coords
            bbox_string = record['properties']['footprintWkt'] [15:-3]
            bbox_pairs = bbox_string.split(", ")
            bbox_array = []
            for bbox_item in bbox_pairs:
                temp = bbox_item.split(" ")
                bbox_new_list = [float(temp[0]),float(temp[1])]
                bbox_array.append(bbox_new_list)
            bbox_array_minx = sorted(bbox_array, key=itemgetter(0))
            bbox_array_maxx = sorted(bbox_array, key=itemgetter(0), reverse=True)
            bbox_array_miny = sorted(bbox_array, key=itemgetter(1))
            bbox_array_maxy = sorted(bbox_array, key=itemgetter(1), reverse=True)

            image_URL = record['properties']['browseURL']

            temp_list.append([catid, date, image_URL, bbox_array_minx[0]])

            # Finished our image now add it to the array
            images.append(new_image)
            i = i + 1
            print("Just finished " + str(i))






    temp_list.sort(key=itemgetter(1))
    for temp_list_item in temp_list:
        print(temp_list_item)
    print("hello world")


run_numbers()