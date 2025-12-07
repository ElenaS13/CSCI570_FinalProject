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

def get_index(char):
    mapping = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    return mapping[char]

def get_efficient_cost(x, y):
    """
    Calculates alignment cost of string x and string y using 2 only rows for memory.
    Returns the final column/row for costs.
    """
    m = len(x)
    n = len(y)
    
    prev = [j * DELTA for j in range(n + 1)]
    
    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        curr[0] = i * DELTA
        
        for j in range(1, n + 1):
            char_x = x[i-1]
            char_y = y[j-1]
            mismatch_cost = ALPHA[get_index(char_x)][get_index(char_y)]
            
            val1 = prev[j-1] + mismatch_cost
            val2 = prev[j] + DELTA
            val3 = curr[j-1] + DELTA
            
            curr[j] = min(val1, val2, val3)
            
        prev = curr
        
    return prev

def solve_base_case(x, y):
    m, n = len(x), len(y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1): dp[i][0] = i * DELTA
    for j in range(n + 1): dp[0][j] = j * DELTA

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match = dp[i-1][j-1] + ALPHA[get_index(x[i-1])][get_index(y[j-1])]
            gap_x = dp[i-1][j] + DELTA
            gap_y = dp[i][j-1] + DELTA
            dp[i][j] = min(match, gap_x, gap_y)

    align_x, align_y = [], []
    i, j = m, n
    while i > 0 or j > 0:
        curr = dp[i][j]
        if i > 0 and j > 0 and curr == dp[i-1][j-1] + ALPHA[get_index(x[i-1])][get_index(y[j-1])]:
            align_x.append(x[i-1]); align_y.append(y[j-1])
            i -= 1; j -= 1
        elif i > 0 and curr == dp[i-1][j] + DELTA:
            align_x.append(x[i-1]); align_y.append('_')
            i -= 1
        else:
            align_x.append('_'); align_y.append(y[j-1])
            j -= 1

    return dp[m][n], "".join(align_x[::-1]), "".join(align_y[::-1])


def generate_string(base_str, indices):
    """
    Generates string through inserting current string in itself at specified indices.
    """
    current_string = base_str
    for index in indices:
        current_string = current_string[:index+1] + current_string + current_string[index+1:]
        
    return current_string

def divide_conquer(x, y):
    m = len(x)
    n = len(y)
    
    if m <= 2 or n <= 2:
        return solve_base_case(x, y)
    
    x_mid = m // 2

    score_left = get_efficient_cost(x[:x_mid], y)
    

    score_right = get_efficient_cost(x[x_mid:][::-1], y[::-1])
    

    min_cost = float('inf')
    split_index = -1
    
    for k in range(n + 1):
        current_cost = score_left[k] + score_right[n - k]
        if current_cost < min_cost:
            min_cost = current_cost
            split_index = k
            

    cost1, align_x1, align_y1 = divide_conquer(x[:x_mid], y[:split_index])
    cost2, align_x2, align_y2 = divide_conquer(x[x_mid:], y[split_index:])
    
    return cost1 + cost2, align_x1 + align_x2, align_y1 + align_y2



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

def processing_memory():
    """
    Returns  peak memory usage.
    """
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    if sys.platform == 'darwin': 
        return usage / 1024
    else:
        return usage

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 efficient.py <input_file> <output_file>")
        sys.exit(1)
        
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    base_x, ind_x, base_y, ind_y = read_input_file(input_path)
    final_x = generate_string(base_x, ind_x)
    final_y = generate_string(base_y, ind_y)
    
    start_time = time.time()
    
    cost, align_x, align_y = divide_conquer(final_x, final_y)
    
    end_time = time.time()
    time_taken_ms = (end_time - start_time) * 1000
    memory_used_kb = processing_memory()
    
    with open(output_path, 'w') as f:
        f.write(f"{cost}\n")
        f.write(f"{align_x}\n")
        f.write(f"{align_y}\n")
        f.write(f"{time_taken_ms}\n")
        f.write(f"{memory_used_kb}\n")