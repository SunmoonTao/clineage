import pytest

from targeted_enrichment.reagents.models import PCR1PrimerPairTER

from tests.targeted_enrichment.planning.conftest import *
from tests.targeted_enrichment.amplicons.conftest import *
from tests.primers.synthesis.conftest import *


@pytest.fixture()
def ter_28727(te_28727, primer_28727_left, primer_28727_right, pu_28727):
    ter = PCR1PrimerPairTER.objects.create(
        te=te_28727,
        passed_validation=False,
        left_primer=primer_28727_left,
        right_primer=primer_28727_right,
        amplicon=pu_28727,
    )
    # So our objects don't have "special" objects in fields
    ter = PCR1PrimerPairTER.objects.get(pk=ter.pk)
    return ter


@pytest.fixture()
def ter_28734(te_28734, primer_28734_left, primer_28734_right, pu_28734):
    ter = PCR1PrimerPairTER.objects.create(
        te=te_28734,
        passed_validation=True,
        left_primer=primer_28734_left,
        right_primer=primer_28734_right,
        amplicon=pu_28734,
    )
    # So our objects don't have "special" objects in fields
    ter = PCR1PrimerPairTER.objects.get(pk=ter.pk)
    return ter
