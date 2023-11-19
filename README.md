# knowledgestream-graph-transformer
This transformation script transforms a knowledge graph into a format used in the knowledge stream repository.

The packages needs modules like rdflid and numpy.

In knowledgestream, The knowledge graph has to be in a specific format. This script accepts A knowledge graph in turtle format, such as is provided by DBpedia. THe transformation process is straightforward:

`
python Transformer.py -g /source_file_of_the_kg -o ./output_directory
`
