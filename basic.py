import sys
import time
import resource

DELTA = 30

# mismatch costs 
# A=0, C=1, G=2, T=3
# Matrix order: A, C, G, T
# A-A=0, A-C=110, A-G=48, A-T=94 ...
ALPHA = [
    [0, 110, 48, 94],   
    [110, 0, 118, 48],  
    [48, 118, 0, 110], 
    [94, 48, 110, 0]   
]


def read_input_file(file_path):
    """
    Parses the input file to extract base strings and indices.
    """
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    
    base_x = lines[0]
    indices_x = []
    
    current_line_idx = 1
    while current_line_idx < len(lines):
        line = lines[current_line_idx]
        if not line.isdigit():
            break
        indices_x.append(int(line))
        current_line_idx += 1
        
    base_y = lines[current_line_idx]
    indices_y = []
    current_line_idx += 1
    
    while current_line_idx < len(lines):
        indices_y.append(int(lines[current_line_idx]))
        current_line_idx += 1
        
    return base_x, indices_x, base_y, indices_y


def generate_string(base_str, indices):
    """
    Generates string through inserting current string in itself at specified indices.
    """
    current_string = base_str
    for index in indices:
        current_string = current_string[:index+1] + current_string + current_string[index+1:]
        
    return current_string


def processing_memory():
    """
    Returns  peak memory usage.
    """
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    if sys.platform == 'darwin': 
        return usage / 1024
    else:
        return usage

    
def get_index(char):
    mapping = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    return mapping[char]


def sequence_alignment(x, y):
    m, n = len(x), len(y)

    # dp table initialization
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        dp[i][0] = i * DELTA
    for j in range(1, n + 1):
        dp[0][j] = j * DELTA

    # bottom up pass
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            p = get_index(x[i - 1])
            q = get_index(y[j - 1])

            cost_match = dp[i - 1][j - 1] + ALPHA[p][q]
            cost_gap_x = dp[i - 1][j] + DELTA
            cost_gap_y = dp[i][j - 1] + DELTA

            dp[i][j] = min(cost_match, cost_gap_x, cost_gap_y)

    # top down pass
    aligned_x = []
    aligned_y = []

    i, j = m, n
    while i > 0 or j > 0:

        if i > 0 and j > 0:
            p = get_index(x[i - 1])
            q = get_index(y[j - 1])

            if dp[i][j] == dp[i - 1][j - 1] + ALPHA[p][q]:
                aligned_x.append(x[i - 1])
                aligned_y.append(y[j - 1])
                i -= 1
                j -= 1
                continue

        if i > 0 and dp[i][j] == dp[i - 1][j] + DELTA:
            aligned_x.append(x[i - 1])
            aligned_y.append("_")
            i -= 1
        else:
            aligned_x.append("_")
            aligned_y.append(y[j - 1])
            j -= 1

    aligned_x.reverse()
    aligned_y.reverse()

    return dp[m][n], "".join(aligned_x), "".join(aligned_y)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 basic.py <input_file> <output_file>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    base_x, ind_x, base_y, ind_y = read_input_file(input_path)
    final_x = generate_string(base_x, ind_x)
    final_y = generate_string(base_y, ind_y)
    
    start_time = time.time()

    cost, align_x, align_y = sequence_alignment(final_x, final_y)
    
    end_time = time.time()
    time_taken_ms = (end_time - start_time) * 1000
    memory_used_kb = processing_memory()
    
    with open(output_path, 'w') as f:
        f.write(f"{cost}\n")
        f.write(f"{align_x}\n")
        f.write(f"{align_y}\n")
        f.write(f"{time_taken_ms}\n")
        f.write(f"{memory_used_kb}\n")
