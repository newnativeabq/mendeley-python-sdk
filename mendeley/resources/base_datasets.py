from mendeley.resources.base import ListResource, GetByIdResource


class DatasetsBase(GetByIdResource, ListResource):
    def __init__(self, session, category):
        self.session = session
        self.category = category

    def get(self, id, view=None):
        return super(DatasetsBase, self).get(id, view=view)

    def list(self, page_size=None, order=None, article_doi=None, limit=None, fields=None, version=None):
        return super(DatasetsBase, self).list(page_size,
                                               article_doi=article_doi,
                                               limit=limit,
                                               fields=fields,
                                               version=version,
                                               order=order,
                                               category=self.category)

    def iter(self, page_size=None, order=None, article_doi=None, limit=None, fields=None, version=None):
        return super(DatasetsBase, self).iter(page_size,
                                               article_doi=article_doi,
                                               limit=limit,
                                               fields=fields,
                                               version=version,
                                               order=order,
                                               category=self.category)

    @property
    def _session(self):
        return self.session

    def _obj_type(self, **kwargs):
        return self.view_type(kwargs.get('view'))

    @staticmethod
    def view_type(view):
        raise NotImplementedError