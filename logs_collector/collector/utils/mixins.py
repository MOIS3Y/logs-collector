class ExtraContextMixin:
    """The class adds additional context
        to all child view classes that inherit from it.
        Overrides the get_context_data method for CBV
    """

    title = 'Collector'

    def get_title(self, *args, **kwargs):
        """
        Return the class title attr by default,
        but you can override this method to further customize
        """
        return self.title

    def get_context_data(self, **kwargs):
        context = {}
        try:
            context = super().get_context_data(**kwargs)
        except Exception:
            pass
        context['title'] = self.get_title()
        return context
