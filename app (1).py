from flask import Flask, request, render_template_string, jsonify
import numpy as np
from helpers import (
    gram_schmidt,
    extract_matrix_from_request,
    validate_matrix_dimensions,
)
from openai import OpenAI
from dotenv import load_dotenv
import os

# Initialize Flask application
app = Flask(__name__)


# Route for the home page, handling GET requests
@app.route("/", methods=["GET"])
def index():
    with open("index.html", "r") as file:
        return render_template_string(file.read())


# Route for Gram–Schmidt Process Calculation Tab
@app.route("/process", methods=["POST"])
def process():
    # Extracting and validating input data for number of vectors and their sizes

    number_of_vectors = request.form.get("numberOfVectors")
    size_of_vectors = request.form.get("sizeOfVectors")

    is_valid, error_message = validate_matrix_dimensions(
        number_of_vectors, size_of_vectors, min_size=1, max_size=10
    )
    if not is_valid:
        return jsonify({"error": error_message}), 400

    # Now that these are validated, convert these values to integers
    number_of_vectors = int(number_of_vectors)
    size_of_vectors = int(size_of_vectors)

    # Constructing vectors from input data
    vectors = []
    for i in range(1, number_of_vectors + 1):
        vectors = []
    for i in range(1, number_of_vectors + 1):
        vector = []
        for j in range(size_of_vectors):
            coordinate = request.form.get(f"vector{i}[{j}]")
            # Checking for empty coordinate values
            if coordinate == "":
                return jsonify({"success": False, "error": f"Missing data"}), 400
            else:
                try:
                    vector.append(float(coordinate))
                except ValueError:
                    return (
                        jsonify({"success": False, "error": f"Invalid data type"}),
                        400,
                    )
        vectors.append(np.array(vector))

    # Applying the Gram-Schmidt process (from helpers.py) to the vectors
    orthonormal_vectors = gram_schmidt(vectors)

    return jsonify(
        {
            "success": True,
            "message": "Orthonormal list of vectors computed successfully.",
            "orthonormal_vectors": [v.tolist() for v in orthonormal_vectors],
        }
    )


# Route for handling the specialized chatbot functionality using OpenAI API / Fine-Tuning
@app.route("/chat", methods=["POST"])
def chat():
    # Extract the message from the form
    user_message = request.form["message"]

    # Initialize OpenAI client using API key from environment variable
    # Write "OPENAI_API_KEY" instead of actual openAPI key for privacy protection
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Generating a response from OpenAI's chat model
    # Note that 'model="ft:gpt-3.5-turbo-1106:personal::8QTHrMqA' is the specefic model I fine-tuned using Linear Algebra data in finetuning.jsonl
    completion = client.chat.completions.create(
        model="ft:gpt-3.5-turbo-1106:personal::8QTHrMqA",
        messages=[
            {
                "role": "system",
                "content": "You are a mathematician, specialized in linear algebra. You are known for your meticulous approach to problem-solving and your focus on logical consistency, clarity, precision, and thoroughly justifying your work.",
            },
            {"role": "user", "content": user_message},
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    # Extracting and returning the response from the model
    response = (
        completion.choices[0].message.content
        if completion.choices[0].message
        else "No response"
    )
    return jsonify({"response": response})


# Flask route for diagonalizing a matrix, handling POST requests
@app.route("/diagonalize", methods=["POST"])
def diagonalize_matrix():
    # Extract and validate the size of the matrix from the request

    matrix_size = request.form.get("matrixSize")
    # Use the helper function (abstracted because used multiple times) to validate matrix dimensions
    is_valid, error_message = validate_matrix_dimensions(matrix_size, matrix_size)
    if not is_valid:
        return jsonify({"error": error_message}), 400

    # Call upon extract_matrix_from_request function from helpers.py (abstracted because function used in diagonalization, determinant/trace, and SVD)
    # n x n matrix
    matrix, error = extract_matrix_from_request(matrix_size, matrix_size)
    if error:
        return error

    # Perform matrix diagonalization using numpy
    try:
        matrix_np = np.array(matrix)
        eigvals, eigvecs = np.linalg.eig(matrix_np)
        P = eigvecs

        # Create diagonal matrix from eigenvalues
        D = np.diag(eigvals)

        P_inv = np.linalg.inv(P)
        # Reconstruct original matrix A as PDP^-1

        A_reconstructed = P.dot(D).dot(P_inv)

    # Return an error if the matrix cannot be diagonalized
    except np.linalg.LinAlgError:
        return "Error: Matrix cannot be diagonalized", 400

    # Return eigenvalues, eigenvectors, the diagonal matrix, and the reconstructed matrix
    return {
        "original_matrix": matrix_np.tolist(),
        "eigenvalues": eigvals.tolist(),
        "eigenvectors": [vec.tolist() for vec in eigvecs],
        "diagonal_matrix": D.tolist(),
        "inverse_of_P": P_inv.tolist(),
        "reconstructed_matrix": A_reconstructed.tolist(),
    }


# Flask route for computing the determinant and trace of a matrix (the signature in the 2x2 symmetric matrix case), handling POST requests
@app.route("/signature", methods=["POST"])
def compute_signature():
    matrix_size = request.form.get("matrixSize")
    # Use the helper function (abstracted because used multiple times) to validate matrix dimensions
    is_valid, error_message = validate_matrix_dimensions(matrix_size, matrix_size)
    if not is_valid:
        return jsonify({"error": error_message}), 400

    # n x n matrix
    matrix, error = extract_matrix_from_request(matrix_size, matrix_size)

    if error:
        return error

    # Compute the trace and determinant of the matrix using numpy
    try:
        matrix_np = np.array(matrix)
        trace = np.trace(matrix_np)
        determinant = np.linalg.det(matrix_np)
    except Exception as e:
        # Return an error for any exception during computation
        return {"error": str(e)}, 400

    return {"trace": trace, "determinant": determinant}


# Flask route for computing the Singular Value Decomposition (SVD) of a matrix, handling POST requests
# Note that SVD works for square (n x n) matrices as well as nonsquare (m x n) matrices,
# while diagonilization/determinant/trace worked only for square matrices
@app.route("/svd", methods=["POST"])
def compute_svd():
    rows = request.form.get("matrixRows")
    cols = request.form.get("matrixCols")

    # Use the helper function (abstracted because used multiple times) to validate matrix dimensions
    is_valid, error_message = validate_matrix_dimensions(rows, cols)
    if not is_valid:
        return jsonify({"error": error_message}), 400

    matrix, error = extract_matrix_from_request(rows, cols)

    if error:
        return error

    # Perform the SVD using numpy
    try:
        matrix_np = np.array(matrix)
        U, S, VT = np.linalg.svd(matrix_np)
    except np.linalg.LinAlgError:
        return {"error": "SVD computation failed"}, 400

    # Return the relevant matrices U, S, and V transpose from the SVD
    return {"U_matrix": U.tolist(), "S_values": S.tolist(), "VT_matrix": VT.tolist()}


# Main execution block to run the Flask app in debug mode
if __name__ == "__main__":
    app.run(debug=True)
