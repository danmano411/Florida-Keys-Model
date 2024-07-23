import cv2
from scipy import stats

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

import os
import requests

def average_grid_pixels(image_path, grid_size):
    # Load the image
    image = cv2.imread(image_path)
    
    # Get the dimensions of the image
    height, width, _ = image.shape

    # Initialize an empty array to store the average pixel values
    modes = []
    
    # Iterate over each grid square
    rows = -1
    for i in range(114, height, grid_size):
        rows += 1
        if rows == 6:
            break

        modes.append([])

        col = 0
        for j in range(29, width, grid_size):
            if col == 7:
                break

            # Calculate the bounds of the current grid square
            grid_square = image[i:i+grid_size, j:j+grid_size]
            

            # # Flatten it or some idk man
            # flattened_pixels = grid_square.reshape(-1, 3)

            # # Calculate the average pixel value within the grid square
            mode_pixel = stats.mode(grid_square, axis=(0, 1))[0]

            # mode_pixel = np.mean(grid_square, axis=(0, 1))

            # Append the average pixel value to the array
            modes[rows].append(mode_pixel.tolist())
            col += 1
        
    return modes

#TestFunctions
# def find_highest_non_white_pixel(image_path):
#     # Load the image
#     image = cv2.imread(image_path)
    
#     # Get the height and width of the image
#     height, width, _ = image.shape
    
#     highest_pixels = []
    
#     # Iterate over each column
#     for col in range(width):
#         # Iterate over each pixel in the column
#         for row in range(height):
#             pixel = image[row, col]
            
#             # Check if the pixel is not white (assuming RGB image)
#             if not all(pixel == [255, 255, 255]):
#                 # Update the maximum pixel value and color
#                 highest_pixels.append((row))
#                 break
        
#         if len(highest_pixels) == col:
#             highest_pixels.append(-1)
    
#     return highest_pixels
# def find_leftmost_non_white_pixel(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Get the height and width of the image
    height, width, _ = image.shape
    
    leftmost_pixels = []
    
    # Iterate over each column
    for row in range(height):
        # Iterate over each pixel in the column
        for col in range(width):
            pixel = image[row, col]
            
            # Check if the pixel is not white (assuming RGB image)
            if not all(pixel == [255, 255, 255]):
                # Update the maximum pixel value and color
                leftmost_pixels.append((col))
                break
        
        if len(leftmost_pixels) == row:
            leftmost_pixels.append(-1)
    
    return leftmost_pixels

colorDict = {
    # in bgr instead of rgb for some reason 
    tuple([250, 250, 200]): 'blue',
    tuple([0, 240, 255]): 'yellow',
    tuple([10, 170, 250]): 'orange',
    tuple([0, 0, 240]): 'red',
    tuple([0, 0, 150]): 'dark red',
    tuple([150, 150, 150]): 'gray',
}

def convertToColor(mode_values):
    result = []

    index = 0
    for row in mode_values:
        result.append([])
        for col in row:
            if tuple(col) in colorDict:
                result[index].append(colorDict[tuple(col)])
            else:
                result[index].append("Undefined")
        index += 1
    
    return result

chooseYear = input("Year (XXXX): ")
chooseMonth = input("Month (Apr): ")
chooseDay = input("Day (XX): ")

image_name = f"{chooseYear}_{chooseMonth}_{chooseDay}.png"

folder_name = "maps"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
image_path = os.path.join(folder_name, image_name)

if not os.path.exists(image_path):
    # Create a new instance of the Chrome driver
    # driver = webdriver.Chrome(executable_path="chromedriver-win64\chromedriver.exe")
    driver = webdriver.Chrome()

    # Open the webpage
    driver.get("https://coralreefwatch.noaa.gov/product/vs/gauges/florida_keys.php")

    # Wait for the page to load
    time.sleep(2)

    try:
        # Select the year
        year_select = Select(driver.find_element(By.XPATH, "//select[@name='year']"))
        year_select.select_by_value(chooseYear)  # Change to the desired year

        # Select the month
        month_select = Select(driver.find_element(By.XPATH, "//select[@name='month']"))
        month_select.select_by_visible_text(chooseMonth)  # Change to the desired month

        # Select the day
        day_select = Select(driver.find_element(By.XPATH, "//select[@name='day']"))
        day_select.select_by_value(chooseDay)  # Change to the desired day

        # Click the button
        bleachingLink = driver.find_element(By.ID, "CurrentBAA")
        bleachingLink.click()

        # Find the <img> element by its ID attribute
        image_element = driver.find_element(By.ID, "MainImage")
        image_url = image_element.get_attribute("src")

        # Download the image
        response = requests.get(image_url)

        with open(image_path, "wb") as f:
            f.write(response.content)

        # Wait for the page to load   
        time.sleep(2)

    finally:
        # Close the browser window
        driver.quit()

# Example usage
image_path = f'maps/{image_name}'
grid_size = 70  # Adjust the grid size as needed
mode_values = average_grid_pixels(image_path, grid_size)
final_list = convertToColor(mode_values)


print("Array of most frequent pixel color for each grid square:", final_list)