
from django.contrib.contenttypes import fields
from django.db import models
from primers.synthesis.models import PCR1PlusPrimer, PCR1MinusPrimer, TargetedNoTailPlusPrimer, TargetedNoTailMinusPrimer
from targeted_enrichment.planning.models import TargetEnrichment

from wet_storage.models import SampleLocation

class TargetEnrichmentFailureType(models.Model):
    """
    1 = No product
    2 = Primer dimer is wider, equal or  close to the same band width of expected product
    3 = Smear or more than 3 products  (other than the primer dimer which can be purified). If less than 3, real product
        has to be wider than byproducts.
    4 = More than 1 product is in the range of correct size.
    5 = NGS failure - Primer pair did not work in the context of a successful NGS run (amplified and sequenced).
    """
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name

class TargetedEnrichmentReagent(models.Model):
    te = models.ForeignKey(TargetEnrichment)
    passed_validation = models.NullBooleanField()
    validation_failure = models.ForeignKey(TargetEnrichmentFailureType, null=True)
    validation_date = models.DateField(null=True, blank=True)
    comment = models.CharField(max_length=50, blank=True, null=True)
    physical_locations = fields.GenericRelation(SampleLocation,
                                                 content_type_field='content_type',
                                                 object_id_field='object_id')

    class Meta:
        abstract = True


class PCR1PrimerPairTER(TargetedEnrichmentReagent):
    left_primer = models.ForeignKey(PCR1PlusPrimer)
    right_primer = models.ForeignKey(PCR1MinusPrimer)


class TargetedNoTailPrimerPairTER(TargetedEnrichmentReagent):
    left_primer = models.ForeignKey(TargetedNoTailPlusPrimer)
    right_primer = models.ForeignKey(TargetedNoTailMinusPrimer)


class PCR1PrimerPairTERDeprecated(TargetedEnrichmentReagent): #TODO: kill?
    left_primer = models.ForeignKey(PCR1PlusPrimer)
    right_primer = models.ForeignKey(PCR1MinusPrimer)

