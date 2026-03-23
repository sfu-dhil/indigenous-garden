
from .models import WelcomePopup, History, ResidentialSchools, \
    ContextualEthicalFraming, RelationalInterconnectedTeachings, \
    Acknowledgements, OverheadMap

from .schema import WelcomePopupSchema, HistorySchema, ResidentialSchoolsSchema, \
    ContextualEthicalFramingSchema, RelationalInterconnectedTeachingsSchema, \
    AcknowledgementsSchema, OverheadMapSchema

def get_interface_content_dict():
    return {
        'welcome_popup': WelcomePopupSchema.from_orm(WelcomePopup.get_solo()).dict(),
        'history': HistorySchema.from_orm(History.get_solo()).dict(),
        'residential_schools': ResidentialSchoolsSchema.from_orm(ResidentialSchools.get_solo()).dict(),
        'contextual_ethical_framing': ContextualEthicalFramingSchema.from_orm(ContextualEthicalFraming.get_solo()).dict(),
        'relational_interconnected_teachings': RelationalInterconnectedTeachingsSchema.from_orm(RelationalInterconnectedTeachings.get_solo()).dict(),
        'acknowledgements': AcknowledgementsSchema.from_orm(Acknowledgements.get_solo()).dict(),
        'overhead_map': OverheadMapSchema.from_orm(OverheadMap.get_solo()).dict(),
    }