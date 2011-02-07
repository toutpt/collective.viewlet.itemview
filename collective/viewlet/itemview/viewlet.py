from plone.app.layout.viewlets import common
from plone.memoize.instance import memoize
from zope import component
import logging
logger = logging.getLogger('collective.viewlet.itemview')

class Viewlet(common.ViewletBase):
    def index(self):
        target = self.target_up()
        try:
            view = component.getMultiAdapter((target, self.request),
                                             name="itemview_viewlet")
            return view()
        except component.ComponentLookupError:
            try:
                return target.restrictedTraverse('itemview_viewlet')()
            except AttributeError:
                logger.error()
        return ''

    def target_up(self):
        target_path= '/test'
        target = self.target(target_path)
        if not target:
            return None

    def target(self, target_path):
        if not target_path:
            return None

        if target_path.startswith('/'):
            target_path = target_path[1:]

        if not target_path:
            return None

        portal_state = component.getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        portal = portal_state.portal()
        if isinstance(target_path, unicode):
            #restrictedTraverse accept only strings
            target_path = str(target_path)
        return portal.restrictedTraverse(target_path, default=None)
