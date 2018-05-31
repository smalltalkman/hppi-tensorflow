"""Implementation of MoS1 coding method
"""

__all__ = ['mos1_code_of', 'corrcoef_of']

import numpy as np
import sys
epsilon = sys.float_info.epsilon

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

v_classification_of = np.vectorize(classification_of)

def classification_sequence_of(PS):
    """Make classification sequence from protein sequence."""
    return ''.join(v_classification_of(np.array(list(PS))))

def mos1_code_of(PS):
    """Get MoS1 Code of protein sequence."""
    # MoS1 = np.zeros( (AAC_L, AAC_L) )
    MoS1 = np.eye( AAC_L ) * epsilon
    CS = classification_sequence_of(PS)
    Len = len(CS)
    Line = np.zeros(AAC_L)
    for I in range(Len-2, -1, -1):
        # print('I=', I)
        CI = int(CS[I  ])-1
        CJ = int(CS[I+1])-1
        # print('CI=', CI)
        # print('CJ=', CJ)
        Line[CJ] += 1
        MoS1[CI] += Line
        # print('MoS1=', MoS1)
    Sum = Len*(Len-1)/2
    MoS1 = MoS1/Sum
    return MoS1

def corrcoef_of(PS1, PS2):
    CC = np.zeros( (AAC_L, AAC_L) )
    Code1 = mos1_code_of(PS1)
    Code2 = mos1_code_of(PS2)
    for I, VI in enumerate(Code1):
        for J, VJ in enumerate(Code2):
            corrcoef = np.corrcoef(VI, VJ)
            corrcoef = (corrcoef+1)/2
            CC[I, J] = corrcoef[0, 1]
    return CC

def main():
    PS = 'VCCPPVCVVCPPVCVPVPPCCV'
    print('PS=', PS)
    CS = classification_sequence_of(PS)
    print('CS=', CS)
    MoS1 = mos1_code_of(PS)
    print('MoS1=', MoS1.flatten().tolist())
    PS1 = 'MESSKKMDSPGALQTNPPLKLHTDRSAGTPVFVPEQGGYKEKFVKTVEDKYKCEKCHLVLCSPKQTECGHRFCESCMAALLSSSSPKCTACQESIVKDKVFKDNCCKREILALQIYCRNESRGCAEQLMLGHLLVHLKNDCHFEELPCVRPDCKEKVLRKDLRDHVEKACKYREATCSHCKSQVPMIALQKHEDTDCPCVVVSCPHKCSVQTLLRSELSAHLSECVNAPSTCSFKRYGCVFQGTNQQIKAHEASSAVQHVNLLKEWSNSLEKKVSLLQNESVEKNKSIQSLHNQICSFEIEIERQKEMLRNNESKILHLQRVIDSQAEKLKELDKEIRPFRQNWEEADSMKSSVESLQNRVTELESVDKSAGQVARNTGLLESQLSRHDQMLSVHDIRLADMDLRFQVLETASYNGVLIWKIRDYKRRKQEAVMGKTLSLYSQPFYTGYFGYKMCARVYLNGDGMGKGTHLSLFFVIMRGEYDALLPWPFKQKVTLMLMDQGSSRRHLGDAFKPDPNSSSFKKPTGEMNIASGCPVFVAQTVLENGTYIKDDTIFIKVIVDTSDLPDP'
    PS2 = 'MARPHPWWLCVLGTLVGLSATPAPKSCPERHYWAQGKLCCQMCEPGTFLVKDCDQHRKAAQCDPCIPGVSFSPDHHTRPHCESCRHCNSGLLVRNCTITANAECACRNGWQCRDKECTECDPLPNPSLTARSSQALSPHPQPTHLPYVSEMLEARTAGHMQTLADFRQLPARTLSTHWPPQRSLCSSDFIRILVIFSGMFLVFTLAGALFLHQRRKYRSNKGESPVEPAEPCRYSCPREEEGSTIPIQEDYRKPEPACSP'
    CC = corrcoef_of(PS1, PS2)
    print('CC=', CC.flatten().tolist())

if __name__=="__main__":
    main()
