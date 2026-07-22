# Name-to-Nationality Prediction

Two separate models are trained — one for first names, one for last names — to predict a person's likely cultural origin from their name alone.

## Repository Structure

Paths below are relative to the repo root.

```
├── data/final_project/qicheng-lee/
│   └── raw/
│       └── name_dataset.zip              # Source dataset (~4.7M names, 105 countries) - gitignored, see "Reproducing" below
└── notebooks/hw/final_project/qicheng-lee/
    ├── name-dataset.ipynb                # Main notebook: data prep, training, evaluation
    ├── name_dataset_cache_50000.pkl      # Pickled/filtered dataset cache - gitignored, auto-rebuilt from the zip on first run
    ├── rnn_firstname_nat.pth             # Trained first name model weights (committed)
    ├── rnn_lastname_nat.pth              # Trained last name model weights (committed)
    └── README_name2nat.md                # This file
```

## References

- [Name Dataset](https://github.com/philipperemy/name-dataset) — source of the ~4.7 million first/last name records across 105 countries
- [name2nat](https://github.com/Kyubyong/name2nat) — prior work on name-to-nationality prediction
- [PyTorch RNN/LSTM/GRU notebook](https://www.kaggle.com/code/sharanharsoor/pytorch-rnn-lstm-gru) — basis for the model architecture

## Reproducing: Getting the Raw Dataset

`data/final_project/qicheng-lee/raw/name_dataset.zip` is not tracked in git (see `.gitignore`). To reproduce the notebook from scratch:

1. Download `name_dataset.zip` from Google Drive: https://drive.google.com/file/d/1QDbtPWGQypYxiS4pC_hHBBtbRHk9gEtr/view
2. Save it to `data/final_project/qicheng-lee/raw/name_dataset.zip` (create the `raw/` folder if it doesn't exist).
3. Delete any stale `notebooks/hw/final_project/qicheng-lee/name_dataset_cache_*.pkl` file if present, so the notebook rebuilds the cache from the zip instead of reusing an old one.
4. Run `name-dataset.ipynb` top to bottom (Restart & Run All) — the first cell load will take a few minutes and will regenerate the pickle cache.

## Data

The dataset contains ~4.7 million names drawn from 105 countries. Because many countries share naming conventions, the 105 countries are consolidated into **23 nationality groups** organized by how distinctive their naming patterns are.

### Tier 1 — Highly distinctive names

These nationalities have naming patterns unique enough that they rarely get confused with others.

| Group | Example patterns |
|---|---|
| Japanese (JP) | Syllabic CV patterns: -mura, -moto, -kawa (Tanaka, Suzuki) |
| Korean (KR) | Very short, limited surname set (Kim, Park, Choi) |
| Chinese (CN) | Short, distinctive romanizations (Wang, Li, Zhang) |
| Finnish (FI) | Double vowels, -nen endings (Virtanen, Korhonen) |
| Georgian (GE) | -shvili, -dze, -ia suffixes (Beridze, Kvirikashvili) |
| Greek (GR) | -opoulos, -idis, -akis (Papadopoulos, Nikolaidis) |
| Hungarian (HU) | sz, gy, cs clusters (Kovacs, Szabo, Nagy) |
| Icelandic (IS) | Patronymic -son/-dottir, unique first names |

### Tier 2 — Distinctive with minor overlap

Still recognizable, but occasional confusion with neighboring traditions.

| Group | Example patterns |
|---|---|
| Polish (PL) | -ski, -wicz, -czyk, sz/cz clusters |
| Italian (IT) | Vowel-heavy, -ini, -elli, -ucci |
| French (FR) | Le-, Du-, -eux, -eau |
| Turkish (TR) | Vowel harmony patterns (includes Azerbaijan, Turkmenistan, Kazakhstan) |
| Persian (IR) | -zadeh, -pour, -nejad (includes Afghanistan) |
| Lithuanian (LT) | -auskas, -aitis, -unas |
| Indian (IN) | Singh, Patel, Kumar, -krishnan, -murthy |
| Nigerian (NG) | Yoruba/Igbo patterns like Okonkwo, Adeyemi (includes Ghana, Burkina Faso) |

### Tier 3 — Merged groups

Countries that share a language or naming tradition are grouped under one label.

| Group | Members |
|---|---|
| Spanish (ES) | Spain, Mexico, Colombia, Argentina, Peru, Chile, + 10 others |
| Portuguese (PT) | Portugal, Brazil, Angola |
| Arabic (SA) | Saudi Arabia, Egypt, Iraq, Syria, Jordan, Lebanon, + 13 others |
| English (GB) | UK, US, Canada, Ireland, Jamaica |
| Nordic (SE) | Sweden, Denmark, Norway |
| Slavic (CZ) | Czechia, Croatia, Serbia, Slovenia, Bulgaria, Russia |
| Germanic (GM) | Germany, Netherlands |

24 countries whose names don't map cleanly to any single group (e.g., Belgium, Singapore, Philippines) are dropped. After filtering, ~3.7 million names remain, split 80/20 into training and test sets.

## How the Model Works

The model reads a name **one letter at a time**, building up an internal summary of what it has seen so far. After processing the last letter, it outputs a probability for each of the 23 nationalities. Think of it like a person scanning a name left to right — the ending "-ovich" might suggest Slavic, while "-moto" might suggest Japanese. The model learns these patterns automatically from millions of examples rather than from hand-written rules.

Because some nationalities have far more examples than others (Arabic names outnumber Korean names ~100:1), the training process **upweights underrepresented groups** so the model doesn't simply learn to guess "Arabic" for everything.

## Accuracy

| Metric | Last Name Model | First Name Model |
|---|---|---|
| Top-1 accuracy (exact match) | **60%** | **50%** |
| Top-2 accuracy (correct in top 2 guesses) | **73%** | **64%** |

Last names are more predictive than first names — first names are more likely to cross cultural boundaries (e.g., "Maria" appears in Spanish, Italian, Portuguese, and other traditions).

### Confidence Calibration

The model's self-reported confidence aligns well with actual accuracy. When the last name model says it is 90% confident, it is correct ~86% of the time. When it says 30%, it is correct ~34% of the time. The confidence score is a reliable indicator of prediction quality.

## Key Limitations

- **Shared naming traditions** across nationality groups (e.g., English vs. Germanic) cause confusion — the models work best for Tier 1 and Tier 2 names with distinctive patterns.
- **First names travel across cultures** more than last names, which is why the first-name model is less accurate.
- **Low-sample groups** like Korean (~8,000 examples vs. ~900,000 for Arabic) are harder to predict reliably despite upweighting.
- The model predicts **cultural/linguistic origin of the name**, not necessarily the person's actual nationality or ethnicity.
