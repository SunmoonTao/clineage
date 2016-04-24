import pytest


@pytest.mark.django_db
def test_dnabarcode1(dnabarcode1):
    assert dnabarcode1.ref_sequence.seq == b"TCCGCGAA"


@pytest.mark.django_db
def test_dnabarcode2(dnabarcode2):
    assert dnabarcode2.ref_sequence.seq == b"GTACTGAC"


@pytest.mark.django_db
def test_illuminareadingadaptor1(illuminareadingadaptor1):
    assert illuminareadingadaptor1.ref_sequence.seq == b"ACACTCTTTCCCTACACGACGCTCTTCCGATCT"


@pytest.mark.django_db
def test_illuminareadingadaptor1(illuminareadingadaptor2):
    assert illuminareadingadaptor2.ref_sequence.seq == b"AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC"


@pytest.mark.django_db
def test_illuminareadingadaptor1cuts_numbers(illuminareadingadaptor1cuts):
    assert illuminareadingadaptor1cuts.overlap_start == 11
    assert illuminareadingadaptor1cuts.overlap_end == 33


@pytest.mark.django_db
def test_illuminareadingadaptor2cuts_numbers(illuminareadingadaptor2cuts):
    assert illuminareadingadaptor2cuts.overlap_start == 12
    assert illuminareadingadaptor2cuts.overlap_end == 34


@pytest.mark.django_db
def test_illuminareadingadaptor1cuts_primer1tail(illuminareadingadaptor1cuts):
    assert illuminareadingadaptor1cuts.primer1tail.seq == b"CTACACGACGCTCTTCCGATCT"


@pytest.mark.django_db
def test_illuminareadingadaptor2cuts_primer1tail(illuminareadingadaptor2cuts):
    assert illuminareadingadaptor2cuts.primer1tail.seq == b"CAGACGTGTGCTCTTCCGATCT"
