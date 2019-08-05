from mendeley.exception import MendeleyException
from mendeley.models.dataset import *
from mendeley.resources.base import add_query_params, ListResource, GetByIdResource


class Datasets(GetByIdResource):
    """
    Top-level resource for accessing datasets.
    """
    _url = '/datasets'

    def __init__(self, session):
        self.session = session

    def get(self, id, view=None):
        """
        Retrieves a dataset by ID.

        :param id: the ID of the datasete to get.
        :param view: the view to get.  One of 'bib', 'client', 'stats', 'all'.
        :return: a :class:`datasetDocument <mendeley.models.Dataset.DatasetDocument>`.
        """
        return super(Dataset, self).get(id, view=view)

    def by_identifier(self, arxiv=None, doi=None, isbn=None, issn=None, pmid=None, scopus=None, filehash=None,
                      view=None):
        """
        Retrieves a dataset by an external identifier.  Only one identifier may be specified.

        :param arxiv: ArXiV ID.
        :param doi: DOI.
        :param isbn: ISBN.
        :param issn: ISSN.
        :param pmid: PubMed ID.
        :param scopus: Scopus ID (EID).
        :param filehash: SHA-1 filehash.
        :param view: the view to get.  One of 'bib', 'client', 'stats', 'all'.
        :return: a :class:`datasetDocument <mendeley.models.dataset.Dataset>`.
        """
        url = add_query_params('/dataset', {'arxiv': arxiv, 'doi': doi, 'isbn': isbn, 'issn': issn, 'pmid': pmid,
                                            'scopus': scopus, 'filehash': filehash, 'view': view})
        obj_type = view_type(view)

        rsp = self.session.get(url, headers={'Accept': obj_type.content_type})

        if len(rsp.json()) == 0:
            raise MendeleyException('dataset document not found')

        return obj_type(self.session, rsp.json()[0])

    def lookup(self, arxiv=None, doi=None, pmid=None, filehash=None, title=None, authors=None, year=None, source=None,
               view=None):
        """
        Finds the closest matching dataset document to a supplied set of metadata.

        :param arxiv: ArXiV ID.
        :param doi: DOI.
        :param pmid: PubMed ID.
        :param filehash: SHA-1 filehash.
        :param title: Title.
        :param authors: Authors.
        :param year: Year.
        :param source: Source.
        :param view: the view to get.  One of 'bib', 'client', 'stats', 'all'.
        :return: a :class:`Dataset <mendeley.models.dataset.Dataset>`.
        """
        url = add_query_params('/metadata', {'arxiv': arxiv, 'doi': doi, 'pmid': pmid, 'filehash': filehash,
                                             'title': title, 'authors': authors, 'year': year, 'source': source})
        obj_type = view_type(view)

        rsp = self.session.get(url, headers={'Accept': 'application/vnd.mendeley-document-lookup.1+json'})

        return LookupResponse(self.session, rsp.json(), view, obj_type)

    def search(self, query, view=None):
        """
        Searches the datasets for dataset.

        :param query: the search query to execute.
        :param view: the view to get.  One of 'bib', 'client', 'stats', 'all'.
        :return: a :class:`DatasetSearch <mendeley.resources.Dataset.DatasetSearch>` resource, from which results can be
                 retrieved.
        """
        return DatasetSearch(self.session, query=query, view=view)

    def advanced_search(self, title=None, author=None, source=None, abstract=None, min_year=None, max_year=None,
                        open_access=None, view=None):
        """
        Executes an advanced dataset search, where individual fields can be searched on.

        :param title: Title.
        :param author: Author.
        :param source: Source.
        :param abstract: Abstract.
        :param min_year: Minimum year for documents to return.
        :param max_year: Maximum year for documents to return.
        :param open_access: If 'true', only returns open access documents.
        :return: a :class:`DatasetSearch <mendeley.resources.Dataset.DatasetSearch>` resource, from which results can be
                 retrieved.
        """
        return DatasetSearch(self.session, title=title, author=author, source=source, abstract=abstract,
                             min_year=min_year, max_year=max_year, open_access=open_access)

    @property
    def _session(self):
        return self.session

    def _obj_type(self, **kwargs):
        return view_type(kwargs.get('view'))


class DatasetSearch(ListResource):
    """
    Resource for accessing the results of a dataset search.
    """
    def __init__(self, session, **kwargs):
        self.session = session
        self.params = kwargs

    def list(self, page_size=None):
        """
        Retrieves search results, as a paginated collection.

        :param page_size: the number of search results to return on each page.  Defaults to 20.
        :return: a :class:`Page <mendeley.pagination.Page>` of
                 :class:`DatasetDocuments <mendeley.models.Dataset.DatasetDocument>`.
        """
        return super(DatasetSearch, self).list(page_size)

    def iter(self, page_size=None):
        """
        Retrieves search results, as an iterator.

        :param page_size: the number of search results to retrieve at a time.  Defaults to 20.
        :return: an iterator of :class:`DatasetDocuments <mendeley.models.Dataset.DatasetDocument>`.
        """
        return super(DatasetSearch, self).iter(page_size)

    def _obj_type(self, **kwargs):
        return view_type(self.params['view'])

    @property
    def _url(self):
        return add_query_params('', self.params)

    @property
    def _session(self):
        return self.session


def view_type(view):
    return {
        'bib': datasetBibDocument,
        'client': datasetClientDocument,
        'stats': datasetStatsDocument,
        'all': datasetAllDocument,
        'core': datasetDocument
    }.get(view, datasetDocument)