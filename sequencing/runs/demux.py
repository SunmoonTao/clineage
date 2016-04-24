
from plumbum import local
import itertools
import csv
import io


SAMPLESHEET_HEADERS = [
"Sample_ID",
"Sample_Name",
"Sample_Plate",
"Sample_Well",
"I7_Index_ID",
"index",
"I5_Index_ID",
"index2",
"Sample_Project",
"Description",
]

HEADER_FORMAT = \
"""[Header],,,,,,,,,
IEMFileVersion,4,,,,,,,,
Experiment Name,{run_name},,,,,,,,
Date,{run_date},,,,,,,,
Workflow,GenerateFASTQ,,,,,,,,
Application,FASTQ Only,,,,,,,,
Assay,TruSeq HT,,,,,,,,
Description,{run_desc},,,,,,,,
Chemistry,Amplicon,,,,,,,,
,,,,,,,,,
[Reads],,,,,,,,,
{read_length},,,,,,,,,
{read_length},,,,,,,,,
,,,,,,,,,
[Settings],,,,,,,,,
ReverseComplement,0,,,,,,,,
Adapter,{fwd_read_adaptor},,,,,,,,
AdapterRead2,{rev_read_adaptor},,,,,,,,
,,,,,,,,,
[Data],,,,,,,,,
"""


def run_bcl2fastq(bcl_folder, sample_sheet_path):
    bcl2fastq = local["bcl2fastq"]
    bcl2fastq_with_defaults = bcl2fastq["--no-lane-splitting",
                                            "--processing-threads", 20]
    bcl2fastq_with_defaults(
        "--runfolder-dir", bcl_folder,
        "--sample-sheet", sample_sheet_path)

def _rows_iter(bcs):
    for bc in bcs:
        yield {
            "Sample_ID": bc.id,
            "Sample_Name": bc.id,
            "I7_Index_ID": bc.barcodes.left.name,
            "index": bc.barcodes.left.sequence,
            "I5_Index_ID": bc.barcodes.right.name,
            "index2": bc.barcodes.right.sequence,  # Or ref_seq?
        }

def generate_sample_sheets(barcodes, name, date, description, read_length, fwd_read_adaptor, rev_read_adaptor, demux_scheme, max_samples=None):
        out = []
        rows = _rows_iter(barcodes)
        while True:
            sio = io.StringIO()
            sio.write(HEADER_FORMAT.format(
                run_name=name,
                run_date=date,
                run_desc=description,
                read_length=read_length,
                fwd_read_adaptor=fwd_read_adaptor,
                rev_read_adaptor=rev_read_adaptor,
            ))
            w = csv.DictWriter(sio, fieldnames=SAMPLESHEET_HEADERS)
            w.writeheader()
            if max_samples is None:
                for row in rows:
                    w.writerow(row)
                b = sio.getvalue()
                sio.close()
                return b
            else:
                row = None
                for row in itertools.islice(rows, max_samples):
                    w.writerow(row)
                if row is None:
                    return out
            out.append(sio.getvalue())
            sio.close()



# [dcsoft@n71 ~]$ bcl2fastq --help
# BCL to FASTQ file converter
# bcl2fastq v2.16.0.10
# Copyright (c) 2007-2015 Illumina, Inc.
#
# 2016-02-14 12:11:44 [1363880] Command-line invocation: bcl2fastq --help
# 2016-02-14 12:11:44 [1363880] INFO: Minimum log level: INFO
# 2016-02-14 12:11:44 [1363880] INFO: Runfolder path: '/home/dcsoft/'
# 2016-02-14 12:11:44 [1363880] INFO: Input path: '/home/dcsoft/Data/Intensities/BaseCalls/'
# 2016-02-14 12:11:44 [1363880] INFO: Intensities path: '/home/dcsoft/Data/Intensities/'
# 2016-02-14 12:11:44 [1363880] INFO: Output path: '/home/dcsoft/Data/Intensities/BaseCalls/'
# 2016-02-14 12:11:44 [1363880] INFO: InterOp path: '/home/dcsoft/InterOp/'
# 2016-02-14 12:11:44 [1363880] INFO: Stats path: '/home/dcsoft/Data/Intensities/BaseCalls/Stats/'
# 2016-02-14 12:11:44 [1363880] INFO: Reports path: '/home/dcsoft/Data/Intensities/BaseCalls/Reports/'
# 2016-02-14 12:11:44 [1363880] INFO: Detected CPUs: 40
# 2016-02-14 12:11:44 [1363880] INFO: Loading threads: 4
# 2016-02-14 12:11:44 [1363880] INFO: Processing threads: 40
# 2016-02-14 12:11:44 [1363880] INFO: Demultiplexing threads: 8
# 2016-02-14 12:11:44 [1363880] INFO: Writing threads: 4
# 2016-02-14 12:11:44 [1363880] INFO: Aggregated tiles: AUTO
# 2016-02-14 12:11:44 [1363880] INFO: Allowed barcode mismatches: 1
# 2016-02-14 12:11:44 [1363880] INFO: Tiles: <ALL>
# 2016-02-14 12:11:44 [1363880] INFO: Minimum trimmed read length: 35
# 2016-02-14 12:11:44 [1363880] INFO: Use bases masks: <NONE>
# 2016-02-14 12:11:44 [1363880] INFO: Mask short adapter reads: 22
# 2016-02-14 12:11:44 [1363880] INFO: Adapter stringency: 0.9
# 2016-02-14 12:11:44 [1363880] INFO: Ignore missing BCLs: NO
# 2016-02-14 12:11:44 [1363880] INFO: Ignore missing filters: NO
# 2016-02-14 12:11:44 [1363880] INFO: Ignore missing positions: NO
# 2016-02-14 12:11:44 [1363880] INFO: Ignore missing controls: NO
# 2016-02-14 12:11:44 [1363880] INFO: Include non-PF clusters: NO
# 2016-02-14 12:11:44 [1363880] INFO: Create FASTQs for index reads: NO
# 2016-02-14 12:11:44 [1363880] INFO: Use bgzf compression for FASTQ files: YES
# 2016-02-14 12:11:44 [1363880] INFO: FASTQ compression level: 4
# Usage:
#       bcl2fastq [options]
#
# Command-line options:
#   -h [ --help ]                                   produce help message and exit
#   -v [ --version ]                                print program version information
#   -l [ --min-log-level ] arg (=INFO)              minimum log level
#                                                   recognized values: NONE, FATAL, ERROR, WARNING, INFO, DEBUG, TRACE
#   -i [ --input-dir ] arg (=<runfolder-dir>/Data/Intensities/BaseCalls/)
#                                                   path to input directory
#   -R [ --runfolder-dir ] arg (=./)                path to runfolder directory
#   --intensities-dir arg (=<input-dir>/../)        path to intensities directory
#                                                   if intensities directory is specified, also input directory must be specified
#   -o [ --output-dir ] arg (=<input-dir>)          path to demultiplexed output
#   --interop-dir arg (=<runfolder-dir>/InterOp/)   path to demultiplexing statistics directory
#   --stats-dir arg (=<output-dir>/Stats/)          path to human-readable demultiplexing statistics directory
#   --reports-dir arg (=<output-dir>/Reports/)      path to reporting directory
#   --sample-sheet arg (=<runfolder-dir>/SampleSheet.csv)
#                                                   path to the sample sheet
#   --aggregated-tiles arg (=AUTO)                  tiles aggregation flag determining structure of input files
#                                                   recognized values:
#                                                     AUTO Try to detect correct setting
#                                                     YES  Tiles are aggregated into single input file
#                                                     NO   There are separate input files for individual tiles
#
#   -r [ --loading-threads ] arg (=4)               number of threads used for loading BCL data
#   -d [ --demultiplexing-threads ] arg             number of threads used for demultiplexing
#   -p [ --processing-threads ] arg                 number of threads used for processing demultiplexed data
#   -w [ --writing-threads ] arg (=4)               number of threads used for writing FASTQ data
#                                                   this must not be higher than number of samples
#   --tiles arg                                     Comma-separated list of regular expressions to select only a subset of the tiles available in the
#                                                   flow-cell. Multiple entries allowed, each applies to the corresponding base-calls.
#                                                   For example:
#                                                    * to select all the tiles ending with '5' in all lanes:
#                                                        --tiles [0-9][0-9][0-9]5
#                                                    * to select tile 2 in lane 1 and all the tiles in the other lanes:
#                                                        --tiles s_1_0002,s_[2-8]
#   --minimum-trimmed-read-length arg (=35)         minimum read length after adapter trimming
#   --use-bases-mask arg                            Specifies how to use each cycle.
#   --mask-short-adapter-reads arg (=22)            smallest number of remaining bases (after masking bases below the minimum trimmed read length) below which
#                                                   whole read is masked
#   --adapter-stringency arg (=0.9)                 adapter stringency
#   --ignore-missing-bcls                           assume 'N'/'#' for missing calls
#   --ignore-missing-filter                         assume 'true' for missing filters
#   --ignore-missing-positions                      assume [0,i] for missing positions, where i is incremented starting from 0
#   --ignore-missing-controls                       assume 0 for missing controls
#   --write-fastq-reverse-complement                Generate FASTQs containing reverse complements of actual data
#   --with-failed-reads                             include non-PF clusters
#   --create-fastq-for-index-reads                  create FASTQ files also for index reads
#   --no-bgzf-compression                           Turn off BGZF compression for FASTQ files
#   --fastq-compression-level arg (=4)              Zlib compression level (1-9) used for FASTQ files
#   --barcode-mismatches arg (=1)                   number of allowed mismatches per index
#                                                   multiple entries, comma delimited entries, allowed; each entry is applied to the corresponding index;last
#                                                   entry applies to all remaining indices
#   --no-lane-splitting                             Do not split fastq files by lane.
