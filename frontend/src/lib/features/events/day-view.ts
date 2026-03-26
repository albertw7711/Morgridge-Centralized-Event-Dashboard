import type { EventInfo } from '$lib/mockEvents';
import { filterEventsByIsoDate } from '$lib/features/events/utils';

export function buildDayViewEvents(events: EventInfo[], selectedDate: string | null): EventInfo[] {
	return filterEventsByIsoDate(events, selectedDate);
}

export function toggleExpandedEvent(expandedEventIds: number[], eventId: number): number[] {
	return expandedEventIds.includes(eventId)
		? expandedEventIds.filter((currentId) => currentId !== eventId)
		: [...expandedEventIds, eventId];
}