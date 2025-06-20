from app.utils.env_constants import GOOGLE_CREDENTIALS_PATH

from langchain_core.tools import BaseTool
from langchain_google_community import (
    CalendarCreateEvent,
    CalendarDeleteEvent,
    CalendarUpdateEvent,
    CalendarSearchEvents,
    GetCalendarsInfo,
    GetCurrentDatetime,
)
from langchain_google_community.calendar.utils import get_google_credentials, build_resource_service

google_credentials = get_google_credentials(
    client_secrets_file=GOOGLE_CREDENTIALS_PATH,
    scopes=["https://www.googleapis.com/auth/calendar"],
)
api_resource = build_resource_service(google_credentials, service_name="calendar", service_version="v3")

def get_calendar_create_event_tool() -> BaseTool:
    return CalendarCreateEvent.from_api_resource(api_resource)

def get_calendar_delete_event_tool() -> BaseTool:
    return CalendarDeleteEvent.from_api_resource(api_resource)

def get_calendar_update_event_tool() -> BaseTool:
    return CalendarUpdateEvent.from_api_resource(api_resource)

def get_calendar_search_events_tool() -> BaseTool:
    return CalendarSearchEvents.from_api_resource(api_resource)

def get_calendars_info_tool() -> BaseTool:
    return GetCalendarsInfo.from_api_resource(api_resource)

def get_current_datetime_tool() -> BaseTool:
    return GetCurrentDatetime.from_api_resource(api_resource)