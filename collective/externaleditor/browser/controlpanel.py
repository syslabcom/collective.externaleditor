from zope.interface import Interface
from zope.component import adapts
from zope.formlib import form
from zope.interface import implements
from zope.schema import List
from zope.schema import Tuple
from zope.schema import Choice

from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.interfaces import IPloneSiteRoot

from plone.app.controlpanel.form import ControlPanelForm


class IExternalEditorSchema(Interface):
    """
    """    
    externaleditor_enabled_types = List(
        title = _(u"label_externaleditor_enabled_types",
                  default=u"Content types editable with externaleditor"),
        required = False,
        default = ['File', 'Image', ],
        description = _(u"help_externaleditor_enabled_types",
                        default=u"Choose here the content types where the externaleditor action will be available"),
        value_type = Choice(title=u"externaleditor_enabled_types",
                            source="plone.app.vocabularies.ReallyUserFriendlyTypes"))


class ExternalEditorControlPanelAdapter(SchemaAdapterBase):
    """
    """
    adapts(IPloneSiteRoot)
    implements(IExternalEditorSchema)

    def __init__(self, context):
        super(ExternalEditorControlPanelAdapter, self).__init__(context)

    externaleditor_enabled_types = ProxyFieldProperty(IExternalEditorSchema['externaleditor_enabled_types'])


class ExternalEditorControlPanel(ControlPanelForm):
    """
    """
    form_fields = form.FormFields(IExternalEditorSchema)

    label = _("ExternalEditor settings")
    description = _("ExternalEditor settings.")
    form_name = _("ExternalEditor settings")
