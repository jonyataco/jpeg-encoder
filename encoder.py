# Program that will perform lossless JPEG compression.
# Given a greyscale image, this program will perform the encoding and decoding.

from bitarray import bitarray

IMAGE_SIZE = 16

# The given greyscale image for the assignment
given_image = [
    [88, 88, 88, 89, 90, 91, 92, 93, 94, 95, 93, 95, 96, 98, 97, 94],
    [93, 91, 91, 90, 92, 93, 94, 94, 95, 95, 92, 93, 95, 95, 95, 96],
    [95, 95, 95, 95, 96, 97, 94, 96, 97, 96, 98, 97, 98, 99, 95, 97],
    [97, 96, 98, 97, 98, 94, 95, 97, 99, 100, 99, 101, 100, 100, 98, 98],
    [99, 100, 97, 99, 100, 100, 98, 98, 100, 101, 100, 99, 101, 102, 99, 100],
    [100, 101, 100, 99, 101, 102, 99, 100, 103, 102, 103, 101, 101, 100, 102, 101],
    [100, 102, 103, 101, 101, 100, 102, 103, 103, 105, 104, 104, 103, 104, 104, 103],
    [103, 105, 103, 105, 105, 104, 104, 104, 102, 101, 100, 100, 100, 101, 102, 103],
    [104, 104, 105, 105, 105, 104, 104, 106, 102, 103, 101, 101, 102, 101, 102, 102],
    [102, 105, 105, 105, 106, 104, 106, 104, 103, 101, 100, 100, 101, 102, 102, 103],
    [102, 105, 105, 105, 106, 104, 106, 104, 103, 101, 100, 100, 101, 102, 102, 103],
    [102, 105, 105, 105, 106, 104, 105, 104, 103, 101, 102, 100, 102, 102, 102, 103],
    [104, 105, 106, 105, 106, 104, 106, 103, 103, 102, 100, 100, 101, 102, 102, 103],
    [103, 105, 107, 107, 106, 104, 106, 104, 103, 101, 100, 100, 101, 102, 102, 103],
    [103, 105, 106, 108, 106, 104, 106, 105, 103, 101, 101, 100, 101, 103, 102, 105],
    [102, 105, 105, 105, 106, 104, 106, 107, 104, 103, 102, 100, 101, 104, 102, 104]
]

# The given huffman table used in order to encode/decode.
huffman_table = {
    0: bitarray('1'),
    1: bitarray('00'),
    -1: bitarray('011'),
    2: bitarray('0100'),
    -2: bitarray('01011'),
    3: bitarray('010100'),
    -3: bitarray('0101011'),
    4: bitarray('01010100'),
    -4: bitarray('010101011'),
    5: bitarray('0101010100'),
    -5: bitarray('01010101011'),
    6: bitarray('010101010100'),
    -6: bitarray('0101010101011')
}

# Returns the difference value given the case and X, A, B, and C.
def performPrediction(case, X, A, B, C):
    if case == 1:
        return X - A
    elif case == 2:
        return X - B
    elif case == 3:
        return X - C
    elif case == 4:
        return X - (A + B - C)
    elif case == 5:
        return X - (A + round(((B - C)/2)))
    elif case == 6:
        return X - (B + round(((A - C)/2)))
    elif case == 7:
        return X - round(((A + B)/2))

# Performs the inverse prediction used during decoding.
def performInversePrediction(case, X, A, B, C):
    if case == 1:
        return X + A
    elif case == 2:
        return X + B
    elif case == 3:
        return X + C
    elif case == 4:
        return X + (A + B - C)
    elif case == 5:
        return X + (A + round(((B - C)/2)))
    elif case == 6:
        return X + (B + round(((A - C)/2)))
    elif case == 7:
        return X + round(((A + B)/2))

# Prints an image in a formmated manner given a matrix
def printImage(matrix):
    formattedMatrix = ""
    for row in matrix:
        formattedMatrix = formattedMatrix + str(row)
        formattedMatrix = formattedMatrix + "\n"
    return formattedMatrix

# Creates the coefficient matrix given an image and a case for the predictor.
def createCoefficientMatrix(image, case):
    coefficientMatrix = [[0 for x in range(IMAGE_SIZE)] for y in range(IMAGE_SIZE)]
    for i in range(IMAGE_SIZE):
        for j in range(IMAGE_SIZE):
            # For the first value [0,0] it will always be the same.
            if i == 0 and j == 0:
                coefficientMatrix[i][j] = image[i][j]
            # Check to see if we are in the first row.
            # If so, then apply the first prediction formula.
            # DX = X - A
            elif i == 0:
                coefficientMatrix[i][j] = image[i][j] - image[i][j-1]
            # Check to see if we are in the first column.
            # If we are then use B to perform the prediction.
            # DX = X - B
            elif j == 0:
                coefficientMatrix[i][j] = image[i][j] - image[i-1][j]
            # Otherwise we just use the prediction formula
            else:
                coefficientMatrix[i][j] = performPrediction(case, image[i][j], image[i][j-1], image[i-1][j], image[i-1][j-1])
    return coefficientMatrix

# Creates the bit matrix given the coefficient matrix
def createBitMatrix(matrix):
    bitMatrix = [[0 for x in range(IMAGE_SIZE)] for y in range(IMAGE_SIZE)]
    for i in range(IMAGE_SIZE):
        for j in range(IMAGE_SIZE):
            # The first value [0,0] will be the same
            if i == 0 and j == 0:
                bitMatrix[i][j] = matrix[i][j]
            # All other values will look into the huffman_table and
            # return the corresponding bits. 
            # Program represents the bits as a bitarry
            else:
                bitMatrix[i][j] = huffman_table[matrix[i][j]]
    return bitMatrix

# Utility function to print the bit matrix in binary form
def printBitMatrix(matrix):
    bitMatrix = [[0 for x in range(IMAGE_SIZE)] for y in range(IMAGE_SIZE)]
    for i in range(IMAGE_SIZE):
        for j in range(IMAGE_SIZE):
            # Change the first number to its binary representation
            if i == 0 and j == 0:
                bitMatrix[i][j] = bin(matrix[i][j])
            # use the to01() method to print bits as a string
            else:
                bitMatrix[i][j] = matrix[i][j].to01()
    return printImage(bitMatrix)

# Utility function that returns the number of bits in a compressed image
def getNumOfBits(matrix):
    num = 0
    for i in range(IMAGE_SIZE):
        for j in range(IMAGE_SIZE):
            # The first number [0,0] will always have 8 bits in this case
            if i == 0 and j == 0:
                num += 8
            # Get the length of the bitarray in all other cases (number of bits)
            else:
                num += len(matrix[i][j])
    return num

# Utility function to retrieve key for decoding purposes
def get_key(val):
    for key, value in huffman_table.items():
        if val == value:
            return key

# Recreates coefficient matrix from compressed matrix
def createCoefficientMatrixFromCompressedMatrix(matrix):
    # Creates a matrix of size IMAGE_SIZE x IMAGE_SIZE and sets all values to 0
    coefficientMatrix = [[0 for x in range(IMAGE_SIZE)] for y in range(IMAGE_SIZE)]
    for i in range(IMAGE_SIZE):
        for j in range(IMAGE_SIZE):
            # First value will be the same
            if i == 0 and j == 0:
                coefficientMatrix[i][j] = int(matrix[i][j])
            # Second value will be the key that corresponds to the bit value
            else:
                coefficientMatrix[i][j] = get_key(matrix[i][j])
    return coefficientMatrix

# Recreates the original image from the recreated coefficient matrix
def createOriginalImage(matrix, case):
    # Creates a matrix of size IMAGE_SIZE x IMAGE_SIZE and sets all values to 0
    original_image = [[0 for x in range(IMAGE_SIZE)] for y in range(IMAGE_SIZE)]
    for i in range(IMAGE_SIZE):
        for j in range(IMAGE_SIZE):
            # The first value will be the same
            if i == 0 and j == 0:
                original_image[i][j] = matrix[i][j]
            # This case covers the first row so use inverse of first case.
            elif i == 0:
                original_image[i][j] = matrix[i][j] + original_image[i][j-1]
            # This case covers the first column so use inverse of second case.
            elif j == 0:
                original_image[i][j] = matrix[i][j] + original_image[i-1][j]
            # Otherwise use coressponding inverse formula based on given case
            else:
                original_image[i][j] = performInversePrediction(case, matrix[i][j], original_image[i][j-1], original_image[i-1][j], original_image[i-1][j-1])
    return original_image

# Performs an experiment given a case to use for the prediction formula.
# Writes the results of an experiment to a seperate txt file
def performExperiment(case):
    file_name = str(case) + "_case.txt"
    f = open(file_name, "w")
    f.write("Case being tested: " + str(case) + "\n")
    f.write("The original image is: \n")
    f.write(printImage(given_image))
    # ENCODING PROCESS 
    new_image = createCoefficientMatrix(given_image, case)
    bit_matrix = createBitMatrix(new_image)
    f.write("\nThis is the created coefficient matrix: \n")
    f.write(printImage(new_image))
    f.write("\nThis is the compressed image: \n")
    f.write(printBitMatrix(bit_matrix))
    # DECODING PROCESS
    decoded_image = createCoefficientMatrixFromCompressedMatrix(bit_matrix)
    f.write("\nThis is the image after huffman decoder: \n")
    f.write(printImage(decoded_image))
    if decoded_image == new_image:
        f.write("\nThe decoded image is equal to the coefficient matrix. \n")
    f.write("Now recreating the original image using decompression... \n")
    original_image = createOriginalImage(decoded_image, case)
    f.write("The original image is: \n")
    f.write(printImage(original_image))
    compression_ratio = 2048 / getNumOfBits(bit_matrix)
    beats_per_pixel = 8 / compression_ratio
    f.write("\nThe compression ratio is: " + str(compression_ratio))
    f.write("\nThe bits/pixel is: " + str(beats_per_pixel))
    # Checks to make sure the recreated image is equal to the given image
    if given_image == original_image:
        f.write("\nThe RMS Erorr is 0")
        f.write("\nSuccessful recreation\n")
    f.close()

if __name__ == "__main__":
    for case in range(1,8):
        performExperiment(case)
