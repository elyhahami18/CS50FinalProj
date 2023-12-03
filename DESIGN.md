# Project Design Document

## Overview

This document provides a technical overview of our project, a Flask-based web application (https://linearalgebra-3d3395b01e23.herokuapp.com/
) that offers various linear algebra computations and includes a specialized chatbot for mathematical inquiries. We'll discuss the core components, design decisions, and the rationale behind them.

## Core Components

### Flask Application (App.py)

Our project utilizes the Flask web framework for handling HTTP requests and responses. Flask's simplicity and flexibility make it an ideal choice for building a lightweight web application.

### Routes and Endpoints

We define several routes and endpoints to handle different functionalities:

- `/`: The home page serves an HTML template, providing users with a user-friendly interface and background information about the web app. 
- `/process`: This endpoint handles POST requests for computing the Gram-Schmidt process on a set of input vectors. It extracts the number of vectors and their sizes from the request, validates the input, and meticulously applies the Gram-Schmidt process. The result, a list of orthonormalized vectors, is returned as a JSON response.
- `/chat`: This endpoint empowers users to interact with a specialized chatbot that I fine-tuned on linear algebra data. It accepts a user's message, initializes the OpenAI client using an API key (securely stored as an environment variable), and generates a response using my specefic fine-tuned OpenAI chat model. The response is thoughtfully returned as a JSON response.
- `/diagonalize`: Responsible for diagonalizing square matrices, this endpoint starts by validating the input matrix's dimensions. Subsequently, it extracts the matrix data from the request and employs numpy to calculate the eigenvalues, eigenvectors, and the diagonal matrix. The results are meticulously returned in JSON format.
- `/signature`: For square matrices, this endpoint adeptly computes both the determinant and trace. It follows a similar validation process, extracts the matrix data, and employs numpy to calculate these essential linear algebra properties. The results are meticulously returned in JSON format.
- `/svd`: his versatile endpoint handles Singular Value Decomposition (SVD) for matrices, functioning seamlessly for both square and non-square matrices. It begins with dimension validation, matrix data extraction, and employs numpy to perform SVD. The results, including matrices U, S (singular values), and V^T (transpose of V), are returned in JSON format.

### Index.html

The index.html file serves as the front-end interface for our Linear Algebra Web Application. In this design document, I will provide an overview of how we implemented the project and the reasoning behind the design decisions made for this HTML file.

1. Structured Tabs for User Interaction: The core design decision behind our user interface was to organize the application into tabs. Each tab corresponds to a specific mathematical operation or feature, such as Gram-Schmidt calculation, Matrix Diagonalization, Singular Value Decomposition (SVD), and a specialized chatbot. This tab-based structure makes it intuitive for users to navigate the application and access the functionality they need. It also keeps the user interface clean and uncluttered.

2. Dynamically Generated Input Forms: We implemented JavaScript functions to dynamically generate input forms based on user input. For instance, in the Gram-Schmidt Calculation tab, users can specify the number of vectors and their size. The JavaScript function generateVectorInputs then generates the appropriate number of input fields for vector coordinates. This dynamic form generation simplifies the user experience, as users only see the necessary input fields, and it ensures that the input corresponds to the user's selection.

3. Consistency in Input Forms: Across all tabs that involve matrix or vector input, we maintain consistency in the design of input forms. Each input form includes fields to specify the size or dimensions of the matrix or vector and dynamically generated input fields for the matrix or vector elements. This consistency enhances user familiarity and reduces the learning curve when switching between different mathematical operations.

4. Real-Time Result Display: For each mathematical operation, we provide a designated div (e.g., "result," "matrixResult," "signatureResult," "svdResult") to display the results or messages. JavaScript functions handle form submissions, communicate with the server to perform calculations, and then update the respective result div with the computed results or error messages in real-time. This real-time feedback enhances the user experience and provides immediate feedback on the calculations performed.

5. Use of Bootstrap for Responsive Design: We utilize Bootstrap for styling and responsive design. Bootstrap's pre-built components ensure that our web application is mobile-friendly and visually appealing. It also provides consistency in design elements, such as the navigation bar and tabs.

6. Server-Side Validation: Input Data Validation: One of the primary focuses of server-side validation is to ensure that the data submitted by users through forms or API requests is valid and meets the required criteria. In our application, we perform input data validation for various mathematical operations, including Gram-Schmidt calculation, matrix diagonalization, matrix determinant and trace calculation, and SVD. 

We have dedicated validation functions for each mathematical operation in our Flask-based server application. These functions check input data for criteria such as matrix size, vector dimensions, data types, and value ranges. For example, in the Gram-Schmidt calculation, we validate that the input vectors are of the correct size and are numerical. Even if the user 'inspects' the web page and tries to change the minimum, maximum, or type allowed for the 'number of vectors' field, the computation will not execute and provide an error message to the user. Inspired by this type of error-handling in Finance, this kind of server-side validation is good design. 

Lastly, when input data doesn't pass validation, we generate meaningful error messages that explain to users what went wrong. These messages are designed to be user-friendly and guide users on how to correct their input. For example, if a user tries to calculate the Gram-Schmidt process with non-numeric input, they will receive an error message explaining the need for numerical input. If they try to diagonlize a square matrix with too large of a dimension, then they will recieve an error message explaining that the issue lies specifically with the dimension of their input.  


### External Libraries

We use several external libraries:

- `numpy`: For efficient matrix operations and numerical computations.
- `Flask`: As mentioned earlier, for building the web application.
- `OpenAI`: To integrate the chatbot functionality.
- `dotenv`: For managing environment variables securely.

### Helpers Module

We have a `helpers.py` module that contains functions for:

- Extracting and validating matrix data from HTTP requests.
- Implementing the Gram-Schmidt process for orthonormalization.
- Performing matrix diagonalization.
- Computing determinant, trace, and SVD.

Since many routes (such as `/diagonalize`, `/signature`, and `/svd`) need matrix input validation, we thought it was best design to abstract a singular matrix dimension validation function in helpers.py was used multiple times in app.py rather than copying and pasting code -- which we learned was bad practice. 
## Design Decisions
Here is a screenshot of how we fine-tuned GPT-3.5. I hand-picked and curated training data (that can be viewed in finetuning.jsonl) that can be thought of a prompt as input and desired response as output. Here is a screenshot from OpenAI playground that displays the decreasing training loss of our fine-tuned model:
<img width="1512" alt="Screenshot 2023-12-03 at 3 06 23 PM" src="https://github.com/elyhahami18/CS50FinalProj/assets/130234343/65cce9c8-ed13-435a-99af-c1cfeb38ffb9">

### Separation of Concerns

We follow the principle of separation of concerns by organizing our code into different modules and functions. This makes our codebase more maintainable and testable. For example, matrix operations are abstracted into helper functions in `helpers.py`, which can be reused across multiple endpoints.

### Validation and Error Handling

We prioritize input validation and error handling to ensure the reliability of our application. We validate input dimensions, data types, and handle various error scenarios gracefully, returning meaningful error messages to the user.

### Use of External Libraries

We leverage external libraries like `numpy` and the OpenAI API to simplify complex mathematical computations and chatbot functionality. These libraries provide robust, well-tested solutions, saving development time and ensuring accuracy.

### Flask's RESTful Design

We adhere to RESTful design principles by using HTTP methods (GET, POST) appropriately for each endpoint. This improves the clarity of our API and makes it easier for users to interact with our application programmatically.

### Privacy Protection

We use environment variables and the `dotenv` library to securely manage sensitive data, such as API keys. The actual API key is not hardcoded in the source code, enhancing security.

### Debug Mode

We set Flask to run in debug mode only during development, enhancing security in production environments.

## Conclusion

Our project's design focuses on providing a user-friendly interface for performing various linear algebra computations while ensuring robustness, security, and maintainability. The use of Flask, external libraries, and separation of concerns allows us to create a reliable and efficient web application.
