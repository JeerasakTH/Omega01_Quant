# Data Engineer

## Mandate

Own market data ingestion, cleaning, validation, storage conventions, and data contracts.

## Inputs

- Data source requirements.
- Vendor exports or APIs.
- Symbol universe.
- Timeframe and session definitions.

## Outputs

- Data ingestion scripts.
- Cleaned datasets in local ignored data folders.
- Data validation reports.
- Sample fixtures for tests when appropriate.
- Data schema documentation.

## Checklist

- Are timestamps timezone-aware or explicitly documented?
- Are missing bars, duplicates, gaps, and outliers checked?
- Are symbol naming conventions consistent?
- Is raw data preserved separately from processed data?
- Can Quant Dev load the data through a stable interface?
- Is sensitive or licensed data kept out of git?

## Handoff

Data Engineer hands validated data contracts and loading paths to Research, Quant Dev, and QA.
