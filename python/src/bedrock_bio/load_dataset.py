import duckdb
from duckdb import ColumnExpression, ConstantExpression

from .utils import get_catalog, get_connection


def load_dataset(name: str, **kwargs: object) -> duckdb.DuckDBPyRelation:
    """
    Lazily query a dataset.

    Parameters
    ----------
    name : str
        Dataset identifier (e.g. 'ukb_ppp.pqtls').
    **kwargs
        Equality filters applied to the table (e.g. ancestry='EUR').

    Returns
    -------
    duckdb.DuckDBPyRelation
        A lazy relation that can be further filtered, selected, or collected.

    Raises
    ------
    ConnectionError
        If the catalog cannot be accessed.
    KeyError
        If the dataset is not found in the catalog.

    Examples
    --------
    >>> import bedrock_bio as bb
    >>>
    >>> # load full table as a lazy relation
    >>> rel = bb.load_dataset('ukb_ppp.pqtls')
    >>>
    >>> # load with equality filters, then project and filter further
    >>> rel = bb.load_dataset('ukb_ppp.pqtls', ancestry='EUR', protein_id='A0FGR8')
    >>> rel = rel.select('chromosome, position, beta, neg_log_10_p_value')
    >>> rel = rel.filter('neg_log_10_p_value >= 8')
    >>> df = rel.fetchdf()

    """
    catalog = get_catalog()

    if name not in catalog:
        raise KeyError(
            f"Dataset '{name}' not found in catalog. "
            f"See list_datasets() for available datasets."
        )

    metadata_url = catalog[name]
    conn = get_connection()
    rel = conn.sql(f"SELECT * FROM iceberg_scan('{metadata_url}')")

    for key, value in kwargs.items():
        rel = rel.filter(ColumnExpression(key) == ConstantExpression(value))

    return rel
