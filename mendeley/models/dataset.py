from mendeley.models.base_documents import BaseDocument, BaseClientView, BaseBibView
from mendeley.response import LazyResponseObject


class Dataset(BaseDocument):
    """
    Base class for dataset documents.

    .. attribute:: id
    .. attribute:: title
    .. attribute:: type
    .. attribute:: source
    .. attribute:: year
    .. attribute:: identifiers
    .. attribute:: keywords
    .. attribute:: abstract
    .. attribute:: link
    """
    @property
    def files(self):
        """
        a :class:`Files <mendeley.resources.files.Files>` resource, from which
        :class:`Files <mendeley.models.files.File>` can be retrieved.
        """
        return self.session.dataset_files(dataset_id=self.id)

    @classmethod
    def fields(cls):
        return super(datasetDocument, cls).fields() + ['link']


class DatasetBibView(BaseBibView):
    """
    Additional fields returned when getting a :class:`datasetDocument <mendeley.models.dataset.datasetDocument>` with
    view='bib' or 'all'.

    .. attribute:: pages
    .. attribute:: volume
    .. attribute:: issue
    .. attribute:: websites
    .. attribute:: month
    .. attribute:: publisher
    .. attribute:: day
    .. attribute:: city
    .. attribute:: edition
    .. attribute:: institution
    .. attribute:: series
    .. attribute:: chapter
    .. attribute:: revision
    """
    pass


class DatasetClientView(BaseClientView):
    """
    Additional fields returned when getting a :class:`datasetDocument <mendeley.models.dataset.datasetDocument>` with
    view='client' or 'all'.

    .. attribute:: file_attached
    """
    pass


class DatasetStatsView(object):
    """
    Additional fields returned when getting a :class:`datasetDocument <mendeley.models.dataset.datasetDocument>` with
    view='stats' or 'all'.

    .. attribute:: reader_count
    .. attribute:: reader_count_by_academic_status
    .. attribute:: reader_count_by_subdiscipline
    .. attribute:: reader_count_by_country
    """
    @classmethod
    def fields(cls):
        return ['reader_count', 'reader_count_by_academic_status', 'reader_count_by_subdiscipline',
                'reader_count_by_country']


class DatasetBibDocument(DatasetBibView, DatasetDocument):
    @classmethod
    def fields(cls):
        return DatasetDocument.fields() + DatasetBibView.fields()


class DatasetClientDocument(DatasetClientView, DatasetDocument):
    @classmethod
    def fields(cls):
        return DatasetDocument.fields() + DatasetClientView.fields()


class DatasetStatsDocument(DatasetStatsView, DatasetDocument):
    @classmethod
    def fields(cls):
        return DatasetDocument.fields() + DatasetStatsView.fields()


class DatasetAllDocument(DatasetBibView, DatasetClientView, DatasetStatsView, DatasetDocument):
    @classmethod
    def fields(cls):
        return DatasetDocument.fields() + \
            DatasetBibView.fields() + \
            DatasetClientView.fields() + \
            DatasetStatsView.fields()


class LookupResponse(LazyResponseObject):
    def __init__(self, session, json, view, obj_type):
        super(LookupResponse, self).__init__(session, json['dataset_id'], obj_type, lambda: self._load())
        self.score = json['score']
        self.view = view

    def _load(self):
        return self.session.dataset.get(self.id, view=self.view)
