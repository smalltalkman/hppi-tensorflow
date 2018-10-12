"""Implementation of MoS0 coding method
"""

__all__ = ['mos0_code_of']

# AAC: Classification of amino acids.
AAC = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y', ]

# AAC_L: Length of AAC.
AAC_L = len(AAC)
# AAC_R: Reverse of AAC.
AAC_R = {}
for I, CH in enumerate(AAC):
    AAC_R[CH] = str(I+1)

def classification_of(AA):
    """Get classification of amino acids."""
    return AAC_R[AA]

def classification_sequence_of(PS):
    """Make classification sequence from protein sequence."""
    CS = ''
    for I, CH in enumerate(PS):
        CS = CS + classification_of(CH)
    return CS

def mos0_code_of(PS):
    """Get MoS0 Code of protein sequence."""
    MOS0 = [[0]*AAC_L for _ in range(AAC_L)]
    CS = classification_sequence_of(PS)
    Len = len(CS)
    Line = [0]*AAC_L
    for I in range(Len-1, -1, -1):
        # print('I=', I)
        CI = int(CS[I  ])-1
        # print('CI=', CI)
        Line[CI] = Line[CI]+1
        for P in range(AAC_L):
            MOS0[CI][P] = MOS0[CI][P]+Line[P]
        # print('MOS0=', MOS0)
    # flat mos
    TMP = MOS0
    MOS0 = []
    I   = 0
    for L in TMP:
        MOS0 = MOS0 + L[I:]
        I   = I   + 1
    # convert to proper decimal
    Sum = Len*(Len+1)/2
    MOS0 = [Num*1.0/Sum for Num in MOS0]+[1.0/Sum]
    return MOS0

def main():
    PS = 'VCCPPVCVVCPPVCVPVPPCCV'
    print('PS=', PS)
    CS = classification_sequence_of(PS)
    print('CS=', CS)
    MOS0 = mos0_code_of(PS)
    print('MOS0=', MOS0)

if __name__=="__main__":
    main()
