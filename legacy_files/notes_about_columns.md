### Some notes about columns in curated:
- some columns don't have NA values, instead some other alternative for when value not there (like control). Need to make a mark of these columns for cases when such information is not there.
- some columns need a very careful look into the sentence-meaning matching entries for it, (eg- target_condition, disease).
- don't have to worry about the ontology-term-columns because their information can be derived from the columns they are for, if those columns have been filled correctly.
- some columns are of text type, but still they have some categorical nature (eg- disease, treatment)
    - feces_phenotype_value should be int. Make sure.

### Options for remaining cols
- consider storing in unmetadata col
- consider removing

# Other, skeptical possiblities
- if can be joined into existing cols (skeptical about this)
- some columns also need more careful column mapped to them than others (like treatment), because we expect generally expect such a column from studies
