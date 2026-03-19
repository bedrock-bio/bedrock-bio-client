from .utils import get_catalog


def list_datasets() -> list[str]:
    """
    List available datasets in the Bedrock Bio library.

    Returns
    -------
    list[str]
        A list of dataset identifiers (e.g. 'ukb_ppp.pqtls').

    Raises
    ------
    ConnectionError
        If the catalog cannot be accessed.

    Examples
    --------
    >>> import bedrock_bio as bb
    >>> bb.list_datasets()
    ['ukb_ppp.pqtls', ...]

    """
    catalog = get_catalog()
    return list(catalog.keys())
