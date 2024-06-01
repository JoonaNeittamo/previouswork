# Neural Style Transfer with TensorFlow

This repository contains a script that performs neural style transfer using TensorFlow and TensorFlow Hub. The process involves applying the artistic style of one image to the content of another, creating a new image that blends the content and style.

---

## Overview

Neural style transfer is a technique that takes two images— a content image and a style image— and blends them together so that the output image looks like the content image painted in the style of the style image. This is achieved by using a pre-trained convolutional neural network to extract features from the images and then optimizing a new image to match the content and style features.

## Features

- **Image Loading and Processing**: Utilizes TensorFlow utilities to load images from URLs and preprocess them for style transfer.
- **Pre-trained Models**: Uses the VGG19 model from `tf.keras.applications` for feature extraction and a pre-trained style transfer model from TensorFlow Hub.
- **Optimization**: Applies the Adam optimizer to iteratively update the generated image, minimizing the combined style and content loss.
- **Visualization**: Employs Matplotlib for displaying images during the process.
- **Google Colab Integration**: Includes functionality to save the final images to Google Drive when running in Google Colab.

## Workflow

1. **Setup**: Import necessary libraries and configure the environment.
2. **Image Loading**: Download content and style images from given URLs and preprocess them.
3. **Model Loading**: Load the pre-trained style transfer model from TensorFlow Hub.
4. **Feature Extraction**: Use the VGG19 model to extract style and content features from the images.
5. **Loss Calculation**: Define style and content loss functions to measure the differences between the generated image and target images.
6. **Optimization**: Use the Adam optimizer to minimize the loss and update the generated image.
7. **Training Loop**: Run the optimization in a loop, periodically displaying and saving the generated images.

## Integration

- **Google Drive**: The script includes commands to mount Google Drive and save the final stylized images directly to your Drive when running in a Google Colab environment.

## Example Output

Here are some example outputs of the neural style transfer process:

![Example Output](https://github.com/JoonaNeittamo/previouswork/blob/main/style_transfer/finalized_5_1000.jpeg)
![Example Output](https://github.com/JoonaNeittamo/previouswork/blob/main/style_transfer/finalized_2_600.jpeg)


## Acknowledgements

- [TensorFlow](https://www.tensorflow.org/)
- [TensorFlow Hub](https://tfhub.dev/)
- [Google Colab](https://colab.research.google.com/)
- Pre-trained VGG19 model from `tf.keras.applications`
