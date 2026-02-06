import httpx
import polars as pl


def load_dataset(name: str) -> pl.LazyFrame:
    """
    Lazily read a dataset from the Bedrock Bio library.

    Parameters
    ----------
    name : str
        Dataset name (e.g. 'ukb_ppp/pqtls').

    Returns
    -------
    pl.LazyFrame
        A lazy data frame that can be filtered and collected.

    Raises
    ------
    ConnectionError
        If the dataset manifest cannot be accessed.

    Examples
    --------
    >>> import bedrock_bio as bb
    >>>
    >>> # load into lazy data frame
    >>> lf = bb.load_dataset('ukb_ppp/pqtls')
    >>>
    >>> # filter rows, select columns, collect as data frame
    >>> df = lf \\
    ...     .filter(
    ...         pl.col('ancestry') == 'EUR',
    ...         pl.col('protein') == 'A0FGR8'
    ...     ) \\
    ...     .select(
    ...         'chromosome',
    ...         'position',
    ...         'effect_allele',
    ...         'other_allele',
    ...         'beta',
    ...         'neg_log_10_p_value'
    ...     ) \\
    ...     .collect()

    """
    base_url = "https://data.bedrock.bio"
    manifest_url = f"{base_url}/{name}/manifest.json"

    try:
        response = httpx.get(manifest_url)
        response.raise_for_status()
    except Exception:
        raise ConnectionError(
            f"Unable to access manifest '{manifest_url}' for dataset '{name}'. "
            "Check internet connection and try again."
        )
    else:
        files = response.json()["files"]

    urls = [f"{base_url}/{file}" for file in files]

    return pl.scan_parquet(urls, hive_partitioning=True)
