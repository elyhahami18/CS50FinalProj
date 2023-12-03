# CS50FinalProj
## Introduction
This web application was created with Flask in November 2023 by Ely Hahami for Harvard's CS 50 final project. Inspired by the fascinating linear algebra content in Math 25A (Theoretical Linear Algebra and Real Analysis I), this web app provides tools and functionalities to explore various concepts in linear algebra, including Gram-Schmidt Calculation, Matrix Diagonalization, Singular Value Decomposition (SVD) and more.

Lastly, inspired by David Malan's lecture on artificial intelligence and the current state of natural language processing, the last functionality is a specialized chatbot -- that is, a version of GPT 3.5 but fine-tuned on content from Sheldon Axler's well-regarded textbook "Linear Algebra Done Right." This means that users can ask complex questions about linear algebra and receive answers that are not only contextually accurate but also reflect the depth and pedagogical approach of Axler's work. Whether it's understanding the fundamentals of vector spaces, the subtleties of eigenvalues and eigenvectors, or the complexities of the spectral theorem or inner product spaces, the chatbot serves as an interactive tool that augments the learning experience.

## Requirements
Before running <the Linear Algebra Web App>, you need to have the following installed:
- Python 3.7 or above
- Flask
- Other dependencies listed in `requirements.txt` -- namely, numpy, dotenv, and openai. 

## Installation
To get <The Linear Algebra Web App> up and running on your local machine, follow these steps using VSCODE IDE:

1. Clone the repository: git clone <https://github.com/elyhahami18/CS50FinalProj.git>

2. Navigate to the project directory: cd CS50FinalProj

3. Install the required dependencies: pip install -r requirements.txt


## Configuration
Before starting the application, configure the necessary environment variables:

1. Create a `.env` file in the project root directory.
2. Add the following lines, replacing `<API_KEY>` with your actual API key:

## API Key Restriction
Please note that the chatbot feature in the source code requires an OpenAI API key, which is not included in the project repository for security reasons. Consequently, you will not be able to use the chatbot feature in your local setup without an API key.

However, you can interact with the chatbot in the deployed version of the application on Heroku, where the API key has been securely configured. We ensure the security of the API key using environment variables and do not expose it within the source code.

If you wish to use the chatbot feature locally, you will need to obtain your own API key from OpenAI and set it as an environment variable in your `.env` file as described in the Configuration section below.

## Running the Application
To run <the Linear Algebra Web App> locally, execute the following command: flask run
The application will be available at `http://127.0.0.1:5000/` by default.
Alternatively, you may view and interact with the web app here <https://linearalgebra-3d3395b01e23.herokuapp.com/>, thanks to deployment on Heroku. 

## Support
Should you need further assistance, please reach out to me at `elyhahami@college.harvard.edu`.


