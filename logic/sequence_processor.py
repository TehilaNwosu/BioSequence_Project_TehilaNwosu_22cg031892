# logic/sequence_processor.py

# --- Codon Table (mRNA codons → Amino Acids) ---
CODON_TABLE = {
    "UUU": ("Phe", "F"), "UUC": ("Phe", "F"),
    "UUA": ("Leu", "L"), "UUG": ("Leu", "L"),
    "UCU": ("Ser", "S"), "UCC": ("Ser", "S"), "UCA": ("Ser", "S"), "UCG": ("Ser", "S"),
    "UAU": ("Tyr", "Y"), "UAC": ("Tyr", "Y"),
    "UAA": ("Stop", "*"), "UAG": ("Stop", "*"), "UGA": ("Stop", "*"),
    "UGU": ("Cys", "C"), "UGC": ("Cys", "C"),
    "UGG": ("Trp", "W"),
    "CUU": ("Leu", "L"), "CUC": ("Leu", "L"), "CUA": ("Leu", "L"), "CUG": ("Leu", "L"),
    "CCU": ("Pro", "P"), "CCC": ("Pro", "P"), "CCA": ("Pro", "P"), "CCG": ("Pro", "P"),
    "CAU": ("His", "H"), "CAC": ("His", "H"),
    "CAA": ("Gln", "Q"), "CAG": ("Gln", "Q"),
    "CGU": ("Arg", "R"), "CGC": ("Arg", "R"), "CGA": ("Arg", "R"), "CGG": ("Arg", "R"),
    "AUU": ("Ile", "I"), "AUC": ("Ile", "I"), "AUA": ("Ile", "I"),
    "AUG": ("Met", "M"),
    "ACU": ("Thr", "T"), "ACC": ("Thr", "T"), "ACA": ("Thr", "T"), "ACG": ("Thr", "T"),
    "AAU": ("Asn", "N"), "AAC": ("Asn", "N"),
    "AAA": ("Lys", "K"), "AAG": ("Lys", "K"),
    "AGU": ("Ser", "S"), "AGC": ("Ser", "S"),
    "AGA": ("Arg", "R"), "AGG": ("Arg", "R"),
    "GUU": ("Val", "V"), "GUC": ("Val", "V"), "GUA": ("Val", "V"), "GUG": ("Val", "V"),
    "GCU": ("Ala", "A"), "GCC": ("Ala", "A"), "GCA": ("Ala", "A"), "GCG": ("Ala", "A"),
    "GAU": ("Asp", "D"), "GAC": ("Asp", "D"),
    "GAA": ("Glu", "E"), "GAG": ("Glu", "E"),
    "GGU": ("Gly", "G"), "GGC": ("Gly", "G"), "GGA": ("Gly", "G"), "GGG": ("Gly", "G"),
}

DNA_COMPLEMENT = {"A": "T", "T": "A", "C": "G", "G": "C"}
RNA_COMPLEMENT = {"A": "U", "U": "A", "C": "G", "G": "C"}


def validate_sequence(sequence):
    """Clean and validate the input sequence."""
    sequence = sequence.upper().strip().replace(" ", "").replace("\n", "")
    valid_chars = set("ATCGU")
    invalid = set(sequence) - valid_chars
    if invalid:
        raise ValueError(f"Invalid characters found: {', '.join(invalid)}")
    has_T = "T" in sequence
    has_U = "U" in sequence
    if has_T and has_U:
        raise ValueError("Sequence contains both T and U — cannot be DNA or RNA.")
    return sequence


def detect_type(sequence):
    """Detect whether sequence is DNA or RNA."""
    if "U" in sequence:
        return "RNA"
    return "DNA"


def transcribe(sequence, seq_type):
    """Transcribe DNA to mRNA or RNA to DNA template."""
    if seq_type == "DNA":
        return sequence.replace("T", "U")  # DNA → mRNA
    else:
        return sequence.replace("U", "T")  # RNA → DNA template


def get_complement(sequence, seq_type):
    """Generate the complement strand."""
    table = DNA_COMPLEMENT if seq_type == "DNA" else RNA_COMPLEMENT
    return "".join(table.get(base, "?") for base in sequence)


def get_reverse_complement(sequence, seq_type):
    """Generate the reverse complement strand."""
    return get_complement(sequence, seq_type)[::-1]


def translate(mrna):
    """Translate mRNA sequence into a protein sequence."""
    one_letter = []
    three_letter = []

    # Trim to nearest codon
    trimmed = mrna[:len(mrna) - (len(mrna) % 3)]

    for i in range(0, len(trimmed), 3):
        codon = trimmed[i:i+3]
        amino = CODON_TABLE.get(codon, ("???", "?"))
        if amino[0] == "Stop":
            break
        three_letter.append(amino[0])
        one_letter.append(amino[1])

    return "".join(one_letter), "-".join(three_letter)


def analyze_sequence(raw_sequence):
    """Main function — runs the full analysis pipeline."""
    sequence = validate_sequence(raw_sequence)
    seq_type = detect_type(sequence)
    transcribed = transcribe(sequence, seq_type)
    complement = get_complement(sequence, seq_type)
    reverse_complement = get_reverse_complement(sequence, seq_type)

    # Translation always uses mRNA
    mrna = transcribed if seq_type == "DNA" else sequence
    protein_1, protein_3 = translate(mrna)

    return {
        "sequence": sequence,
        "type": seq_type,
        "transcribed": transcribed,
        "complement": complement,
        "reverse_complement": reverse_complement,
        "mrna": mrna,
        "protein_1letter": protein_1,
        "protein_3letter": protein_3,
    }