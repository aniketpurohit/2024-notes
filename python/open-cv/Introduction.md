# Getting Started wit Images

## cv::imread

- function loads the image using the file path specified by the first argument
- second argument is optional and specifies the format in which we want the image
  - IMREAD_COLOR - loads the image in BGR 8-bit format (default)
  - IMREAD_UNCHANGED loads the image as is (including the alpha channel if present)
  - IMREAD_GRAYSCALE loads the image as an intensity one

After reading in the image data will be stored in a `cv::Mat` object

## cv::imshow

- image is shown using a call to the cv::imshow function.
- The first argument is the title of the window
- the second argument is the cv::Mat object that will be shown

## cv::waitforkey

- for displaying our window  until the user presses a key (otherwise the program would end far too quickly)
- only parameter is just how long should it wait for a user input (measured in milliseconds). Zero means to wait forever.
- return value is the key that was pressed.

## cv::imwrite

- function to create or write a new image
- argument file_path

## MAT - the basic Image Container

when transforming this to our digital devices what we record are numerical values for each of the points of the image.
