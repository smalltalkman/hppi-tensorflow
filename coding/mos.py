"""Implementation of MoS coding method
"""

__all__ = ['mos_code_of']

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

def mos_code_of(PS):
    """Get MoS Code of protein sequence."""
    MOS = [0]*7*7
    CS = classification_sequence_of(PS)
    Len = len(CS)
    for I in range(0, Len-1):
        for J in range(I+1, Len):
            CI = int(CS[I])-1
            CJ = int(CS[J])-1
            Index = CI*7+CJ
            MOS[Index] = MOS[Index] + 1
    Sum = Len*(Len-1)/2
    MOS = [Num*1.0/Sum for Num in MOS]
    return MOS

def main():
    PS = 'VCCPPVCVVCPPVCVPVPPCCV'
    print('PS=', PS)
    CS = classification_sequence_of(PS)
    print('CS=', CS)
    MOS = mos_code_of(PS)
    print('MOS=', MOS)

if __name__=="__main__":
    main()
