from flask import request, jsonify
import numpy as np


def gram_schmidt(V):
    """
    Applies the Gram-Schmidt process to a list of vectors V in R^n.

    Parameters:
    V (list of np.array): A list of vectors (arrays) in R^n.

    Returns:
    list of np.array: A list of orthonormal vectors.
    """
    U = []
    for v in V:
        u = v.astype(float)  # Ensure the vector is of float type
        for i in range(len(U)):
            u -= np.dot(u, U[i]) * U[i]
        norm_u = np.linalg.norm(u)
        if norm_u > 1e-10:  # Avoid divide by zero or very small values
            u /= norm_u
            U.append(u)
    return U


def extract_matrix_from_request(rows, cols):
    matrix = []
    # Loop through the matrix to populate it with elements from the request
    for i in range(int(rows)):
        row = []
        # Can use int(rows) or int(cols) because dimensions will be validated in validate_matrix_dimensions function BEFORE extract_matrix_from_request is called
        for j in range(int(cols)):
            element = request.form.get(f"matrix[{i}][{j}]")
            if element:
                try:
                    row.append(float(element))
                except ValueError:
                    # Return an error if an element is not a valid float
                    return None, jsonify({"error": f"Error: Invalid data type."}), 400
            else:
                # Return an error if an element is missing
                return None, jsonify({"error": f"Error: Missing data."}), 400
        matrix.append(row)
    return matrix, None


# Helper function to validate dimensions of a matrix between a certain desired range
def validate_matrix_dimensions(rows, cols, min_size=2, max_size=7):
    try:
        rows = int(rows)
        cols = int(cols)
        # Make sure rows and cols are between min_size and max_size, inclusive
        if not (min_size <= rows <= max_size and min_size <= cols <= max_size):
            return False, f"Dimensions must be between {min_size} and {max_size}"
        return True, None
    except ValueError:
        # If the exception is reached, rows and cols were not convertible to an integer
        return False, "Dimensions must be integers"
