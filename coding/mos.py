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
# AAC = { '1':['1'], '2':['2'], '3':['3'], '4':['4'], '5':['5'], '6':['6'], '7':['7'], }

# AAC_L: Length of AAC.
AAC_L = len(AAC)
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

def mos_code_of_0(PS):
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

def mos_code_of_1(PS):
    """Get MoS Code of protein sequence."""
    # MOS = [[0]*7]*7
    MOS = [[0]*7 for _ in range(7)]
    CS = classification_sequence_of(PS)
    Len = len(CS)
    Line = [0]*7
    for I in range(Len-2, -1, -1):
        # print('I=', I)
        CI = int(CS[I  ])-1
        CJ = int(CS[I+1])-1
        # print('CI=', CI)
        # print('CJ=', CJ)
        Line[CJ] = Line[CJ]+1
        for P in range(7):
            MOS[CI][P] = MOS[CI][P]+Line[P]
        # print('MOS=', MOS)
    TMP = MOS
    MOS = []
    for L in TMP:
        MOS = MOS + L
    Sum = Len*(Len-1)/2
    MOS = [Num*1.0/Sum for Num in MOS]
    return MOS

def mos_code_of(PS):
    """Get MoS Code of protein sequence."""
    MOS = [[0]*AAC_L for _ in range(AAC_L)]
    CS = classification_sequence_of(PS)
    Len = len(CS)
    Line = [0]*AAC_L
    for I in range(Len-1, -1, -1):
        # print('I=', I)
        CI = int(CS[I  ])-1
        # print('CI=', CI)
        Line[CI] = Line[CI]+1
        for P in range(AAC_L):
            MOS[CI][P] = MOS[CI][P]+Line[P]
        # print('MOS=', MOS)
    # flat mos
    TMP = MOS
    MOS = []
    I   = 0
    for L in TMP:
        MOS = MOS + L[I:]
        I   = I   + 1
    # convert to proper decimal
    Sum = Len*(Len+1)/2
    MOS = [Num*1.0/Sum for Num in MOS]+[1.0/Sum]
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
