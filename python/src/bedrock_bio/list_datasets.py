import httpx


def list_datasets() -> list[str]:
    """
    List available datasets in the Bedrock Bio library.

    Returns
    -------
    list[str]
        A list of dataset names.

    Raises
    ------
    ConnectionError
        If the catalog 'https://data.bedrock.bio/catalog.json' cannot be accessed.

    Examples
    --------
    >>> import bedrock_bio as bb
    >>> bb.list_datasets()
    ['ukb_ppp/pqtls', ...]

    """
    catalog_url = "https://data.bedrock.bio/catalog.json"

    try:
        response = httpx.get(catalog_url)
        response.raise_for_status()
    except Exception:
        raise ConnectionError(
            f"Unable to access catalog URL '{catalog_url}'. "
            "Check internet connection and try again."
        )
    else:
        return response.json()["datasets"]
