# Journey

Notes on how this tool evolved, the decisions made along the way, trade-offs taken, and
concepts learned while building it.

## Milestones

1. **Read a file path via `sys.argv`** — first pass just validated a CSV path was
   provided.
2. **Switch to `argparse`** — replaced manual `sys.argv` handling with `argparse` for
   proper usage/help text and argument validation.
3. **Load into pandas, print to console** — `FileReader.get_data()` returns a
   `DataFrame` via `pd.read_csv`.
4. **MVP 1 — fix nulls in string columns only** — interactive prompt per column asking
   for a fill value, defaulting to `"undefined"` if skipped.
5. **MVP 2 — handle numeric columns too** — added mean / median / custom-value options
   for numeric columns.
6. **Refactor to non-interactive auto-fill** — replaced per-column prompts with a fixed
   default strategy (`"undefined"` for strings, `0` for numbers) and a `summary`
   property that reports what changed, why, and the resulting `DataFrame.describe()`.

## Decisions & trade-offs

- **Non-interactive over interactive prompts.** Early versions asked the user for a
  fill value per null column. Simpler to reason about and testable end-to-end without
  stdin wrangling, at the cost of losing per-column control — every string column gets
  `"undefined"`, every numeric column gets `0`, regardless of what makes sense for that
  column (e.g. `mean` might suit a `sleep_hours` column better than `0`).
- **`data.copy()` for the working frame, keep `__original_data` untouched.** Needed so
  the `summary` property can diff before/after null counts without re-reading the file.
- **`pd.api.types.is_string_dtype` / `is_numeric_dtype` over `dtype == "str"`.** The
  literal string comparison only worked because pandas 3.0 infers a `StringDtype` whose
  `dtype` reprs as `"str"` — it would silently break on older pandas or any
  non-default dtype. The `pd.api.types.*` helpers are the dtype-agnostic way to ask
  "is this string-like / numeric-like".
- **`unique()` + `str.join` needs an explicit cast.** `Series.unique()` returns a raw
  array that can mix real values with `NaN` (a `float`). `", ".join(...)` requires
  every item to already be `str`, so `NaN` blows it up — `map(str, values)` (or
  `.astype(str)`) is required before joining.

## Bugs found & fixed along the way

- **`before`/`after` DataFrame with mismatched lengths.** An earlier version built a
  before/after report from two `unique()` arrays — but filling nulls removes `NaN` as a
  unique value, so the arrays differed in length and `pd.DataFrame({...})` raised
  `ValueError`. Resolved by switching the summary to aggregate counts
  (`isna().sum()`) instead of raw unique-value arrays.
- **Skipped input never fell back to `"undefined"`.** The prompt text promised a
  default but the fill only ran when the user typed something — fixed by adding an
  explicit `else` branch.
- **`option == 1` never matched.** `input()` always returns a `str`, so comparing it to
  an `int` silently fell through to the "unrecognized option" branch every time —
  a reminder that CLI input needs explicit casting before comparison. (This applied to
  the interactive numeric-option flow before it was replaced by the current
  auto-fill approach.)

## Concepts used / learnt

- pandas dtype introspection (`pd.api.types.is_string_dtype`, `is_numeric_dtype`) vs.
  brittle literal dtype comparisons.
- pandas 3.0's default string-inference behaviour and how it changes `dtype` reprs
  compared to earlier pandas versions (`object` vs. `StringDtype`).
- Why `Series.unique()` is not the same as `Series` — it drops the pandas wrapper, so
  `NaN` shows up as a plain `float` and vectorised string ops (`.str.*`) aren't
  available on it directly.
- `DataFrame.isna().sum()` as the standard way to count/report missing data per column.
- Structuring a small CLI package with `#region`/`#endregion`-style public/private
  method grouping and name-mangled (`__attr`) instance state.
