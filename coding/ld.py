"""Implementation of LD coding method
"""

__all__ = ['ld_code_of']

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

def ld_info_of(CS):
    L = len(CS)
    C = {}
    T = {}
    for I, CH in enumerate(CS):
        if CH not in C:
            C[CH] = []
        C[CH].append(I+1)
        if I > 0:
            PCH = CS[I-1]
            if PCH != CH:
                if int(PCH)<int(CH):
                    TIndex = PCH + CH
                else:
                    TIndex = CH + PCH
                if TIndex not in T:
                    T[TIndex] = 0
                T[TIndex] = T[TIndex]+1
    return L, C, T

def ld_code_of_0(CS):
    RC = [0]*7
    RT = [0]*21
    RD = [0]*35
    L, C, T = ld_info_of(CS)
    for Class, Indexs in C.items():
        Len = len(Indexs)
        RC[int(Class)-1]=Len*1.0/L
        Residues = [1, int(Len*0.25), int(Len*0.5), int(Len*0.75), Len]
        # Residues = list(map(lambda x:x*1.0/L, Residues))
        Residues = list(map(lambda x:Indexs[x-1]*1.0/L, Residues))
        RD[(int(Class)-1)*5:int(Class)*5] = Residues
    for Trans, Frequency in T.items():
        PI, I = int(Trans[0])-1, int(Trans[1])-1
        Index = int((21-(6-PI)*(6-PI+1)/2)+(I-PI-1))
        RT[Index] = Frequency*1.0/(L-1)
    # return RC, RT, RD
    return RC+RT+RD

def ld_code_of(PS):
    """Get LD Code of protein sequence."""
    CS = classification_sequence_of(PS)
    L = len(CS)
    A = ld_code_of_0(CS[          0:int(L*0.25)])
    B = ld_code_of_0(CS[int(L*0.25):int(L*0.50)])
    C = ld_code_of_0(CS[int(L*0.50):int(L*0.75)])
    D = ld_code_of_0(CS[int(L*0.75):L          ])
    E = ld_code_of_0(CS[          0:int(L*0.50)])
    F = ld_code_of_0(CS[int(L*0.50):L          ])
    G = ld_code_of_0(CS[int(L*0.25):int(L*0.75)])
    H = ld_code_of_0(CS[          0:int(L*0.75)])
    I = ld_code_of_0(CS[int(L*0.25):L          ])
    J = ld_code_of_0(CS[int(L*0.125):int(L*0.875)])
    return A+B+C+D+E+F+G+H+I+J

if __name__=="__main__":
    PS = 'VCCPPVCVVCPPVCVPVPPCCV'
    print('PS=', PS)
    CS = classification_sequence_of(PS)
    print('CS=', CS)
    LD_INFO = ld_info_of(CS)
    print('LD_INFO=', LD_INFO)
    LD_CODE = ld_code_of_0(CS)
    print('LD_CODE=', LD_CODE)
    LD_CODE = ld_code_of(PS)
    print('LD_CODE=', LD_CODE)
