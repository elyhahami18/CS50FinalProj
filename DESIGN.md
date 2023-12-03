# Project Design Document

## Overview

This document provides a technical overview of our project, a Flask-based web application (https://linearalgebra-3d3395b01e23.herokuapp.com/
) that offers various linear algebra computations and includes a specialized chatbot for mathematical inquiries. We'll discuss the core components, design decisions, and the rationale behind them.

## Core Components

### Flask Application

Our project utilizes the Flask web framework for handling HTTP requests and responses. Flask's simplicity and flexibility make it an ideal choice for building a lightweight web application.

### Routes and Endpoints

We define several routes and endpoints to handle different functionalities:

- `/`: The home page, serving an HTML template.
- `/process`: Computes the Gram-Schmidt process for a set of input vectors.
- `/chat`: Utilizes the OpenAI API to provide a specialized chatbot for mathematical queries.
- `/diagonalize`: Diagonalizes a square matrix.
- `/signature`: Computes the determinant and trace of a square matrix.
- `/svd`: Performs Singular Value Decomposition (SVD) on matrices.

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
