# ROS Bag Data Extraction and Synchronization Script

This document explains the functionality of a Python script designed to extract data from ROS (Robot Operating System) bag files, convert images, and synchronize data across multiple topics.
---

## Overview
This script processes a ROS bag file to extract images and topic data, saves them to a specified directory, and generates CSV files for the extracted data. It also synchronizes data based on a specified camera topic.

## Key Steps:
1. **Input Data**: The script takes a ROS bag file as input and creates a subdirectory for the output.
2. **Configuration**: Define topics and their data extraction details in the configuration dictionary.
3. **Directory Creation**: Ensures the output directory and subdirectories for images exist.
4. **Image Extraction**: Converts ROS image messages to OpenCV images and saves them as JPEG files.
5. **Data Extraction**: Extracts specified data fields from messages and stores them in pandas DataFrames.
6. **CSV Generation**: Creates separate CSV files for each topic and a combined CSV file with synchronized data.
7. **Output**: Prints the progress and the location of the output files.


This was a group project, my role was to create and tune this extraction tool.
