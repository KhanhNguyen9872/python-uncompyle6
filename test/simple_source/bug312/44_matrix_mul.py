# Hard: matrix operations
def matrix_mul(a, b):
    rows_a = len(a)
    cols_a = len(a[0])
    cols_b = len(b[0])
    result = []
    for i in range(rows_a):
        row = []
        for j in range(cols_b):
            s = 0
            for k in range(cols_a):
                s += a[i][k] * b[k][j]
            row.append(s)
        result.append(row)
    return result

m1 = [[1, 2], [3, 4]]
m2 = [[5, 6], [7, 8]]
print(matrix_mul(m1, m2))
