# Contributing

## Prerequisites

- **Node.js** ≥ 20
- **Python** 3
- **GSD CLI** installed globally

## Development Setup

```bash
git clone https://github.com/qazmaster/gsd-ui-consistency-extension.git
cd gsd-ui-consistency-extension

# Install Node dependencies
npm install

# Type-check the extension
npx tsc --noEmit

# Test without installing
gsd -e .

# Or install locally
./install.sh
```

## Running Tests

```bash
cd skills/ui-consistency/tests
python3 run_all_tests.py
```

## Adding Tests

When adding new features, add corresponding tests to `skills/ui-consistency/tests/`:

1. Create `test_your_feature.py`
2. Add it to `run_all_tests.py` TESTS list
3. Run the full suite to verify

## Release Checklist

- [ ] All tests pass (`python3 run_all_tests.py`)
- [ ] Version bumped in `package.json` and `extension-manifest.json`
- [ ] `CHANGELOG.md` updated
- [ ] Git tag created (`git tag v1.x.x`)
