import { writable } from 'svelte/store';
import { mockEvents, type EventInfo } from '$lib/mockEvents';
import { sortEventsChronologically } from '$lib/features/events/utils';

const initialEvents = sortEventsChronologically(mockEvents);
export const allEvents = writable<EventInfo[]>(initialEvents);

export function setAllEvents(events: EventInfo[]): void {
	allEvents.set(sortEventsChronologically(events));
}
