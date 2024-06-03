import sys
import os
import rosbag
import pandas as pd
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
import cv2
import functools

SAMPLE_ONLY = False  # process only 100 first msgs?

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

if len(sys.argv) == 1:
    print("\n Usage: bag_extract <bag-file-path>\n\n Creates a subdir in current directory for results.\n")
    exit()

bagfilename = sys.argv[1]
output_dir = bagfilename.replace('.bag', '_extract')

bridge = CvBridge()

bag = rosbag.Bag(bagfilename)
types, topics = bag.get_type_and_topic_info()

print("")
print(bagfilename)
print("Bag Message Count: " + str(bag.get_message_count()))
print("Bag Topics: " + ", ".join(topics.keys()))
print("Extracting images and csv to: " + output_dir)

# SYNCc_TOPIC : (camera) topic for index base. rows not matching the index will be dropped.
# for multiple cameras, we could do some extra syncing with
# wiki.ros.org > Message filters#Time Synchronizer <http://wiki.ros.org/message_filters#Time_Synchronizer>
# if needed
SYNC_TOPIC = '/camera_crop/image_rect_color/compressed'

# config to define topics and their data extraction
config = {
    '/speed': {
        'values': ['cog', 'sog'],  # 'normal' msg values to be extracted
        'prefix': 'speed_',  # prefix csv columns to prevent naming conflicts
    }
}
for x in ['', '2', '3', '4']:  # add cameras to conf, eg ['', 2,3,4] , assuming suffixed topicnames
    config[f'/camera_crop{x}/image_rect_color/compressed'] = {
        'values': [],
        'type': 'image',
        'prefix': f'camera{x}_'
    }

for key, conf in config.items():
    if conf.get('type') == 'image':
        ensure_dir(os.path.join(output_dir, conf['prefix'] + 'images'))

msgs = bag.read_messages(config.keys())
dfs = {topic: pd.DataFrame(columns=['timestamp', 'datetime'] + conf['values']) for topic, conf in config.items()}

# http://wiki.ros.org/cv_bridge/Tutorials/ConvertingBetweenROSImagesAndOpenCVImagesPython
def write_image(filepath, msg):
    result = {}
    try:
        if hasattr(msg, 'format') and 'compressed' in msg.format:
            buf = np.ndarray(shape=(1, len(msg.data)), dtype=np.uint8, buffer=msg.data)
            cv_img = cv2.imdecode(buf, cv2.IMREAD_ANYCOLOR)
            result['height'] = cv_img.shape[0]
            result['width'] = cv_img.shape[1]
            cv2.imwrite(filepath, cv_img)
        else:
            cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
            cv2.imwrite(filepath, cv_img)
    except CvBridgeError as e:
        print(f"Error converting image: {e}")
    return result

i = 0
# iterate through all bag msgs
for topic, msg, _timestamp in msgs:
    rowDict = {}
    timestamp = msg.header.stamp.to_nsec()  
    rowDict['timestamp'] = timestamp
    rowDict['datetime'] = pd.to_datetime(timestamp)

    if config[topic].get('type') == 'image':
        filename = topic.replace("/", "_") + f'_{msg.header.seq:09d}.jpg'
        filepath_relative = os.path.join(config[topic]['prefix'] + 'images', filename)
        filepath = os.path.join(output_dir, filepath_relative)

        image_info = write_image(filepath, msg)
        image_info['filename'] = filename
        image_info['filepath'] = filepath_relative
        rowDict.update(image_info)

    for col in config[topic]['values']:
        rowDict[col] = getattr(msg, col)

    dfs[topic] = dfs[topic].append(rowDict, ignore_index=True)
    i += 1
    if i % 10 == 0:  # progress indicator..
        sys.stdout.write('.')
        sys.stdout.flush()

    if SAMPLE_ONLY and i > 100:
        break

# create separate csv:s for each topic
for topic, df in dfs.items():
    df.set_index('datetime', inplace=True)
    filename = topic.replace("/", "_") + '.csv'
    filepath = os.path.join(output_dir, filename)
    df.to_csv(filepath, header=True)

df_all = functools.reduce(lambda left, right: pd.merge(
    left, right, how='outer', left_index=True, right_index=True), dfs.values())
df_all.interpolate(method='time', inplace=True)

df_all_filtered = df_all.loc[dfs[SYNC_TOPIC].index]
df_all_filtered.dropna(inplace=True)

filepath = os.path.join(output_dir, 'topics_combined.csv')
df_all_filtered.to_csv(filepath, header=True, index=False)

print("Done!")
