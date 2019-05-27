# First, parse a string to create a SpaCy Doc object
import en_core_web_sm

text = 'We introduce efficient methods for fitting Boolean models to molecular data, successfully demonstrating their application to synthetic time courses generated by a number of established clock models, as well as experimental expression levels measured using luciferase imaging.'
nlp = en_core_web_sm.load()
doc = nlp(text)

from role_pattern_nlp import RolePatternBuilder

pos_example = {
    'prep': [doc[4]],  # [for]
    'arg': [doc[7]],  # [models]
}
neg_examples = [{
    'prep': [doc[8]],  # [to]
    'arg': [doc[10]],  # [data]
}]

feature_dict = {'DEP': 'dep_', 'TAG': 'tag_', 'LOWER': 'lower_'}
role_pattern_builder = RolePatternBuilder(feature_dict)
pattern = role_pattern_builder.build(
    doc, pos_example, features=['DEP']
)
matches = pattern.match(doc)

# Our pattern matches both the pos_example and neg_examples
assert pos_example in matches
assert neg_examples[0] in matches

# RolePatternBuilder.refine() yields pattern variants that match the pos_example but not the neg_examples
role_pattern_variants = role_pattern_builder.refine(doc, pattern, pos_example, neg_examples)
for role_pattern_variant in role_pattern_variants:
    matches = role_pattern_variant.match(doc)
    assert pos_example in matches
    assert neg_examples[0] not in matches
