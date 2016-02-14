from django.db import models

from sequencing.runs.models import MergedReads
from targeted_enrichment.unwrapping.models import Unwrapper


### -------------------------------------------------------------------------------------
class SequencingData(models.Model): # This contains the actual data.
    merged_reads = models.ForeignKey(MergedReads)
    unwrapper = models.ForeignKey(Unwrapper)
    target_offset = models.IntegerField(null=True)
    fastq = models.FilePathField(null=True)
    vcf = models.FilePathField(null=True)

    class Meta:
        index_together = (
            ("cell_content", "merged_reads", "target"),
        )
