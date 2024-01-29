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
OpenCV is a computer vision library whose main focus is to process and manipulate this information.

Mat is basically a class with two data parts:

1. matrix header

- containing information such as the size of the matrix
- method used for storing, at which address is the matrix stored.
- matrix header size is constant

2. a pointer to the matrix containing the pixel values

- dimensionality depending on the method chosen for storing

OpenCV is an image processing library. To solve a computational challenge, most of the time you will end up using multiple functions of the library. Because of this, passing images to functions is a common practice. We should not forget that we are talking about image processing algorithms, which tend to be quite computational heavy. The last thing we want to do is further decrease the speed of your program by making unnecessary copies of potentially large images.
To tackle this issue OpenCV uses a reference counting system. he idea is that each Mat object has its own header, however a matrix may be shared between two Mat objects by having their matrix pointers point to the same address. Moreover, the copy operators will only copy the headers and the pointer to the large matrix, not the data itself.