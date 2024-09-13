

import config
from utils import agendor


def new_register(name: str, phone: str) -> None:
    agendor_api = agendor.AgendorApi()

    agendor_client = agendor_api.list_organizations(phone=phone)[0]

    if agendor_client:
        client_deal = agendor_api.list_deals("organizations", agendor_client.get("id"))[0]
        funnel_name = client_deal.get("dealStage").get("funnel").get("name")
        if funnel_name == "Funil de SDR - Video AI":
            new_funnel = agendor_api.update_deal_stage(deal_id=client_deal.get("id"), deal_stage=1, funnel_id=752516)
            print(new_funnel)
            agendor_api.crea



new_register("Thiago", "558893842660")