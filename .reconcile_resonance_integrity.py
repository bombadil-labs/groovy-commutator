from pathlib import Path

p = Path('scripts/check_result_integrity.py')
text = p.read_text()
key = "'results/dimensional_resonance_response_20260912.json'"
if key not in text:
    block = """    'results/dimensional_resonance_response_20260912.json': {\n        'script': 'scripts/verify_dimensional_resonance_response.py',\n        'protocol': 'docs/research/protocols/dimensional-resonance-response-20260912.md',\n        'gate1_refreeze': 'docs/research/protocols/dimensional-resonance-response-gate1-refreeze-20260912.md',\n        'gate1_null_clarification': 'docs/research/protocols/dimensional-resonance-response-gate1-null-clarification-20260912.md',\n        'gate1_approval': 'docs/research/protocols/dimensional-resonance-response-gate1-approval-20260912.md',\n        'source_census_script': 'scripts/verify_dimensional_resonance_source_census.py',\n        'physical_predecessor_script': 'scripts/verify_interface_factor.py'},\n\n"""
    anchor = "\n}\n\ndef sha("
    if anchor not in text:
        raise SystemExit('integrity registry anchor not found')
    text = text.replace(anchor, "\n" + block + "}\n\ndef sha(", 1)
    p.write_text(text)
