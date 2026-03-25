from .config import config


def describe_dataset(name: str) -> dict:
    """
    Describe a dataset's metadata, citation, and columns.

    Parameters
    ----------
    name : str
        Dataset identifier (e.g. 'ukb_ppp.pqtls').

    Returns
    -------
    dict
        Dataset metadata including description, citation, source_url,
        license, and column definitions.

    Raises
    ------
    ConnectionError
        If the catalog cannot be accessed.
    ValueError
        If the dataset is not found in the catalog.

    Examples
    --------
    >>> import bedrock_bio as bb
    >>> info = bb.describe_dataset('ukb_ppp.pqtls')
    >>> info['name']
    'ukb_ppp.pqtls'

    """
    catalog = config.get_catalog()

    if name not in catalog:
        raise ValueError(
            f"Dataset '{name}' not found in catalog. "
            f"See list_datasets() for available datasets."
        )

    entry = catalog[name]
    return {
        "name": name,
        "description": entry["description"],
        "citation": entry["citation"],
        "source_url": entry["source_url"],
        "license": entry["license"],
        "columns": entry["columns"],
    }
