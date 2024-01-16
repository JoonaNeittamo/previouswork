# House Price Prediction App

A brief introduction and overview of your house price prediction app.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Dataset](#dataset)
- [Model](#model)
- [Contributing](#contributing)
- [License](#license)

## Features

App uses Python. Imports that are mainly used are TKinter, Pandas and RandomForestRegressor.

## Installation

```pip install -r requirements.txt ```

After the installing is done run the APP_start.exe

## Usage

There are 5 stages and those are:

- Start: Start the app.
- Import: Import your column.
- Column: Choose the columns you want to predict with. Model only works with 'price' as target and you need to add 'zip_code' to the columns.
- Input: Input your information for chosen columns. Do not use letters and each column will have their own input box.
- Prediction: Choose to train a new model or a use an existing one. Models imported work only if dumped with JOBLIB.

## Dataset

Dataset 'house_zipcode_usa.csv' is provided within the project. This dataset is used to select your columns and to train a new model.

## Model

Models accepted are those dumped from JOBLIB. Model is trained and will reach over 95% accuracy in predicting, NOTE: Accuracy is only shown if a new model is trained (training with take a long time, approx. 20 minutes)

## Contributing

Neittamo Joona in building

Zhang Weihan in planning

## License

[General Public License](https://www.gnu.org/licenses/gpl-3.0.en.html)https://www.gnu.org/licenses/gpl-3.0.en.html
