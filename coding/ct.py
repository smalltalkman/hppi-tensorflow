"""Implementation of CT coding method
"""

__all__ = ['ct_code_of']

# AAC: Classification of amino acids.
AAC = {
    '1': ['A', 'G', 'V'],
    '2': ['I', 'L', 'F', 'P'],
    '3': ['Y', 'M', 'T', 'S'],
    '4': ['H', 'N', 'Q', 'W'],
    '5': ['R', 'K'],
    '6': ['D', 'E'],
    '7': ['C']
}

# AAC_R: Reverse of AAC.
AAC_R = {}
for C, AAS in AAC.items():
    for AA in AAS:
        AAC_R[AA] = C

def classification_of(AA):
    """Get classification of amino acids."""
    return AAC_R[AA]

def classification_sequence_of(PS):
    """Make classification sequence from protein sequence."""
    CS = ''
    for I, CH in enumerate(PS):
        CS = CS + classification_of(CH)
    return CS

def ct_code_of(PS):
    """Get CT Code of protein sequence."""
    CT_Code = [0]*343
    CS = classification_sequence_of(PS)
    for I in range(len(CS)-2):
        SubCS = CS[I:I+3]
        CT_Code_Index = int(SubCS[0]) + (int(SubCS[1])-1)*7 + (int(SubCS[2])-1)*7*7
        CT_Code[CT_Code_Index-1] = CT_Code[CT_Code_Index-1] + 1
    SUM = sum(CT_Code)
    CT_Code = [N*1.0/SUM for N in CT_Code]
    # Normalizing CT_Code
    # MIN_CODE = min(CT_Code)
    # MAX_CODE = max(CT_Code)
    # CT_Code = [(N-MIN_CODE)*1.0/(MAX_CODE-MIN_CODE) for N in CT_Code]
    return CT_Code

if __name__=="__main__":
    for I, Frequency in enumerate(ct_code_of('MREIVHIQAG')):
        if Frequency>0 :
            print(I+1, Frequency)
