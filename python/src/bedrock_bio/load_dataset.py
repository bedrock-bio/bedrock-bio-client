import duckdb

from .config import config


def load_dataset(name: str, **filters: str) -> duckdb.DuckDBPyRelation:
    """
    Lazily query a dataset.

    Parameters
    ----------
    name : str
        Dataset identifier (e.g. 'ukb_ppp.pqtls').
    **filters : str
        Required partition filters (e.g. ancestry='EUR', protein_id='A0FGR8').

    Returns
    -------
    duckdb.DuckDBPyRelation
        A lazy relation that can be further filtered, selected, or collected.

    Raises
    ------
    ConnectionError
        If the catalog cannot be accessed.
    ValueError
        If the dataset is not found, required filters are missing,
        unknown filters are passed, or filter values are invalid.

    Examples
    --------
    >>> import bedrock_bio as bb
    >>>
    >>> rel = bb.load_dataset('ukb_ppp.pqtls', ancestry='EUR', protein_id='A0FGR8', panel='Inflammation')
    >>> rel = rel.select('chromosome, position, beta, neg_log_10_p_value')
    >>> df = rel.fetchdf()

    """
    catalog = config.get_catalog()

    if name not in catalog:
        raise ValueError(
            f"Dataset '{name}' not found in catalog. "
            f"See list_datasets() for available datasets."
        )

    entry = catalog[name]
    required = entry["required_filters"]
    allowed_values = entry["allowed_values"]

    missing = [f for f in required if f not in filters]
    if missing:
        raise ValueError(
            f"Missing required filters for '{name}': {', '.join(missing)}. "
            f"Required: {', '.join(required)}."
        )

    unknown = [f for f in filters if f not in required]
    if unknown:
        raise ValueError(
            f"Unknown filters for '{name}': {', '.join(unknown)}. "
            f"Valid filters: {', '.join(required)}."
        )

    coerced = {}
    for col, val in filters.items():
        val = str(val).strip()
        if col in allowed_values:
            allowed = allowed_values[col]
            if val not in allowed:
                lookup = {v.lower(): v for v in allowed}
                val = lookup.get(val.lower())
                if not val:
                    raise ValueError(
                        f"Invalid value '{str(filters[col]).strip()}' for filter '{col}'. "
                        f"Allowed: {', '.join(allowed)}."
                    )
        coerced[col] = val

    conn = config.get_connection()
    rel = conn.sql(f"SELECT * FROM iceberg_scan('{entry['metadata_json']}')")

    for col, val in coerced.items():
        safe_val = val.replace("'", "''")
        rel = rel.filter(f"{col} = '{safe_val}'")

    return rel
